$(document).ready(function () {
    // Buscar productos
    $("#buscarProducto").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#tablaProductos tbody tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });

    // Seleccionar productos
    $(".check-producto").on("change", function () {
        const id = $(this).data("id");
        const nombre = $(this).data("nombre");
        const precio = parseFloat($(this).data("precio"));

        if ($(this).is(":checked")) {
            // Agregar producto a la tabla de seleccionados
            const row = `
                <tr data-id="${id}">
                    <td>${nombre}</td>
                    <td>${precio.toFixed(2)}</td>
                    <td><input type="number" class="form-control cantidad" min="1" value="1" style="width:80px;"></td>
                    <td class="subtotal">${precio.toFixed(2)}</td>
                    <td><button type="button" class="btn btn-sm btn-danger eliminar">X</button></td>
                </tr>
            `;
            $("#tablaSeleccionados tbody").append(row);
            actualizarTotal();
        } else {
            $(`#tablaSeleccionados tr[data-id='${id}']`).remove();
            actualizarTotal();
        }
    });

    // Eliminar producto individual
    $(document).on("click", ".eliminar", function () {
        const row = $(this).closest("tr");
        const id = row.data("id");
        $(`.check-producto[data-id='${id}']`).prop("checked", false);
        row.remove();
        actualizarTotal();
    });

    // Cambiar cantidad
    $(document).on("input", ".cantidad", function () {
        const row = $(this).closest("tr");
        const cantidad = parseFloat($(this).val());
        const precio = parseFloat(row.find("td:eq(1)").text());
        const subtotal = precio * cantidad;
        row.find(".subtotal").text(subtotal.toFixed(2));
        actualizarTotal();
    });

    // Calcular total
    function actualizarTotal() {
        let total = 0;
        $("#tablaSeleccionados tbody tr").each(function () {
            total += parseFloat($(this).find(".subtotal").text());
        });
        $("#total").text(total.toFixed(2));
    }

    // Antes de enviar el formulario
    $("#formPedido").on("submit", function () {
        const productos = [];
        const cantidades = [];

        $("#tablaSeleccionados tbody tr").each(function () {
            productos.push($(this).data("id"));
            cantidades.push($(this).find(".cantidad").val());
        });

        $("#productosSeleccionados").val(productos.join(","));
        $("#cantidadesSeleccionadas").val(cantidades.join(","));
    });
});
