function abrirModal() {
    document.getElementById('modalProducto').style.display = 'block';
}

function cerrarModal() {
    document.getElementById('modalProducto').style.display = 'none';
}

document.getElementById('btnAgregarProducto').addEventListener('click', abrirModal);

window.onclick = function(event) {
    const modal = document.getElementById('modalProducto');
    if (event.target === modal) {
        cerrarModal();
    }

$(document).ready(function () {
    const tablaBody = $("#tablaProductos tbody");
    let productos = [];

    // Abrir modal
    $("#btnAgregarProducto").click(function () {
        $("#modalProducto").fadeIn(200);
    });

    // Cerrar modal
    window.cerrarModal = function () {
        $("#modalProducto").fadeOut(200);
        $("#formAgregarProducto")[0].reset();
    };

    // Envío AJAX del modal
    $("#formAgregarProducto").on("submit", function (e) {
        e.preventDefault();

        $.ajax({
            url: "/plato/ajax/agregar_producto/",
            method: "POST",
            data: $(this).serialize(),
            headers: { "X-CSRFToken": $("input[name=csrfmiddlewaretoken]").val() },
            success: function (response) {
                if (response.status === "ok") {
                    const prod = response.producto;
                    productos.push(prod);
                    actualizarTabla();
                    cerrarModal();
                }
            },
            error: function (xhr) {
                alert("Error al agregar producto: " + xhr.responseText);
            }
        });
    });

    // Actualizar tabla
    function actualizarTabla() {
        tablaBody.empty();
        productos.forEach((p, index) => {
            tablaBody.append(`
                <tr>
                    <td>${p.nombre}</td>
                    <td>${p.cantidad}</td>
                    <td>${p.unidad}</td>
                    <td><button type="button" class="btn btn-danger btn-sm" data-index="${index}">Eliminar</button></td>
                </tr>
            `);
        });
        $("#productos_json").val(JSON.stringify(productos));
    }

    // Eliminar fila
    tablaBody.on("click", ".btn-danger", function () {
        const index = $(this).data("index");
        productos.splice(index, 1);
        actualizarTabla();
    });
});

}
