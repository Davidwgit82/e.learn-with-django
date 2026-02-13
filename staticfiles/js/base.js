document.addEventListener("click", (e) => {
  const link = e.target.closest("a");
  if (!link) return;

  const url = link.getAttribute("href");
  if (!url || url.startsWith("#") || url.startsWith("http")) return;

  const isSpecial =
    link.target === "_blank" ||
    link.hasAttribute("download") ||
    url.startsWith("mailto:") ||
    url.startsWith("tel:");

  if (isSpecial) return;

  e.preventDefault();
  navigate(url);
});

async function navigate(url, push = true) {
  try {
    const res = await fetch(url, {
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCSRFToken(), // Inclus par sécurité
      },
    });

    if (!res.ok) throw new Error(res.status);

    const html = await res.text();
    updatePage(html);

    if (push) history.pushState({}, "", url);
  } catch (err) {
    console.error("Navigation error:", err);
    // Optionnel : redirection classique si l'AJAX échoue
    // window.location.href = url;
  }
}

function updatePage(html) {
  const doc = new DOMParser().parseFromString(html, "text/html");
  const newMain = doc.querySelector("main");
  const currentMain = document.querySelector("main");

  if (newMain && currentMain) {
    currentMain.innerHTML = newMain.innerHTML;
  }
  document.title = doc.title;
}

window.addEventListener("popstate", () => {
  navigate(location.pathname, false);
});

function getCSRFToken() {
  return document.cookie
    .split("; ")
    .find((c) => c.trim().startsWith("csrftoken="))
    ?.split("=")[1];
}
