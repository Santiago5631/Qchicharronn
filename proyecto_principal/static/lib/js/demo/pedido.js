$(document).ready(function() {
    const tablaProductos = $("#tablaProductos");
    const tablaSeleccionados = $("#tablaSeleccionados tbody");
    const totalElement = $("#total");
    const buscarProducto = $("#buscarProducto");

    // Filtrar productos en tiempo real
    buscarProducto.on("keyup", function() {
        const valor = $(this).val().toLowerCase();
        tablaProductos.find("tbody tr").each(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(valor) > -1);
        });
    });

    // Seleccionar productos
    tablaProductos.on("change", ".check-producto", function() {
        const checkbox = $(this);
        const id = checkbox.data("id");
        const nombre = checkbox.data("nombre");
        const precio = parseFloat(checkbox.data("precio")) || 0;

        if (checkbox.is(":checked")) {
            // Crear fila en tabla de seleccionados
            const fila = `
                <tr data-id="${id}">
                    <td>${nombre}</td>
                    <td class="precio">${precio.toFixed(2)}</td>
                    <td><input type="number" value="1" min="1" class="form-control cantidad"></td>
                    <td class="subtotal">${precio.toFixed(2)}</td>
                    <td><button type="button" class="btn btn-danger btn-sm eliminar">X</button></td>
                </tr>
            `;
            tablaSeleccionados.append(fila);
        } else {
            // Quitar producto si se desmarca
            tablaSeleccionados.find(`tr[data-id="${id}"]`).remove();
        }

        actualizarTotal();
    });

    // Cambiar cantidad
    tablaSeleccionados.on("input", ".cantidad", function() {
        const fila = $(this).closest("tr");
        const precio = parseFloat(fila.find(".precio").text());
        const cantidad = parseInt($(this).val());
        const subtotal = precio * cantidad;
        fila.find(".subtotal").text(subtotal.toFixed(2));
        actualizarTotal();
    });

    // Eliminar producto
    tablaSeleccionados.on("click", ".eliminar", function() {
        const fila = $(this).closest("tr");
        const id = fila.data("id");
        fila.remove();
        tablaProductos.find(`.check-producto[data-id="${id}"]`).prop("checked", false);
        actualizarTotal();
    });

    // Calcular total general
    function actualizarTotal() {
        let total = 0;
        tablaSeleccionados.find(".subtotal").each(function() {
            total += parseFloat($(this).text()) || 0;
        });
        totalElement.text(total.toFixed(2));
    }
});
