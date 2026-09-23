/* Octavio Gregorio — portfolio. No dependencies. */
(() => {
  "use strict";

  // ---- Config -------------------------------------------------------------
  const EMAIL = "octavio.ogg+pf@gmail.com";

  const root = document.documentElement;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch { /* private mode */ } },
  };
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)");

  // ---- Strings used from JS ----------------------------------------------
  const T = {
    es: {
      copied: "Copiado",
      menuOpen: "Abrir menú",
      menuClose: "Cerrar menú",
      toDark: "Activar modo oscuro",
      toLight: "Activar modo claro",
    },
    en: {
      copied: "Copied",
      menuOpen: "Open menu",
      menuClose: "Close menu",
      toDark: "Switch to dark mode",
      toLight: "Switch to light mode",
    },
  };
  const lang = () => (root.lang === "en" ? "en" : "es");
  const t = (k, ...a) => { const v = T[lang()][k]; return typeof v === "function" ? v(...a) : v; };

  // ---- Language -----------------------------------------------------------
  // Long copy lives in paired elements (lang="es" / lang="en") and CSS hides
  // the inactive one. Attributes use data-es-* / data-en-* (e.g. data-en-placeholder).
  function applyLang(l) {
    root.lang = l;
    $$("*").forEach((el) => {
      for (const { name, value } of Array.from(el.attributes)) {
        if (!name.startsWith(`data-${l}-`)) continue;
        const attr = name.slice(l.length + 6);
        if (attr === "text") el.textContent = value;
        else el.setAttribute(attr, value);
      }
    });
    const title = root.getAttribute(`data-${l}-title`);
    if (title) document.title = title;
    $$(".lang-toggle").forEach((b) => b.setAttribute("aria-label", l === "es" ? "Switch to English" : "Cambiar a español"));
    syncThemeLabel();
    document.dispatchEvent(new CustomEvent("langchange"));
  }

  $$(".lang-toggle").forEach((btn) =>
    btn.addEventListener("click", () => {
      const next = lang() === "es" ? "en" : "es";
      store.set("lang", next);
      applyLang(next);
    })
  );
  if (lang() === "en") applyLang("en");

  // ---- Theme --------------------------------------------------------------
  const themeMeta = $('meta[name="theme-color"]');
  function syncThemeLabel() {
    const dark = root.dataset.theme === "dark";
    $$(".theme-toggle").forEach((b) => {
      b.setAttribute("aria-label", dark ? t("toLight") : t("toDark"));
      b.setAttribute("aria-pressed", String(dark));
    });
    if (themeMeta) themeMeta.content = dark ? "#121019" : "#f4f1ea";
  }
  function setTheme(v) { root.dataset.theme = v; syncThemeLabel(); }

  $$(".theme-toggle").forEach((btn) =>
    btn.addEventListener("click", () => {
      const next = root.dataset.theme === "dark" ? "light" : "dark";
      store.set("theme", next);
      // Swap without every transition on the page firing at once
      root.classList.add("theme-swap");
      setTheme(next);
      requestAnimationFrame(() => requestAnimationFrame(() => root.classList.remove("theme-swap")));
    })
  );
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
    if (!store.get("theme")) setTheme(e.matches ? "dark" : "light");
  });
  syncThemeLabel();

  // ---- Header / menu ------------------------------------------------------
  const header = $(".site-header");
  const menuBtn = $(".menu-btn");
  const menu = $("#mobile-menu");

  function setMenu(open) {
    if (!menu || !menuBtn) return;
    menuBtn.setAttribute("aria-expanded", String(open));
    menuBtn.setAttribute("aria-label", open ? t("menuClose") : t("menuOpen"));
    menu.toggleAttribute("data-open", open);
    menu.inert = !open;
  }
  if (menu) {
    menu.inert = true;
    menuBtn.addEventListener("click", () => setMenu(menuBtn.getAttribute("aria-expanded") !== "true"));
    $$("a", menu).forEach((a) => a.addEventListener("click", () => setMenu(false)));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && menu.hasAttribute("data-open")) { setMenu(false); menuBtn.focus(); }
    });
    matchMedia("(min-width: 861px)").addEventListener("change", (e) => e.matches && setMenu(false));
  }

  // ---- Scroll-driven bits (one passive listener) --------------------------
  const toTop = $(".to-top");
  let ticking = false;
  function onScroll() {
    const y = scrollY;
    header && header.toggleAttribute("data-scrolled", y > 8);
    toTop && toTop.toggleAttribute("data-show", y > 900);
    ticking = false;
  }
  addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  toTop && toTop.addEventListener("click", () => {
    scrollTo({ top: 0, behavior: reduceMotion.matches ? "auto" : "smooth" });
    const target = $("#main");
    target && target.focus({ preventScroll: true });
  });

  // ---- Mobile CTA: visible once the hero CTA is gone, hidden near contact --
  const mcta = $(".mobile-cta");
  if (mcta && "IntersectionObserver" in window) {
    document.body.classList.add("has-mobile-cta");
    const trigger = $("[data-cta-trigger]");
    const hideZones = $$("[data-cta-hide]");
    let pastTrigger = !trigger;
    const hidden = new Set();
    const sync = () => {
      const show = pastTrigger && hidden.size === 0;
      mcta.toggleAttribute("data-show", show);
      mcta.inert = !show;
      toTop && toTop.toggleAttribute("data-lift", show);
    };
    if (trigger) {
      new IntersectionObserver(([e]) => {
        pastTrigger = !e.isIntersecting && e.boundingClientRect.top < 0;
        sync();
      }).observe(trigger);
    }
    const hz = new IntersectionObserver((entries) => {
      entries.forEach((e) => (e.isIntersecting ? hidden.add(e.target) : hidden.delete(e.target)));
      sync();
    });
    hideZones.forEach((z) => hz.observe(z));
    sync();
  }

  // ---- Scroll reveal (once) ----------------------------------------------
  const revealables = $$("[data-reveal]");
  if ("IntersectionObserver" in window && !reduceMotion.matches) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        e.target.classList.add("is-in");
        io.unobserve(e.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealables.forEach((el) => io.observe(el));
  } else {
    revealables.forEach((el) => el.classList.add("is-in"));
  }

  // ---- Active section in nav / table of contents --------------------------
  function trackActive(links) {
    const map = new Map();
    links.forEach((a) => {
      const id = decodeURIComponent(a.hash.slice(1));
      const sec = id && document.getElementById(id);
      if (sec) map.set(sec, a);
    });
    if (!map.size) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        links.forEach((l) => l.classList.remove("is-active"));
        map.get(e.target).classList.add("is-active");
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    map.forEach((_, sec) => io.observe(sec));
  }
  trackActive($$('.site-nav a[href^="#"]'));
  trackActive($$(".toc a"));

  // ---- Skeletons: fade media in once decoded ------------------------------
  $$(".skel img").forEach((img) => {
    const done = () => img.closest(".skel").classList.add("is-loaded");
    if (img.complete && img.naturalWidth) done();
    else { img.addEventListener("load", done, { once: true }); img.addEventListener("error", done, { once: true }); }
  });

  // ---- Copy email ---------------------------------------------------------
  $$(".copy-email").forEach((btn) => {
    let timer;
    btn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(btn.dataset.copy || EMAIL);
        btn.setAttribute("data-copied", "");
        const live = $(".done", btn);
        live && live.setAttribute("aria-live", "polite");
        clearTimeout(timer);
        timer = setTimeout(() => btn.removeAttribute("data-copied"), 1800);
      } catch {
        location.href = `mailto:${btn.dataset.copy || EMAIL}`;
      }
    });
  });

  // ---- YouTube facade -----------------------------------------------------
  $$(".yt[data-id]").forEach((box) => {
    const btn = $("button", box);
    btn && btn.addEventListener("click", () => {
      const f = document.createElement("iframe");
      f.src = `https://www.youtube-nocookie.com/embed/${box.dataset.id}?autoplay=1&rel=0`;
      f.title = box.dataset.title || "YouTube";
      f.allow = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen";
      f.allowFullscreen = true;
      box.replaceChildren(f);
    });
  });

  // ---- Lightbox -----------------------------------------------------------
  const lb = $("#lightbox");
  if (lb) {
    const img = $("img", lb);
    const cap = $("p", lb);
    $$(".gallery button[data-full]").forEach((b) =>
      b.addEventListener("click", () => {
        const thumb = $("img", b);
        img.src = b.dataset.full;
        img.alt = thumb ? thumb.alt : "";
        cap.textContent = thumb ? thumb.alt : "";
        lb.showModal();
      })
    );
    lb.addEventListener("click", (e) => { if (e.target === lb) lb.close(); });
    $(".close", lb).addEventListener("click", () => lb.close());
  }

})();
