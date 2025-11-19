// sweetalert_delete.js
$(document).on("click", ".btn-delete", function (e) {
    console.log("CLICK DETECTADO");
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
                type: "POST",
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
                            location.reload();
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
