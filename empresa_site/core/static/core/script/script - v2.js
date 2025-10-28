document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".sidebar button");
  const pages = document.querySelectorAll(".page");

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      // Atualiza destaque no menu
      buttons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      // Mostra a página correspondente
      const targetId = btn.dataset.target;
      pages.forEach(page => {
        page.classList.toggle("active", page.id === targetId);
      });
    });
  });
});
