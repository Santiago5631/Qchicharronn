if (!localStorage.getItem("theme")) {
  if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    document.documentElement.setAttribute("data-theme", "dark");
    localStorage.setItem("theme", "dark");
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.getElementById("theme-toggle");
  const html = document.documentElement;

  // Detectar tema guardado
  const currentTheme = localStorage.getItem("theme");

  if (currentTheme === "dark") {
    html.setAttribute("data-theme", "dark");
    toggle.checked = true;
  } else {
    toggle.checked = false;
  }

  toggle.addEventListener("change", function () {
    const isDark = this.checked;
    if (isDark) {
      html.setAttribute("data-theme", "dark");
      localStorage.setItem("theme", "dark");
    } else {
      html.removeAttribute("data-theme");
      localStorage.setItem("theme", "light");
    }
  });
});
