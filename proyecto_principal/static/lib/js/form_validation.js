//asd
$(function () {
    $("form").on("submit", function (e) {
        let valid = true;

        $(this).find("input, select, textarea").each(function () {
            let tipo = $(this).attr("type");

            // ignoramos botones, csrf y archivos
            if (tipo === "hidden" || tipo === "submit" || tipo === "button" || tipo === "file") {
                return;
            }

            // obtenemos el valor
            let valor = $(this).val();

            // si es null o vacío (solo espacios en texto)
            if (valor === null || (typeof valor === "string" && valor.trim() === "")) {
                valid = false;
            }
        });

        if (!valid) {
            e.preventDefault();
            Swal.fire({
                title: "Campos incompletos",
                text: "Por favor completa todos los campos antes de enviar.",
                icon: "warning",
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true
            });
        }
    });
});
//asdasd