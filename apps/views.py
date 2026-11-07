from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Cliente, Cita


@login_required
def inicio(request):
    return render(request, "control/inicio.html", {
        "total_clientes": Cliente.objects.count(),
        "total_citas": Cita.objects.count(),
    })


@login_required
def clientes(request):
    lista = Cliente.objects.all().order_by("-id")
    buscar = request.GET.get("buscar", "").strip()
    if buscar:
        lista = lista.filter(Q(nombre__icontains=buscar) |
                             Q(apellido__icontains=buscar) |
                             Q(dni__icontains=buscar))
    editar_id = request.GET.get("editar", "").strip()
    editar = get_object_or_404(Cliente, pk=editar_id) if editar_id else None
    return render(request, "control/clientes.html", {
        "clientes": lista, "buscar": buscar, "editar": editar,
    })


@login_required
@require_POST
def guardar_cliente(request):
    datos = {campo: request.POST.get(campo, "").strip()
             for campo in ("nombre", "apellido", "correo", "dni", "telefono")}
    id_cliente = request.POST.get("id_cliente", "").strip()
    if not all(datos[k] for k in ("nombre", "apellido", "correo", "dni")):
        messages.error(request, "Completa nombre, apellido, correo y DNI.")
        return redirect("clientes")
    if len(datos["dni"]) != 8 or not datos["dni"].isdigit():
        messages.error(request, "El DNI debe tener 8 dígitos.")
        return redirect("clientes")
    try:
        validate_email(datos["correo"])
    except ValidationError:
        messages.error(request, "Ingresa un correo válido.")
        return redirect("clientes")
    if any(len(datos[k]) > limite for k, limite in
           (("nombre", 100), ("apellido", 100), ("correo", 150),
            ("dni", 20), ("telefono", 30))):
        messages.error(request, "Uno de los campos supera su longitud máxima.")
        return redirect("clientes")
    try:
        if id_cliente:
            cliente = get_object_or_404(Cliente, pk=id_cliente)
            for campo, valor in datos.items():
                setattr(cliente, campo, valor)
            cliente.save()
            messages.success(request, "Cliente actualizado correctamente.")
        else:
            Cliente.objects.create(**datos)
            messages.success(request, "Cliente guardado correctamente.")
    except IntegrityError:
        messages.error(request, "El DNI ya está registrado.")
    return redirect("clientes")


@login_required
@require_POST
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    if cliente.citas.exists():
        messages.error(request, "No puedes eliminar un cliente que tiene citas.")
    else:
        cliente.delete()
        messages.success(request, "Cliente eliminado correctamente.")
    return redirect("clientes")


@login_required
def citas(request):
    lista = Cita.objects.select_related("cliente").order_by("fecha", "hora")
    buscar = request.GET.get("buscar", "").strip()
    if buscar:
        lista = lista.filter(Q(cliente__nombre__icontains=buscar) |
                             Q(cliente__apellido__icontains=buscar) |
                             Q(asunto__icontains=buscar) |
                             Q(estado__icontains=buscar))
    editar_id = request.GET.get("editar", "").strip()
    editar = get_object_or_404(Cita, pk=editar_id) if editar_id else None
    return render(request, "control/citas.html", {
        "citas": lista, "clientes": Cliente.objects.all().order_by("nombre"),
        "buscar": buscar, "editar": editar, "estados": Cita.ESTADOS,
    })


@login_required
@require_POST
def guardar_cita(request):
    id_cita = request.POST.get("id_cita", "").strip()
    id_cliente = request.POST.get("id_cliente", "").strip()
    datos = {campo: request.POST.get(campo, "").strip()
             for campo in ("asunto", "direccion", "referencia", "notas", "estado")}
    fecha_texto = request.POST.get("fecha", "").strip()
    hora_texto = request.POST.get("hora", "").strip()
    if not all((id_cliente, datos["asunto"], fecha_texto, hora_texto,
                datos["direccion"], datos["estado"])):
        messages.error(request, "Completa cliente, asunto, fecha, hora, dirección y estado.")
        return redirect("citas")
    if datos["estado"] not in dict(Cita.ESTADOS):
        messages.error(request, "Selecciona un estado válido.")
        return redirect("citas")
    if any(len(datos[k]) > limite for k, limite in
           (("asunto", 200), ("direccion", 255), ("referencia", 255))):
        messages.error(request, "Uno de los campos supera su longitud máxima.")
        return redirect("citas")
    try:
        fecha = datetime.strptime(fecha_texto, "%Y-%m-%d").date()
        hora = datetime.strptime(hora_texto, "%H:%M").time()
    except ValueError:
        messages.error(request, "Fecha u hora no válidas.")
        return redirect("citas")
    cliente = get_object_or_404(Cliente, pk=id_cliente)
    if id_cita:
        cita = get_object_or_404(Cita, pk=id_cita)
        cita.cliente = cliente
        cita.fecha, cita.hora = fecha, hora
        for campo, valor in datos.items():
            setattr(cita, campo, valor)
        cita.save()
        messages.success(request, "Cita actualizada.")
    else:
        Cita.objects.create(cliente=cliente, fecha=fecha, hora=hora, **datos)
        messages.success(request, "Cita guardada.")
    return redirect("citas")


@login_required
@require_POST
def eliminar_cita(request, id):
    get_object_or_404(Cita, pk=id).delete()
    messages.success(request, "Cita eliminada correctamente.")
    return redirect("citas")
