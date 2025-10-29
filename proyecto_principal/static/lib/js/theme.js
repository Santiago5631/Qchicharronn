if (!localStorage.getItem("theme")) {
  if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    document.documentElement.setAttribute("data-theme", "dark");
    localStorage.setItem("theme", "dark");
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const btn = document.getElementById("theme-toggle");
  const html = document.documentElement;

  // Detectar tema guardado
  const currentTheme = localStorage.getItem("theme");

  if (currentTheme === "dark") {
    html.setAttribute("data-theme", "dark");
    btn.textContent = "☀️ Modo claro";
  } else {
    btn.textContent = "🌙 Modo oscuro";
  }

  btn.addEventListener("click", function () {
    const isDark = html.getAttribute("data-theme") === "dark";
    if (isDark) {
      html.removeAttribute("data-theme");
      localStorage.setItem("theme", "light");
      btn.textContent = "🌙 Modo oscuro";
    } else {
      html.setAttribute("data-theme", "dark");
      localStorage.setItem("theme", "dark");
      btn.textContent = "☀️ Modo claro";
    }
  });
});
