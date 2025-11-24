$(document).ready(function () {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrf_token = getCookie('csrftoken');

    $(".btn-delete").on("click", function (e) {
        e.preventDefault();
        let url = $(this).data("url");
        let name = $(this).data("name");
        let button = $(this);

        Swal.fire({
            title: "¿Estás seguro?",
            text: `Se eliminará "${name}"`,
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
                    headers: {'X-CSRFToken': csrf_token},
                    success: function (response) {
                        if(response.success){
                            Swal.fire(
                                "Eliminado",
                                `"${response.nombre}" ha sido eliminado`,
                                "success"
                            );
                            // Eliminar fila de tabla si aplica
                            button.closest("tr").remove();
                        } else {
                            Swal.fire("Error", "No se pudo eliminar", "error");
                        }
                    },
                    error: function () {
                        Swal.fire("Error", "No se pudo eliminar", "error");
                    }
                });
            }
        });
    });
});
