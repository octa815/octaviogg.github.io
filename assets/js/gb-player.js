/* Tower Hero player: wires gb-core.js to the page (screen, sound, keyboard,
   touch buttons, gamepad, pause/reset/fullscreen, battery save). */
(() => {
  "use strict";
  const box = document.getElementById("gb");
  if (!box) return;

  const $ = (s) => box.querySelector(s);
  const canvas = $("#gb-canvas");
  const powerBtn = $("#gb-power");
  const msg = $("#gb-msg");
  const pauseBtn = $("#gb-pause");
  const resetBtn = $("#gb-reset");
  const fullBtn = $("#gb-full");
  const soundBtn = $("#gb-sound");
  const ROM_URL = box.dataset.rom;
  const SAVE_KEY = "towerhero-save";

  const TXT = {
    es: { loading: "Cargando…", error: "No se ha podido cargar el juego. Recarga la página.", pause: "Pausa", resume: "Continuar", paused: "En pausa", soundOn: "Sonido: sí", soundOff: "Sonido: no", full: "Pantalla completa", exitFull: "Salir de pantalla completa", hint: "Pulsa START para empezar" },
    en: { loading: "Loading…", error: "Couldn't load the game. Please reload the page.", pause: "Pause", resume: "Resume", paused: "Paused", soundOn: "Sound: on", soundOff: "Sound: off", full: "Fullscreen", exitFull: "Exit fullscreen", hint: "Press START to begin" },
    zh: { loading: "載入中…", error: "無法載入遊戲，請重新整理頁面。", pause: "暫停", resume: "繼續", paused: "已暫停", soundOn: "聲音：開", soundOff: "聲音：關", full: "全螢幕", exitFull: "離開全螢幕", hint: "按 START 開始" },
  };
  const t = (k) => {
    const l = document.documentElement.lang;
    return (TXT[l === "zh-Hant" ? "zh" : l] || TXT.es)[k];
  };
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch { /* ignore */ } },
  };

  let gb = null, ctx2d = null, image = null, pixels = null;
  let running = false, userPaused = false, autoPaused = false;
  let raf = 0, last = 0, acc = 0;
  let audio = null, sound = store.get("gb-sound") !== "off";
  let saveTimer = 0;

  function say(text, sticky) {
    msg.textContent = text;
    msg.hidden = !text;
    clearTimeout(say.timer);
    if (text && !sticky) say.timer = setTimeout(() => (msg.hidden = true), 2500);
  }

  function labels() {
    pauseBtn.textContent = userPaused ? t("resume") : t("pause");
    soundBtn.textContent = sound ? t("soundOn") : t("soundOff");
    soundBtn.setAttribute("aria-pressed", String(sound));
    fullBtn.textContent = document.fullscreenElement ? t("exitFull") : t("full");
  }
  document.addEventListener("langchange", labels);
  labels();

  // ---- Loading ------------------------------------------------------------
  function loadCore() {
    if (window.GBCore) return Promise.resolve();
    return new Promise((ok, fail) => {
      const s = document.createElement("script");
      s.src = "assets/js/gb-core.js?v=" + (document.querySelector('script[src*="gb-player.js"]').src.split("v=")[1] || "");
      s.onload = ok;
      s.onerror = fail;
      document.head.appendChild(s);
    });
  }

  async function power() {
    powerBtn.disabled = true;
    say(t("loading"), true);
    try {
      const [rom] = await Promise.all([fetch(ROM_URL).then((r) => { if (!r.ok) throw r; return r.arrayBuffer(); }), loadCore()]);
      startAudio();
      gb = new window.GBCore.GB(new Uint8Array(rom), { sampleRate: audio ? audio.ctx.sampleRate : 44100 });
      const saved = store.get(SAVE_KEY);
      if (saved) gb.loadData(Uint8Array.from(atob(saved), (c) => c.charCodeAt(0)));
      ctx2d = canvas.getContext("2d");
      image = ctx2d.createImageData(160, 144);
      pixels = new Uint32Array(image.data.buffer);
      box.setAttribute("data-on", "");
      [pauseBtn, resetBtn, fullBtn, soundBtn].forEach((b) => (b.disabled = false));
      running = true;
      say(t("hint"));
      canvas.focus({ preventScroll: true });
      last = performance.now();
      raf = requestAnimationFrame(loop);
    } catch {
      powerBtn.disabled = false;
      say(t("error"), true);
    }
  }
  powerBtn.addEventListener("click", power);

  // ---- Main loop ----------------------------------------------------------
  function loop(now) {
    raf = requestAnimationFrame(loop);
    if (!running || userPaused || autoPaused) { last = now; return; }
    const frameMs = 1000 / window.GBCore.FPS;
    acc += Math.min(now - last, 100);
    last = now;
    pollGamepad();
    let n = 0;
    while (acc >= frameMs && n < 4) { gb.runFrame(); acc -= frameMs; n++; }
    if (n) {
      pixels.set(gb.frame);
      ctx2d.putImageData(image, 0, 0);
      feedAudio();
    }
    if (gb.ramDirty && now - saveTimer > 3000) persist(now);
  }

  function persist(now) {
    if (!gb || !gb.ramDirty) return;
    const d = gb.saveData();
    if (!d) return;
    let s = "";
    for (let i = 0; i < d.length; i++) s += String.fromCharCode(d[i]);
    store.set(SAVE_KEY, btoa(s));
    gb.ramDirty = false;
    saveTimer = now || performance.now();
  }

  // ---- Audio (ring buffer fed each frame) ---------------------------------
  function startAudio() {
    if (audio) return;
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return;
    const ctx = new AC();
    const size = 16384;
    const ring = new Float32Array(size * 2);
    let rd = 0, wr = 0;
    const gain = ctx.createGain();
    gain.gain.value = sound ? 0.6 : 0;
    const node = ctx.createScriptProcessor(1024, 0, 2);
    node.onaudioprocess = (e) => {
      const L = e.outputBuffer.getChannelData(0), R = e.outputBuffer.getChannelData(1);
      for (let i = 0; i < L.length; i++) {
        if (rd !== wr) { L[i] = ring[rd]; R[i] = ring[rd + 1]; rd = (rd + 2) % ring.length; }
        else { L[i] = 0; R[i] = 0; }
      }
    };
    node.connect(gain);
    gain.connect(ctx.destination);
    audio = {
      ctx, gain,
      push(buf) {
        const queued = (wr - rd + ring.length) % ring.length;
        if (queued > ctx.sampleRate * 0.2) return; // too far ahead: drop to keep latency low
        for (let i = 0; i < buf.length; i += 2) {
          ring[wr] = buf[i]; ring[wr + 1] = buf[i + 1];
          wr = (wr + 2) % ring.length;
          if (wr === rd) rd = (rd + 2) % ring.length;
        }
      },
      flush() { rd = wr; },
    };
  }
  function feedAudio() {
    const buf = gb.apu.take();
    if (audio && sound) audio.push(buf);
  }
  soundBtn.addEventListener("click", () => {
    sound = !sound;
    store.set("gb-sound", sound ? "on" : "off");
    if (audio) { audio.gain.gain.value = sound ? 0.6 : 0; if (!sound) audio.flush(); if (sound) audio.ctx.resume(); }
    labels();
  });

  // ---- Pause, reset, fullscreen -------------------------------------------
  function setUserPause(p) {
    userPaused = p;
    labels();
    if (p) { say(t("paused"), true); persist(); if (audio) audio.flush(); }
    else { say(""); if (audio) audio.ctx.resume(); }
  }
  pauseBtn.addEventListener("click", () => setUserPause(!userPaused));
  resetBtn.addEventListener("click", () => { if (!gb) return; persist(); gb.reset(); const s = store.get(SAVE_KEY); if (s) gb.loadData(Uint8Array.from(atob(s), (c) => c.charCodeAt(0))); setUserPause(false); canvas.focus({ preventScroll: true }); });
  fullBtn.addEventListener("click", () => {
    if (document.fullscreenElement) document.exitFullscreen();
    else if (box.requestFullscreen) box.requestFullscreen().catch(() => {});
  });
  document.addEventListener("fullscreenchange", labels);

  // Stop when the tab is hidden or the console scrolls off-screen.
  document.addEventListener("visibilitychange", () => {
    autoPaused = document.hidden || offscreen;
    if (document.hidden) { persist(); if (audio) audio.flush(); }
  });
  let offscreen = false;
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(([e]) => {
      offscreen = !e.isIntersecting;
      document.body.classList.toggle("gb-in-view", e.isIntersecting);
      autoPaused = offscreen || document.hidden;
      if (offscreen && audio) audio.flush();
    }, { threshold: 0.15 }).observe(box.querySelector(".gb-lcd"));
  }
  addEventListener("pagehide", () => persist());

  // ---- Keyboard -----------------------------------------------------------
  const KEYS = {
    ArrowUp: "up", ArrowDown: "down", ArrowLeft: "left", ArrowRight: "right",
    KeyW: "up", KeyS: "down", KeyA: "left", KeyD: "right",
    KeyF: "a",
    Enter: "start", NumpadEnter: "start",
  };
  const typing = (el) => el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName));
  function onKey(e, down) {
    if (!running || userPaused || typing(document.activeElement)) return;
    const b = KEYS[e.code];
    if (!b || offscreen) return;
    // Enter/Space on a focused button keeps its normal meaning.
    if (e.code === "Enter" && document.activeElement && document.activeElement.tagName === "BUTTON" && !box.contains(document.activeElement)) return;
    e.preventDefault();
    press(b, down);
  }
  addEventListener("keydown", (e) => { if (!e.repeat) onKey(e, true); else if (KEYS[e.code] && running && !offscreen) e.preventDefault(); });
  addEventListener("keyup", (e) => onKey(e, false));
  addEventListener("blur", releaseAll);

  // ---- On-screen buttons (pointer events; slide across the D-pad) --------
  const held = new Map(); // pointerId -> button name
  const counts = {};
  function press(b, down) {
    counts[b] = Math.max(0, (counts[b] || 0) + (down ? 1 : -1));
    const on = counts[b] > 0;
    if (gb) gb.setButton(b, on);
    box.querySelectorAll(`[data-btn="${b}"]`).forEach((el) => el.toggleAttribute("data-pressed", on));
  }
  function releaseAll() {
    Object.keys(counts).forEach((b) => { counts[b] = 0; if (gb) gb.setButton(b, false); });
    box.querySelectorAll("[data-pressed]").forEach((el) => el.removeAttribute("data-pressed"));
    held.clear();
  }
  const controls = $(".gb-controls");
  controls.addEventListener("pointerdown", (e) => {
    const el = e.target.closest("[data-btn]");
    if (!el) return;
    e.preventDefault();
    controls.setPointerCapture(e.pointerId);
    held.set(e.pointerId, el.dataset.btn);
    press(el.dataset.btn, true);
    if (e.pointerType === "touch" && navigator.vibrate) navigator.vibrate(8);
  });
  controls.addEventListener("pointermove", (e) => {
    const cur = held.get(e.pointerId);
    if (!cur) return;
    const el = document.elementFromPoint(e.clientX, e.clientY);
    const btn = el && el.closest && el.closest(".gb-dpad [data-btn]");
    const next = btn ? btn.dataset.btn : null;
    if (next && next !== cur && ["up", "down", "left", "right"].includes(cur)) {
      press(cur, false);
      press(next, true);
      held.set(e.pointerId, next);
    }
  });
  const up = (e) => { const b = held.get(e.pointerId); if (b) { press(b, false); held.delete(e.pointerId); } };
  controls.addEventListener("pointerup", up);
  controls.addEventListener("pointercancel", up);
  controls.addEventListener("contextmenu", (e) => e.preventDefault());

  // ---- Gamepad (standard mapping) ----------------------------------------
  const PAD = { 1: "a", 0: "b", 9: "start", 8: "select", 12: "up", 13: "down", 14: "left", 15: "right" };
  const padState = {};
  function pollGamepad() {
    const pads = navigator.getGamepads ? navigator.getGamepads() : [];
    const p = pads && Array.from(pads).find(Boolean);
    if (!p) return;
    const want = {};
    for (const i in PAD) if (p.buttons[i] && p.buttons[i].pressed) want[PAD[i]] = true;
    const ax = p.axes[0] || 0, ay = p.axes[1] || 0;
    if (ax < -0.5) want.left = true; if (ax > 0.5) want.right = true;
    if (ay < -0.5) want.up = true; if (ay > 0.5) want.down = true;
    for (const b of ["a", "b", "start", "select", "up", "down", "left", "right"]) {
      const on = !!want[b];
      if (on !== !!padState[b]) { padState[b] = on; press(b, on); }
    }
  }
})();
