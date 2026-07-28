document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("theme-toggle-btn");
  const root = document.documentElement;
  const saved = localStorage.getItem("mb-theme");
  if (saved) root.setAttribute("data-theme", saved);

  if (toggleBtn) {
    toggleBtn.textContent = root.getAttribute("data-theme") === "dark" ? "☀️" : "🌙";
    toggleBtn.addEventListener("click", function () {
      const current = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", current);
      localStorage.setItem("mb-theme", current);
      toggleBtn.textContent = current === "dark" ? "☀️" : "🌙";
    });
  }

  document.querySelectorAll(".navbar-nav .nav-link").forEach(function (link) {
    if (link.getAttribute("href") === window.location.pathname) {
      link.classList.add("active-page");
    }
  });
});