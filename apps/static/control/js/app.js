// Confirmación antes de eliminar; se conserva el comportamiento de V1.
document.querySelectorAll(".form-eliminar").forEach(function (formulario) {
    formulario.addEventListener("submit", function (evento) {
        if (!confirm("¿Seguro que deseas eliminar este registro?")) {
            evento.preventDefault();
        }
    });
});
