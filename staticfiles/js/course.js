// message timeout
document.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {
    const messages = document.getElementById("messages");
    if (messages) {
      messages.style.transition = "opacity 0.1s ease";
      messages.style.opacity = "0";
      setTimeout(() => messages.remove(), 500);
    }
  }, 4000);
});
