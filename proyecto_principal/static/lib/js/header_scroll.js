let lastScrollTop = 0;

window.addEventListener("scroll", function() {
    const header = document.getElementById("mainHeader");
    let currentScroll = window.pageYOffset || document.documentElement.scrollTop;

    if (currentScroll > lastScrollTop && currentScroll > 100) {
        // Bajando → ocultar
        header.style.transform = "translateY(-150%)";
    } else {
        // Subiendo → mostrar
        header.style.transform = "translateY(0)";
    }

    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
});