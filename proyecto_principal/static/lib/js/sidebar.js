const body       = document.querySelector("body"),
      sidebar    = body.querySelector(".sidebar"),
      toggle     = body.querySelector(".toggle"),
      searchBtn  = body.querySelector(".search-box"),
      modeSwitch = body.querySelector(".toggle-switch"),  // switch de la sidebar
      modeText   = body.querySelector(".mode-text");      // texto de la sidebar

// Switches adicionales
const navbarModeSwitch  = document.getElementById("navbar-mode-switch");   // desktop navbar
const navbarModeText    = document.getElementById("navbar-mode-text");
const navbarIconMoon    = document.getElementById("navbar-icon-moon");
const navbarIconSun     = document.getElementById("navbar-icon-sun");
const mobileModeSwitch  = document.getElementById("mobile-mode-switch");   // offcanvas móvil
const mobileModeText    = document.getElementById("mobile-mode-text");

// ══════════════════════════════════════
// FUNCIÓN: Aplicar modo oscuro
// Sincroniza todos los switches
// ══════════════════════════════════════
function aplicarModoOscuro(activar) {
    if (activar) {
        body.classList.add("dark");

        // Sidebar desktop
        if (modeText) modeText.innerText = "Modo Claro";

        // Navbar desktop
        if (navbarModeText)  navbarModeText.innerText    = "Modo Claro";
        if (navbarIconMoon)  navbarIconMoon.style.display = "none";
        if (navbarIconSun)   navbarIconSun.style.display  = "";

        // Offcanvas móvil
        if (mobileModeText) mobileModeText.innerText = "Modo Claro";

        localStorage.setItem("dark-mode", "enabled");

    } else {
        body.classList.remove("dark");

        // Sidebar desktop
        if (modeText) modeText.innerText = "Modo Oscuro";

        // Navbar desktop
        if (navbarModeText)  navbarModeText.innerText    = "Modo Oscuro";
        if (navbarIconMoon)  navbarIconMoon.style.display = "";
        if (navbarIconSun)   navbarIconSun.style.display  = "none";

        // Offcanvas móvil
        if (mobileModeText) mobileModeText.innerText = "Modo Oscuro";

        localStorage.setItem("dark-mode", "disabled");
    }
}

function esMobile() {
    return window.innerWidth < 992;
}

// ══════════════════════════════════════
// CARGAR ESTADO INICIAL
// ══════════════════════════════════════
document.addEventListener("DOMContentLoaded", () => {

    // Estado modo oscuro
    const darkMode = localStorage.getItem("dark-mode");
    aplicarModoOscuro(darkMode === "enabled");

    // Estado sidebar (siempre visible en desktop, oculta en móvil)
    if (!esMobile()) {
        const sidebarStatus = localStorage.getItem("sidebar-status");
        if (sidebarStatus === "closed") {
            sidebar.classList.add("close");
        } else {
            sidebar.classList.remove("close");
        }
        sidebar.style.display = "";
    } else {
        sidebar.style.display = "none";
    }

});

// ══════════════════════════════════════
// TOGGLE SIDEBAR (solo desktop)
// ══════════════════════════════════════
if (toggle) {
    toggle.addEventListener("click", () => {
        if (esMobile()) return;

        sidebar.classList.toggle("close");
        localStorage.setItem(
            "sidebar-status",
            sidebar.classList.contains("close") ? "closed" : "open"
        );
    });
}

// ══════════════════════════════════════
// MODO OSCURO — Switch sidebar desktop
// ══════════════════════════════════════
if (modeSwitch) {
    modeSwitch.addEventListener("click", () => {
        aplicarModoOscuro(!body.classList.contains("dark"));
    });
}

// ══════════════════════════════════════
// MODO OSCURO — Switch navbar desktop
// ══════════════════════════════════════
if (navbarModeSwitch) {
    navbarModeSwitch.addEventListener("click", () => {
        aplicarModoOscuro(!body.classList.contains("dark"));
    });
}

// ══════════════════════════════════════
// MODO OSCURO — Switch offcanvas móvil
// ══════════════════════════════════════
if (mobileModeSwitch) {
    mobileModeSwitch.addEventListener("click", () => {
        aplicarModoOscuro(!body.classList.contains("dark"));
    });
}

// ══════════════════════════════════════
// RESIZE: mostrar/ocultar sidebar
// ══════════════════════════════════════
window.addEventListener("resize", () => {
    if (esMobile()) {
        sidebar.style.display = "none";
    } else {
        sidebar.style.display = "";
        const sidebarStatus = localStorage.getItem("sidebar-status");
        if (sidebarStatus === "closed") {
            sidebar.classList.add("close");
        } else {
            sidebar.classList.remove("close");
        }
    }
});

// ══════════════════════════════════════
// SEARCH BOX
// ══════════════════════════════════════
const sidebarSearch = document.getElementById('sidebar-search');

if (sidebarSearch) {
    sidebarSearch.addEventListener('input', function() {
        const query = this.value.toLowerCase().trim();
        const links = document.querySelectorAll('.menu-links .nav-link');

        links.forEach(li => {
            const texto = li.querySelector('.nav-text');
            if (!texto) return;

            const nombre = texto.textContent.toLowerCase();
            li.style.display = nombre.includes(query) ? '' : 'none';
        });
    });
}