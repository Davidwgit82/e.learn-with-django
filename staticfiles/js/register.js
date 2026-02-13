// mask on/off password
function togglePassword(fieldId, btn) {
  const input = document.getElementById(fieldId);
  if (input.type === "password") {
    input.type = "text";
    // Change l'icône pour un oeil barré (optionnel)
    btn.classList.add("text-blue-600");
  } else {
    input.type = "password";
    btn.classList.remove("text-blue-600");
  }
}
