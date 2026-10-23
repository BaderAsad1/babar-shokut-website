/* Lightweight enhancements. Content, navigation and phone contact also work without JavaScript. */
(() => {
  "use strict";
  const menuButton = document.querySelector(".menu-toggle");
  const mobileMenu = document.getElementById("mobile-menu");
  const closeMenu = () => {
    if (!menuButton || !mobileMenu) return;
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", "Open navigation");
    mobileMenu.hidden = true;
    mobileMenu.dataset.open = "false";
  };
  if (menuButton && mobileMenu) {
    menuButton.addEventListener("click", () => {
      const open = menuButton.getAttribute("aria-expanded") !== "true";
      menuButton.setAttribute("aria-expanded", String(open));
      menuButton.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
      mobileMenu.hidden = !open;
      mobileMenu.dataset.open = String(open);
    });
    mobileMenu.querySelectorAll("a").forEach(link => link.addEventListener("click", closeMenu));
    document.addEventListener("keydown", event => {
      if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
        closeMenu(); menuButton.focus();
      }
    });
    window.matchMedia("(min-width: 1000px)").addEventListener("change", event => {
      if (event.matches) closeMenu();
    });
  }

  const dialog = document.getElementById("inspection-dialog");
  const form = document.getElementById("inspection-form");
  let opener = null;
  if (dialog && typeof dialog.showModal === "function" && form) {
    document.querySelectorAll(".open-enquiry").forEach(link => link.addEventListener("click", event => {
      event.preventDefault(); closeMenu(); opener = link;
      if (link.dataset.service) form.elements.appliance.value = link.dataset.service;
      document.getElementById("enquiry-status").textContent = "";
      document.getElementById("whatsapp-fallback").hidden = true;
      dialog.showModal();
      document.body.classList.add("dialog-open");
    }));
    dialog.querySelector(".dialog-close").addEventListener("click", () => dialog.close());
    dialog.addEventListener("click", event => {
      if (event.target !== dialog) return;
      const box = dialog.getBoundingClientRect();
      if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
    });
    dialog.addEventListener("close", () => {
      document.body.classList.remove("dialog-open");
      if (opener) opener.focus();
    });
    form.addEventListener("submit", event => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const data = new FormData(form);
      const issue = String(data.get("issue") || "").trim();
      const message = "Hi Bilal, I would like to enquire about an AED 50 inspection.\nAppliance: " +
        data.get("appliance") + "\nCity: " + data.get("city") +
        (issue ? "\nIssue: " + issue : "") + "\nPlease let me know the available arrangements.";
      const url = "https://wa.me/" + dialog.dataset.whatsapp + "?text=" + encodeURIComponent(message);
      const fallback = document.getElementById("whatsapp-fallback");
      fallback.href = url;
      fallback.hidden = false;
      document.getElementById("enquiry-status").textContent = "Your enquiry is ready. Send it in WhatsApp to contact Bilal. An appointment has not been confirmed.";
      window.open(url, "_blank", "noopener,noreferrer");
    });
  }

  const search = document.getElementById("guide-search");
  if (search) {
    const cards = Array.from(document.querySelectorAll(".article-card[data-category]"));
    const tabs = Array.from(document.querySelectorAll(".filter-button"));
    const feature = document.querySelector(".featured-guide");
    const count = document.querySelector(".result-count");
    const noResults = document.querySelector(".no-results");
    const clearButton = document.getElementById("clear-filters");
    let category = "all";
    const normalise = text => String(text).toLowerCase().replace(/[^\p{L}\p{N}\s]/gu, " ").replace(/\s+/g, " ").trim();
    const filter = () => {
      const query = normalise(search.value);
      const words = query.split(" ").filter(Boolean);
      const isDefault = category === "all" && !query;
      let matches = 0;
      cards.forEach(card => {
        const haystack = normalise(card.dataset.search);
        const match = (category === "all" || card.dataset.category === category) && words.every(word => haystack.includes(word));
        if (match) matches++;
        card.hidden = !match || (isDefault && card.dataset.featured === "true");
      });
      if (feature) feature.hidden = !isDefault;
      count.textContent = matches + (matches === 1 ? " guide found" : " guides found");
      noResults.hidden = matches !== 0;
      clearButton.hidden = isDefault;
      tabs.forEach(tab => tab.setAttribute("aria-pressed", String(tab.dataset.category === category)));
    };
    const reset = () => { category = "all"; search.value = ""; filter(); };
    tabs.forEach(tab => tab.addEventListener("click", () => { category = tab.dataset.category; filter(); }));
    search.addEventListener("input", filter);
    clearButton.addEventListener("click", reset);
    document.querySelectorAll("[data-reset-filters]").forEach(button => button.addEventListener("click", reset));
    document.querySelectorAll("[data-topic]").forEach(button => button.addEventListener("click", () => {
      category = "all"; search.value = button.dataset.topic; filter();
      document.querySelector(".advice-toolbar").scrollIntoView({behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth", block: "start"});
      search.focus({preventScroll:true});
    }));
    filter();
  }
})();
