from django.db import models


class Cita(models.Model):
    ESTADOS = [
        ("Pendiente", "Pendiente"),
        ("Confirmada", "Confirmada"),
        ("Completada", "Completada"),
        ("Cancelada", "Cancelada"),
    ]

    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey("apps.Cliente", on_delete=models.PROTECT,
                                related_name="citas", db_column="client_id")
    asunto = models.CharField(max_length=200)
    fecha = models.DateField()
    hora = models.TimeField()
    direccion = models.CharField(max_length=255)
    referencia = models.CharField(max_length=255, blank=True)
    notas = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="Pendiente")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "citas"
        ordering = ["fecha", "hora"]

    def __str__(self):
        return self.asunto
