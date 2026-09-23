/*
 * Small Game Boy (DMG) emulator core, written for this portfolio to run
 * Tower Hero in the browser. No dependencies.
 *
 * Covers what a normal cartridge needs: LR35902 CPU, PPU (background,
 * window, sprites), timer, joypad, OAM DMA, MBC1 and a 4-channel APU.
 * Not cycle-exact: the CPU runs whole instructions and the PPU renders
 * one scanline at a time.
 *
 * Works in the browser (window.GBCore) and in Node (module.exports).
 */
(function (root) {
  "use strict";

  const FZ = 0x80, FN = 0x40, FH = 0x20, FC = 0x10;
  const CYCLES_PER_FRAME = 70224;
  const CLOCK = 4194304;

  // Base M-cycle counts; conditional branches add their "taken" cost in code.
  const OP_CYCLES = [
    1,3,2,2,1,1,2,1,5,2,2,2,1,1,2,1, 1,3,2,2,1,1,2,1,3,2,2,2,1,1,2,1,
    2,3,2,2,1,1,2,1,2,2,2,2,1,1,2,1, 2,3,2,2,3,3,3,1,2,2,2,2,1,1,2,1,
    1,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1, 1,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1,
    1,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1, 2,2,2,2,2,2,1,2,1,1,1,1,1,1,2,1,
    1,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1, 1,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1,
    1,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1, 1,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1,
    2,3,3,4,3,4,2,4,2,4,3,0,3,6,2,4, 2,3,3,0,3,4,2,4,2,4,3,0,3,0,2,4,
    3,3,2,0,0,4,2,4,4,1,4,0,0,0,2,4, 3,3,2,1,0,4,2,4,3,2,4,1,0,0,2,4,
  ];

  // Joypad bit per button (active low in P1).
  const BUTTONS = { right: 0, left: 1, up: 2, down: 3, a: 4, b: 5, select: 6, start: 7 };

  // Classic green LCD, ABGR for a Uint32 view over ImageData (little endian).
  const SHADES = [0xff0fbc9b, 0xff0fac8b, 0xff306230, 0xff0f380f];

  // ---------------------------------------------------------------- APU --
  const DUTY = [
    [0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 0],
  ];
  const NOISE_DIV = [8, 16, 32, 48, 64, 80, 96, 112];

  class APU {
    constructor(sampleRate) {
      this.sampleRate = sampleRate || 44100;
      this.cyclesPerSample = CLOCK / this.sampleRate;
      this.buffer = new Float32Array(16384);
      this.bufLen = 0;
      this.reset();
    }
    reset() {
      this.on = false;
      this.regs = new Uint8Array(0x30);
      this.wave = new Uint8Array(16);
      this.seqTimer = 8192;
      this.seqStep = 0;
      this.sampleTimer = 0;
      this.capL = 0;
      this.capR = 0;
      this.ch = [0, 1, 2, 3].map(() => ({
        on: false, dac: false, len: 0, lenOn: false, vol: 0, envDir: 0, envPer: 0, envTimer: 0,
        freq: 0, timer: 0, pos: 0, duty: 0,
        sweepPer: 0, sweepDir: 0, sweepShift: 0, sweepTimer: 0, sweepOn: false, shadow: 0,
        lfsr: 0x7fff, width7: false, shift: 0, divisor: 8, volCode: 0,
      }));
    }
    read(addr) {
      const r = addr - 0xff10;
      if (addr >= 0xff30) return this.wave[addr - 0xff30];
      if (addr === 0xff26) {
        let v = (this.on ? 0x80 : 0) | 0x70;
        this.ch.forEach((c, i) => { if (c.on) v |= 1 << i; });
        return v;
      }
      const MASK = [0x80,0x3f,0x00,0xff,0xbf, 0xff,0x3f,0x00,0xff,0xbf, 0x7f,0xff,0x9f,0xff,0xbf,
                    0xff,0xff,0x00,0x00,0xbf, 0x00,0x00];
      return (this.regs[r] | (MASK[r] ?? 0xff)) & 0xff;
    }
    write(addr, v) {
      if (addr >= 0xff30) { this.wave[addr - 0xff30] = v; return; }
      const r = addr - 0xff10;
      if (addr === 0xff26) {
        const was = this.on;
        this.on = !!(v & 0x80);
        if (was && !this.on) { const w = this.wave; this.reset(); this.wave = w; }
        return;
      }
      if (!this.on) return;
      this.regs[r] = v;
      const c = this.ch;
      switch (addr) {
        case 0xff10: c[0].sweepPer = (v >> 4) & 7; c[0].sweepDir = (v >> 3) & 1; c[0].sweepShift = v & 7; break;
        case 0xff11: c[0].duty = v >> 6; c[0].len = 64 - (v & 63); break;
        case 0xff12: this.envReg(c[0], v); break;
        case 0xff13: c[0].freq = (c[0].freq & 0x700) | v; break;
        case 0xff14: c[0].freq = (c[0].freq & 0xff) | ((v & 7) << 8); c[0].lenOn = !!(v & 0x40); if (v & 0x80) this.trigger(0); break;
        case 0xff16: c[1].duty = v >> 6; c[1].len = 64 - (v & 63); break;
        case 0xff17: this.envReg(c[1], v); break;
        case 0xff18: c[1].freq = (c[1].freq & 0x700) | v; break;
        case 0xff19: c[1].freq = (c[1].freq & 0xff) | ((v & 7) << 8); c[1].lenOn = !!(v & 0x40); if (v & 0x80) this.trigger(1); break;
        case 0xff1a: c[2].dac = !!(v & 0x80); if (!c[2].dac) c[2].on = false; break;
        case 0xff1b: c[2].len = 256 - v; break;
        case 0xff1c: c[2].volCode = (v >> 5) & 3; break;
        case 0xff1d: c[2].freq = (c[2].freq & 0x700) | v; break;
        case 0xff1e: c[2].freq = (c[2].freq & 0xff) | ((v & 7) << 8); c[2].lenOn = !!(v & 0x40); if (v & 0x80) this.trigger(2); break;
        case 0xff20: c[3].len = 64 - (v & 63); break;
        case 0xff21: this.envReg(c[3], v); break;
        case 0xff22: c[3].shift = v >> 4; c[3].width7 = !!(v & 8); c[3].divisor = NOISE_DIV[v & 7]; break;
        case 0xff23: c[3].lenOn = !!(v & 0x40); if (v & 0x80) this.trigger(3); break;
      }
    }
    envReg(c, v) {
      c.dac = (v & 0xf8) !== 0;
      if (!c.dac) c.on = false;
    }
    trigger(i) {
      const c = this.ch[i];
      const nrx2 = [0x02, 0x07, 0, 0x11][i];
      if (i !== 2) {
        const v = this.regs[nrx2];
        c.vol = v >> 4; c.envDir = (v >> 3) & 1; c.envPer = v & 7; c.envTimer = c.envPer || 8;
      }
      if (c.len === 0) c.len = i === 2 ? 256 : 64;
      c.on = c.dac;
      if (i < 2) c.timer = (2048 - c.freq) * 4;
      if (i === 2) { c.timer = (2048 - c.freq) * 2; c.pos = 0; }
      if (i === 3) { c.lfsr = 0x7fff; c.timer = c.divisor << c.shift; }
      if (i === 0) {
        c.shadow = c.freq;
        c.sweepTimer = c.sweepPer || 8;
        c.sweepOn = c.sweepPer > 0 || c.sweepShift > 0;
        if (c.sweepShift) this.sweepCalc(c);
      }
    }
    sweepCalc(c) {
      let f = c.shadow >> c.sweepShift;
      f = c.sweepDir ? c.shadow - f : c.shadow + f;
      if (f > 2047) c.on = false;
      return f;
    }
    sequencer() {
      const s = this.seqStep;
      if ((s & 1) === 0) {
        for (const c of this.ch) if (c.lenOn && c.len > 0 && --c.len === 0) c.on = false;
      }
      if (s === 2 || s === 6) {
        const c = this.ch[0];
        if (--c.sweepTimer <= 0) {
          c.sweepTimer = c.sweepPer || 8;
          if (c.sweepOn && c.sweepPer) {
            const f = this.sweepCalc(c);
            if (f <= 2047 && c.sweepShift) { c.shadow = f; c.freq = f; this.sweepCalc(c); }
          }
        }
      }
      if (s === 7) {
        for (const i of [0, 1, 3]) {
          const c = this.ch[i];
          if (!c.envPer) continue;
          if (--c.envTimer <= 0) {
            c.envTimer = c.envPer;
            if (c.envDir && c.vol < 15) c.vol++;
            else if (!c.envDir && c.vol > 0) c.vol--;
          }
        }
      }
      this.seqStep = (s + 1) & 7;
    }
    tick(cycles) {
      if (!this.on) {
        this.sampleTimer += cycles;
        while (this.sampleTimer >= this.cyclesPerSample) { this.sampleTimer -= this.cyclesPerSample; this.push(0, 0); }
        return;
      }
      const c = this.ch;
      this.seqTimer -= cycles;
      while (this.seqTimer <= 0) { this.seqTimer += 8192; this.sequencer(); }
      for (let i = 0; i < 2; i++) {
        const q = c[i];
        q.timer -= cycles;
        while (q.timer <= 0) { q.timer += (2048 - q.freq) * 4; q.pos = (q.pos + 1) & 7; }
      }
      const w = c[2];
      w.timer -= cycles;
      while (w.timer <= 0) { w.timer += (2048 - w.freq) * 2; w.pos = (w.pos + 1) & 31; }
      const n = c[3];
      n.timer -= cycles;
      while (n.timer <= 0) {
        n.timer += Math.max(8, n.divisor << n.shift);
        const bit = (n.lfsr ^ (n.lfsr >> 1)) & 1;
        n.lfsr = (n.lfsr >> 1) | (bit << 14);
        if (n.width7) n.lfsr = (n.lfsr & ~0x40) | (bit << 6);
      }
      this.sampleTimer += cycles;
      while (this.sampleTimer >= this.cyclesPerSample) {
        this.sampleTimer -= this.cyclesPerSample;
        this.mix();
      }
    }
    mix() {
      const c = this.ch;
      const out = [0, 0, 0, 0];
      if (c[0].on && c[0].dac) out[0] = DUTY[c[0].duty][c[0].pos] ? c[0].vol : 0;
      if (c[1].on && c[1].dac) out[1] = DUTY[c[1].duty][c[1].pos] ? c[1].vol : 0;
      if (c[2].on && c[2].dac && c[2].volCode) {
        const b = this.wave[c[2].pos >> 1];
        const s = c[2].pos & 1 ? b & 15 : b >> 4;
        out[2] = s >> (c[2].volCode - 1);
      }
      if (c[3].on && c[3].dac) out[3] = (~c[3].lfsr & 1) ? c[3].vol : 0;
      const pan = this.regs[0x15], vol = this.regs[0x14];
      let l = 0, r = 0;
      for (let i = 0; i < 4; i++) {
        const s = out[i] / 15;
        if (pan & (1 << (i + 4))) l += s;
        if (pan & (1 << i)) r += s;
      }
      l = (l / 2) * (((vol >> 4) & 7) + 1) / 8;
      r = (r / 2) * ((vol & 7) + 1) / 8;
      // High-pass (like the real console's capacitor) to remove the DC offset.
      const ol = l - this.capL, or = r - this.capR;
      this.capL = l - ol * 0.996;
      this.capR = r - or * 0.996;
      this.push(ol, or);
    }
    push(l, r) {
      if (this.bufLen + 2 > this.buffer.length) return;
      this.buffer[this.bufLen++] = l;
      this.buffer[this.bufLen++] = r;
    }
    take() {
      const out = this.buffer.slice(0, this.bufLen);
      this.bufLen = 0;
      return out;
    }
  }

  // ----------------------------------------------------------------- GB --
  class GB {
    constructor(rom, opts = {}) {
      this.rom = rom instanceof Uint8Array ? rom : new Uint8Array(rom);
      this.apu = new APU(opts.sampleRate);
      this.frame = new Uint32Array(160 * 144);
      this.reset();
    }

    reset() {
      const rom = this.rom;
      this.cartType = rom[0x147];
      this.romBanks = Math.max(2, 2 << rom[0x148]);
      this.ramSize = [0, 0x800, 0x2000, 0x8000, 0x20000, 0x10000][rom[0x149]] || 0;
      this.eram = new Uint8Array(Math.max(this.ramSize, 0x2000));
      this.vram = new Uint8Array(0x2000);
      this.wram = new Uint8Array(0x2000);
      this.oam = new Uint8Array(0xa0);
      this.hram = new Uint8Array(0x7f);
      this.io = new Uint8Array(0x80);
      this.ie = 0;
      this.romBank = 1; this.ramBank = 0; this.ramOn = false; this.mbcMode = 0;

      // Post-boot DMG state
      this.a = 0x01; this.f = 0xb0; this.b = 0x00; this.c = 0x13;
      this.d = 0x00; this.e = 0xd8; this.h = 0x01; this.l = 0x4d;
      this.sp = 0xfffe; this.pc = 0x100;
      this.ime = false; this.imeNext = false; this.halted = false;

      this.divCounter = 0xabcc; this.timaCounter = 0;
      this.lineCycles = 0; this.winLine = 0; this.statLine = false;
      this.joy = 0xff;

      const io = this.io;
      io[0x00] = 0xcf; io[0x05] = 0; io[0x06] = 0; io[0x07] = 0xf8; io[0x0f] = 0xe1;
      io[0x40] = 0x91; io[0x41] = 0x85; io[0x42] = 0; io[0x43] = 0; io[0x44] = 0; io[0x45] = 0;
      io[0x47] = 0xfc; io[0x48] = 0xff; io[0x49] = 0xff; io[0x4a] = 0; io[0x4b] = 0;
      this.apu.reset();
      this.apu.write(0xff26, 0xf1);
      this.apu.write(0xff24, 0x77);
      this.apu.write(0xff25, 0xf3);
      this.frame.fill(SHADES[0]);
    }

    // ---------------------------------------------------------- memory --
    read(addr) {
      addr &= 0xffff;
      if (addr < 0x4000) {
        if (this.mbcMode && this.cartType >= 1 && this.cartType <= 3) {
          const bank = ((this.ramBank << 5) % this.romBanks);
          return this.rom[bank * 0x4000 + addr] ?? 0xff;
        }
        return this.rom[addr] ?? 0xff;
      }
      if (addr < 0x8000) {
        let bank = this.romBank;
        if (this.cartType >= 1 && this.cartType <= 3) bank = (bank | (this.ramBank << 5));
        bank %= this.romBanks;
        return this.rom[bank * 0x4000 + (addr - 0x4000)] ?? 0xff;
      }
      if (addr < 0xa000) return this.vram[addr - 0x8000];
      if (addr < 0xc000) {
        if (!this.ramOn || !this.ramSize) return 0xff;
        const bank = this.mbcMode ? this.ramBank : 0;
        return this.eram[(bank * 0x2000 + addr - 0xa000) % this.eram.length];
      }
      if (addr < 0xe000) return this.wram[addr - 0xc000];
      if (addr < 0xfe00) return this.wram[addr - 0xe000];
      if (addr < 0xfea0) return this.oam[addr - 0xfe00];
      if (addr < 0xff00) return 0xff;
      if (addr < 0xff80) return this.readIO(addr);
      if (addr < 0xffff) return this.hram[addr - 0xff80];
      return this.ie;
    }

    write(addr, v) {
      addr &= 0xffff; v &= 0xff;
      if (addr < 0x8000) {
        if (addr < 0x2000) this.ramOn = (v & 0x0f) === 0x0a;
        else if (addr < 0x4000) { this.romBank = v & 0x1f; if (!this.romBank) this.romBank = 1; }
        else if (addr < 0x6000) this.ramBank = v & 3;
        else this.mbcMode = v & 1;
        return;
      }
      if (addr < 0xa000) { this.vram[addr - 0x8000] = v; return; }
      if (addr < 0xc000) {
        if (!this.ramOn || !this.ramSize) return;
        const bank = this.mbcMode ? this.ramBank : 0;
        this.eram[(bank * 0x2000 + addr - 0xa000) % this.eram.length] = v;
        this.ramDirty = true;
        return;
      }
      if (addr < 0xe000) { this.wram[addr - 0xc000] = v; return; }
      if (addr < 0xfe00) { this.wram[addr - 0xe000] = v; return; }
      if (addr < 0xfea0) { this.oam[addr - 0xfe00] = v; return; }
      if (addr < 0xff00) return;
      if (addr < 0xff80) { this.writeIO(addr, v); return; }
      if (addr < 0xffff) { this.hram[addr - 0xff80] = v; return; }
      this.ie = v;
    }

    readIO(addr) {
      const r = addr & 0x7f;
      switch (r) {
        case 0x00: {
          const sel = this.io[0];
          let low = 0x0f;
          if (!(sel & 0x10)) low &= this.joy & 0x0f;
          if (!(sel & 0x20)) low &= (this.joy >> 4) & 0x0f;
          return 0xc0 | (sel & 0x30) | low;
        }
        case 0x04: return (this.divCounter >> 8) & 0xff;
        case 0x07: return this.io[7] | 0xf8;
        case 0x0f: return this.io[0x0f] | 0xe0;
        case 0x41: return this.io[0x41] | 0x80;
      }
      if (r >= 0x10 && r < 0x40) return this.apu.read(addr);
      return this.io[r];
    }

    writeIO(addr, v) {
      const r = addr & 0x7f;
      switch (r) {
        case 0x00: this.io[0] = v & 0x30; return;
        case 0x04: this.divCounter = 0; return;
        case 0x0f: this.io[0x0f] = v & 0x1f; return;
        case 0x40: {
          const wasOn = this.io[0x40] & 0x80;
          this.io[0x40] = v;
          if (wasOn && !(v & 0x80)) { this.io[0x44] = 0; this.lineCycles = 0; this.io[0x41] &= 0xfc; }
          if (!wasOn && (v & 0x80)) { this.lineCycles = 0; this.winLine = 0; this.checkLyc(); }
          return;
        }
        case 0x41: this.io[0x41] = (this.io[0x41] & 0x07) | (v & 0x78); return;
        case 0x44: return;
        case 0x45: this.io[0x45] = v; this.checkLyc(); return;
        case 0x46: {
          const src = v << 8;
          for (let i = 0; i < 0xa0; i++) this.oam[i] = this.read(src + i);
          this.io[0x46] = v;
          return;
        }
      }
      if (r >= 0x10 && r < 0x40) { this.apu.write(addr, v); return; }
      this.io[r] = v;
    }

    // ------------------------------------------------------------ input --
    setButton(name, down) {
      const bit = BUTTONS[name];
      if (bit === undefined) return;
      const before = this.joy;
      if (down) this.joy &= ~(1 << bit); else this.joy |= 1 << bit;
      if (before !== this.joy && down) this.io[0x0f] |= 0x10;
    }

    // --------------------------------------------------------------- run --
    runFrame() {
      let done = 0;
      while (done < CYCLES_PER_FRAME) {
        const c = this.step();
        this.tickTimer(c);
        this.tickPPU(c);
        this.apu.tick(c);
        done += c;
      }
    }

    step() {
      const pending = this.ie & this.io[0x0f] & 0x1f;
      if (pending) {
        if (this.halted) this.halted = false;
        if (this.ime) {
          this.ime = false;
          const i = 31 - Math.clz32(pending & -pending);
          this.io[0x0f] &= ~(1 << i);
          this.push16(this.pc);
          this.pc = 0x40 + i * 8;
          return 20;
        }
      }
      if (this.halted) return 4;
      if (this.imeNext) { this.imeNext = false; this.ime = true; }
      const op = this.read(this.pc);
      this.pc = (this.pc + 1) & 0xffff;
      return this.exec(op) * 4;
    }

    tickTimer(c) {
      const old = this.divCounter;
      this.divCounter = (this.divCounter + c) & 0xffff;
      const tac = this.io[7];
      if (!(tac & 4)) return;
      const bit = [9, 3, 5, 7][tac & 3];
      // Count falling edges of the selected DIV bit over this span.
      const period = 1 << (bit + 1);
      const edges = Math.floor((old + c) / period) - Math.floor(old / period);
      for (let i = 0; i < edges; i++) {
        if (this.io[5] === 0xff) { this.io[5] = this.io[6]; this.io[0x0f] |= 0x04; }
        else this.io[5]++;
      }
    }

    // -------------------------------------------------------------- PPU --
    setMode(m) {
      this.io[0x41] = (this.io[0x41] & 0xfc) | m;
      this.updateStat();
    }
    checkLyc() {
      if (this.io[0x44] === this.io[0x45]) this.io[0x41] |= 4; else this.io[0x41] &= ~4;
      this.updateStat();
    }
    updateStat() {
      const s = this.io[0x41], mode = s & 3;
      const line = !!(((s & 0x40) && (s & 4)) || ((s & 0x20) && mode === 2) ||
        ((s & 0x10) && mode === 1) || ((s & 0x08) && mode === 0));
      if (line && !this.statLine) this.io[0x0f] |= 0x02;
      this.statLine = line;
    }

    tickPPU(c) {
      if (!(this.io[0x40] & 0x80)) return;
      this.lineCycles += c;
      const ly = this.io[0x44];
      const mode = this.io[0x41] & 3;
      if (ly < 144) {
        if (mode === 2 && this.lineCycles >= 80) this.setMode(3);
        else if (mode === 3 && this.lineCycles >= 252) { this.renderLine(ly); this.setMode(0); }
      }
      if (this.lineCycles >= 456) {
        this.lineCycles -= 456;
        const next = (ly + 1) % 154;
        this.io[0x44] = next;
        if (next === 144) { this.setMode(1); this.io[0x0f] |= 0x01; this.frameReady = true; }
        else if (next < 144) { if (next === 0) this.winLine = 0; this.setMode(2); }
        this.checkLyc();
      }
    }

    renderLine(ly) {
      const lcdc = this.io[0x40], vram = this.vram;
      const out = this.frame, base = ly * 160;
      const bgIdx = this.lineIdx || (this.lineIdx = new Uint8Array(160));
      const bgp = this.io[0x47];
      bgIdx.fill(0);

      if (lcdc & 1) {
        const scy = this.io[0x42], scx = this.io[0x43];
        const map = lcdc & 8 ? 0x1c00 : 0x1800;
        const signed = !(lcdc & 0x10);
        const y = (ly + scy) & 0xff;
        const wy = this.io[0x4a], wx = this.io[0x4b] - 7;
        const winOn = (lcdc & 0x20) && ly >= wy && this.io[0x4b] <= 166;
        const wmap = lcdc & 0x40 ? 0x1c00 : 0x1800;
        for (let x = 0; x < 160; x++) {
          let tileMap, px, py;
          if (winOn && x >= wx) { tileMap = wmap; px = x - wx; py = this.winLine; }
          else { tileMap = map; px = (x + scx) & 0xff; py = y; }
          let tile = vram[tileMap + ((py >> 3) << 5) + (px >> 3)];
          let addr = signed ? 0x1000 + ((tile << 24) >> 24) * 16 : tile * 16;
          addr += (py & 7) * 2;
          const bit = 7 - (px & 7);
          const idx = ((vram[addr] >> bit) & 1) | (((vram[addr + 1] >> bit) & 1) << 1);
          bgIdx[x] = idx;
          out[base + x] = SHADES[(bgp >> (idx * 2)) & 3];
        }
        if (winOn && wx < 160) this.winLine++;
      } else {
        for (let x = 0; x < 160; x++) out[base + x] = SHADES[bgp & 3];
      }

      if (lcdc & 2) {
        const tall = lcdc & 4, h = tall ? 16 : 8;
        const found = [];
        for (let i = 0; i < 40 && found.length < 10; i++) {
          const sy = this.oam[i * 4] - 16;
          if (ly >= sy && ly < sy + h) found.push(i);
        }
        // Draw lowest priority first: larger X, then higher OAM index.
        found.sort((a, b) => (this.oam[b * 4 + 1] - this.oam[a * 4 + 1]) || (b - a));
        for (const i of found) {
          const o = i * 4;
          const sy = this.oam[o] - 16, sx = this.oam[o + 1] - 8, attr = this.oam[o + 3];
          let tile = this.oam[o + 2];
          let row = ly - sy;
          if (attr & 0x40) row = h - 1 - row;
          if (tall) tile &= 0xfe;
          const addr = tile * 16 + row * 2;
          const pal = this.io[attr & 0x10 ? 0x49 : 0x48];
          for (let p = 0; p < 8; p++) {
            const x = sx + p;
            if (x < 0 || x >= 160) continue;
            const bit = attr & 0x20 ? p : 7 - p;
            const idx = ((vram[addr] >> bit) & 1) | (((vram[addr + 1] >> bit) & 1) << 1);
            if (!idx) continue;
            if ((attr & 0x80) && bgIdx[x]) continue;
            out[base + x] = SHADES[(pal >> (idx * 2)) & 3];
          }
        }
      }
    }

    // -------------------------------------------------------------- CPU --
    get af() { return (this.a << 8) | this.f; }
    get bc() { return (this.b << 8) | this.c; }
    get de() { return (this.d << 8) | this.e; }
    get hl() { return (this.h << 8) | this.l; }
    set bc(v) { this.b = (v >> 8) & 0xff; this.c = v & 0xff; }
    set de(v) { this.d = (v >> 8) & 0xff; this.e = v & 0xff; }
    set hl(v) { this.h = (v >> 8) & 0xff; this.l = v & 0xff; }
    set af(v) { this.a = (v >> 8) & 0xff; this.f = v & 0xf0; }

    imm8() { const v = this.read(this.pc); this.pc = (this.pc + 1) & 0xffff; return v; }
    imm16() { const lo = this.imm8(); return lo | (this.imm8() << 8); }
    push16(v) { this.sp = (this.sp - 1) & 0xffff; this.write(this.sp, v >> 8); this.sp = (this.sp - 1) & 0xffff; this.write(this.sp, v & 0xff); }
    pop16() { const lo = this.read(this.sp); this.sp = (this.sp + 1) & 0xffff; const hi = this.read(this.sp); this.sp = (this.sp + 1) & 0xffff; return lo | (hi << 8); }

    getR(i) {
      switch (i) {
        case 0: return this.b; case 1: return this.c; case 2: return this.d; case 3: return this.e;
        case 4: return this.h; case 5: return this.l; case 6: return this.read(this.hl); default: return this.a;
      }
    }
    setR(i, v) {
      v &= 0xff;
      switch (i) {
        case 0: this.b = v; break; case 1: this.c = v; break; case 2: this.d = v; break; case 3: this.e = v; break;
        case 4: this.h = v; break; case 5: this.l = v; break; case 6: this.write(this.hl, v); break; default: this.a = v;
      }
    }

    alu(op, v) {
      const a = this.a;
      let r, f = 0;
      switch (op) {
        case 0: r = a + v; f = ((a & 15) + (v & 15) > 15 ? FH : 0) | (r > 255 ? FC : 0); break;
        case 1: { const cy = this.f & FC ? 1 : 0; r = a + v + cy; f = ((a & 15) + (v & 15) + cy > 15 ? FH : 0) | (r > 255 ? FC : 0); break; }
        case 2: case 7: r = a - v; f = FN | ((a & 15) < (v & 15) ? FH : 0) | (r < 0 ? FC : 0); break;
        case 3: { const cy = this.f & FC ? 1 : 0; r = a - v - cy; f = FN | ((a & 15) - (v & 15) - cy < 0 ? FH : 0) | (r < 0 ? FC : 0); break; }
        case 4: r = a & v; f = FH; break;
        case 5: r = a ^ v; break;
        case 6: r = a | v; break;
      }
      r &= 0xff;
      if (!r) f |= FZ;
      this.f = f;
      if (op !== 7) this.a = r;
    }

    inc8(v) { const r = (v + 1) & 0xff; this.f = (this.f & FC) | (r ? 0 : FZ) | ((v & 15) === 15 ? FH : 0); return r; }
    dec8(v) { const r = (v - 1) & 0xff; this.f = (this.f & FC) | FN | (r ? 0 : FZ) | ((v & 15) === 0 ? FH : 0); return r; }
    addHL(v) {
      const hl = this.hl, r = hl + v;
      this.f = (this.f & FZ) | ((hl & 0xfff) + (v & 0xfff) > 0xfff ? FH : 0) | (r > 0xffff ? FC : 0);
      this.hl = r & 0xffff;
    }
    spOff() {
      const n = (this.imm8() << 24) >> 24, sp = this.sp;
      this.f = ((sp & 15) + (n & 15) > 15 ? FH : 0) | ((sp & 0xff) + (n & 0xff) > 0xff ? FC : 0);
      return (sp + n) & 0xffff;
    }
    cond(i) {
      switch (i) { case 0: return !(this.f & FZ); case 1: return !!(this.f & FZ); case 2: return !(this.f & FC); default: return !!(this.f & FC); }
    }

    exec(op) {
      let cyc = OP_CYCLES[op];
      if (op >= 0x40 && op < 0x80) {
        if (op === 0x76) { this.halted = true; return 1; }
        this.setR((op >> 3) & 7, this.getR(op & 7));
        return cyc;
      }
      if (op >= 0x80 && op < 0xc0) { this.alu((op >> 3) & 7, this.getR(op & 7)); return cyc; }

      switch (op) {
        case 0x00: break;
        case 0x01: this.bc = this.imm16(); break;
        case 0x11: this.de = this.imm16(); break;
        case 0x21: this.hl = this.imm16(); break;
        case 0x31: this.sp = this.imm16(); break;
        case 0x02: this.write(this.bc, this.a); break;
        case 0x12: this.write(this.de, this.a); break;
        case 0x22: { const hl = this.hl; this.write(hl, this.a); this.hl = (hl + 1) & 0xffff; break; }
        case 0x32: { const hl = this.hl; this.write(hl, this.a); this.hl = (hl - 1) & 0xffff; break; }
        case 0x0a: this.a = this.read(this.bc); break;
        case 0x1a: this.a = this.read(this.de); break;
        case 0x2a: { const hl = this.hl; this.a = this.read(hl); this.hl = (hl + 1) & 0xffff; break; }
        case 0x3a: { const hl = this.hl; this.a = this.read(hl); this.hl = (hl - 1) & 0xffff; break; }
        case 0x03: this.bc = (this.bc + 1) & 0xffff; break;
        case 0x13: this.de = (this.de + 1) & 0xffff; break;
        case 0x23: this.hl = (this.hl + 1) & 0xffff; break;
        case 0x33: this.sp = (this.sp + 1) & 0xffff; break;
        case 0x0b: this.bc = (this.bc - 1) & 0xffff; break;
        case 0x1b: this.de = (this.de - 1) & 0xffff; break;
        case 0x2b: this.hl = (this.hl - 1) & 0xffff; break;
        case 0x3b: this.sp = (this.sp - 1) & 0xffff; break;
        case 0x04: case 0x0c: case 0x14: case 0x1c: case 0x24: case 0x2c: case 0x34: case 0x3c: {
          const r = (op >> 3) & 7; this.setR(r, this.inc8(this.getR(r))); break;
        }
        case 0x05: case 0x0d: case 0x15: case 0x1d: case 0x25: case 0x2d: case 0x35: case 0x3d: {
          const r = (op >> 3) & 7; this.setR(r, this.dec8(this.getR(r))); break;
        }
        case 0x06: case 0x0e: case 0x16: case 0x1e: case 0x26: case 0x2e: case 0x36: case 0x3e:
          this.setR((op >> 3) & 7, this.imm8()); break;
        case 0x07: { const a = this.a, c = a >> 7; this.a = ((a << 1) | c) & 0xff; this.f = c ? FC : 0; break; }
        case 0x0f: { const a = this.a, c = a & 1; this.a = (a >> 1) | (c << 7); this.f = c ? FC : 0; break; }
        case 0x17: { const a = this.a, c = a >> 7; this.a = ((a << 1) | (this.f & FC ? 1 : 0)) & 0xff; this.f = c ? FC : 0; break; }
        case 0x1f: { const a = this.a, c = a & 1; this.a = (a >> 1) | (this.f & FC ? 0x80 : 0); this.f = c ? FC : 0; break; }
        case 0x08: { const addr = this.imm16(); this.write(addr, this.sp & 0xff); this.write(addr + 1, this.sp >> 8); break; }
        case 0x09: this.addHL(this.bc); break;
        case 0x19: this.addHL(this.de); break;
        case 0x29: this.addHL(this.hl); break;
        case 0x39: this.addHL(this.sp); break;
        case 0x10: this.imm8(); break; // STOP
        case 0x18: { const n = (this.imm8() << 24) >> 24; this.pc = (this.pc + n) & 0xffff; break; }
        case 0x20: case 0x28: case 0x30: case 0x38: {
          const n = (this.imm8() << 24) >> 24;
          if (this.cond((op >> 3) & 3)) { this.pc = (this.pc + n) & 0xffff; cyc += 1; }
          break;
        }
        case 0x27: {
          let a = this.a, adj = 0, c = false;
          const f = this.f;
          if ((f & FH) || (!(f & FN) && (a & 15) > 9)) adj |= 0x06;
          if ((f & FC) || (!(f & FN) && a > 0x99)) { adj |= 0x60; c = true; }
          a = f & FN ? a - adj : a + adj;
          a &= 0xff;
          this.a = a;
          this.f = (f & FN) | (a ? 0 : FZ) | (c ? FC : 0);
          break;
        }
        case 0x2f: this.a ^= 0xff; this.f |= FN | FH; break;
        case 0x37: this.f = (this.f & FZ) | FC; break;
        case 0x3f: this.f = (this.f & FZ) | (this.f & FC ? 0 : FC); break;

        case 0xc0: case 0xc8: case 0xd0: case 0xd8:
          if (this.cond((op >> 3) & 3)) { this.pc = this.pop16(); cyc += 3; }
          break;
        case 0xc9: this.pc = this.pop16(); break;
        case 0xd9: this.pc = this.pop16(); this.ime = true; break;
        case 0xc2: case 0xca: case 0xd2: case 0xda: {
          const a = this.imm16(); if (this.cond((op >> 3) & 3)) { this.pc = a; cyc += 1; } break;
        }
        case 0xc3: this.pc = this.imm16(); break;
        case 0xe9: this.pc = this.hl; break;
        case 0xc4: case 0xcc: case 0xd4: case 0xdc: {
          const a = this.imm16(); if (this.cond((op >> 3) & 3)) { this.push16(this.pc); this.pc = a; cyc += 3; } break;
        }
        case 0xcd: { const a = this.imm16(); this.push16(this.pc); this.pc = a; break; }
        case 0xc7: case 0xcf: case 0xd7: case 0xdf: case 0xe7: case 0xef: case 0xf7: case 0xff:
          this.push16(this.pc); this.pc = op & 0x38; break;
        case 0xc1: this.bc = this.pop16(); break;
        case 0xd1: this.de = this.pop16(); break;
        case 0xe1: this.hl = this.pop16(); break;
        case 0xf1: this.af = this.pop16(); break;
        case 0xc5: this.push16(this.bc); break;
        case 0xd5: this.push16(this.de); break;
        case 0xe5: this.push16(this.hl); break;
        case 0xf5: this.push16(this.af); break;
        case 0xc6: case 0xce: case 0xd6: case 0xde: case 0xe6: case 0xee: case 0xf6: case 0xfe:
          this.alu((op >> 3) & 7, this.imm8()); break;
        case 0xe0: this.write(0xff00 + this.imm8(), this.a); break;
        case 0xf0: this.a = this.read(0xff00 + this.imm8()); break;
        case 0xe2: this.write(0xff00 + this.c, this.a); break;
        case 0xf2: this.a = this.read(0xff00 + this.c); break;
        case 0xea: this.write(this.imm16(), this.a); break;
        case 0xfa: this.a = this.read(this.imm16()); break;
        case 0xe8: this.sp = this.spOff(); break;
        case 0xf8: this.hl = this.spOff(); break;
        case 0xf9: this.sp = this.hl; break;
        case 0xf3: this.ime = false; this.imeNext = false; break;
        case 0xfb: this.imeNext = true; break;
        case 0xcb: return this.execCB(this.imm8());
        default: /* illegal opcode: behave like NOP */ cyc = 1;
      }
      return cyc;
    }

    execCB(op) {
      const r = op & 7, n = (op >> 3) & 7;
      let v = this.getR(r);
      const hl = r === 6;
      if (op < 0x40) {
        let c = 0;
        switch (n) {
          case 0: c = v >> 7; v = ((v << 1) | c) & 0xff; break;
          case 1: c = v & 1; v = (v >> 1) | (c << 7); break;
          case 2: c = v >> 7; v = ((v << 1) | (this.f & FC ? 1 : 0)) & 0xff; break;
          case 3: c = v & 1; v = (v >> 1) | (this.f & FC ? 0x80 : 0); break;
          case 4: c = v >> 7; v = (v << 1) & 0xff; break;
          case 5: c = v & 1; v = (v >> 1) | (v & 0x80); break;
          case 6: v = ((v & 15) << 4) | (v >> 4); break;
          case 7: c = v & 1; v >>= 1; break;
        }
        this.f = (v ? 0 : FZ) | (c ? FC : 0);
        this.setR(r, v);
        return hl ? 4 : 2;
      }
      if (op < 0x80) {
        this.f = (this.f & FC) | FH | (v & (1 << n) ? 0 : FZ);
        return hl ? 3 : 2;
      }
      if (op < 0xc0) this.setR(r, v & ~(1 << n));
      else this.setR(r, v | (1 << n));
      return hl ? 4 : 2;
    }

    // Battery RAM for saves
    saveData() { return this.ramSize ? this.eram.slice(0, this.ramSize) : null; }
    loadData(d) { if (d && this.ramSize) this.eram.set(d.subarray(0, this.ramSize)); }
  }

  const api = { GB, CYCLES_PER_FRAME, CLOCK, FPS: CLOCK / CYCLES_PER_FRAME };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.GBCore = api;
})(typeof window !== "undefined" ? window : globalThis);
