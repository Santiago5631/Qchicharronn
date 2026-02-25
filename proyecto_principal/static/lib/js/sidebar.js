const body = document.querySelector("body"),
      sidebar = body.querySelector(".sidebar"),
      toggle = body.querySelector(".toggle"),
      searchBtn = body.querySelector(".search-box"),
      modeSwitch = body.querySelector(".toggle-switch"),
      modeText = body.querySelector(".mode-text");

// Cargar estado inicial desde localStorage
document.addEventListener("DOMContentLoaded", () => {
      // Estado de la Sidebar
      const sidebarStatus = localStorage.getItem("sidebar-status");
      if (sidebarStatus === "closed") {
            sidebar.classList.add("close");
      } else {
            sidebar.classList.remove("close");
      }

      // Estado del Modo Oscuro
      const darkMode = localStorage.getItem("dark-mode");
      if (darkMode === "enabled") {
            body.classList.add("dark");
            modeText.innerText = "Modo Claro";
      }
});

toggle.addEventListener("click", () => {
      sidebar.classList.toggle("close");
      // Guardar estado
      if (sidebar.classList.contains("close")) {
            localStorage.setItem("sidebar-status", "closed");
      } else {
            localStorage.setItem("sidebar-status", "open");
      }
});

searchBtn.addEventListener("click", () => {
      // sidebar.classList.remove("close");
      // localStorage.setItem("sidebar-status", "open");
});

modeSwitch.addEventListener("click", () => {
      body.classList.toggle("dark");

      if (body.classList.contains("dark")) {
            modeText.innerText = "Modo Claro";
            localStorage.setItem("dark-mode", "enabled");
      } else {
            modeText.innerText = "Modo Oscuro";
            localStorage.setItem("dark-mode", "disabled");
      }
});