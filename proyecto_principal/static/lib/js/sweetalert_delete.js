// sweetalert_delete.js
$(function () {
    $(".btn-delete").on("click", function (e) {
        e.preventDefault();

        let url = $(this).data("url");
        let name = $(this).data("name");

        Swal.fire({
            title: "¿Estás seguro?",
            text: `Se eliminará ${name}`,
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#3085d6",
            confirmButtonText: "Sí, eliminar",
            cancelButtonText: "Cancelar"
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: url,
                    type: "POST",   // importante, Django espera POST en delete()
                    data: {
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
                    },
                    success: function (response) {
                        if (response.status === "ok") {
                            Swal.fire(
                                "Eliminado!",
                                `${name} fue eliminado correctamente.`,
                                "success"
                            ).then(() => {
                                location.reload(); // recarga la tabla
                            });
                        }
                    },
                    error: function (xhr, status, error) {
                        Swal.fire("Error", "No se pudo eliminar", "error");
                        console.error(error);
                    }
                });
            }
        });
    });
});
// End of sweetalert_delete.js