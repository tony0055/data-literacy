/* 2D 마인크래프트 - 웹 싱글파일 의존성 없음. Canvas + 바닐라 JS. */
(() => {
  "use strict";

  const TILE = 32;
  const WORLD_W = 160;
  const WORLD_H = 72;
  const SAVE_KEY = "mc2d-save-v1";
  const REACH_TILES = 6;
  const DAY_SECONDS = 480;
  const GRAVITY = 2600;
  const MOVE_SPEED = 250;
  const JUMP_VEL = 860;

  const AIR = 0;
  const GRASS = 1;
  const DIRT = 2;
  const STONE = 3;
  const LOG = 4;
  const LEAVES = 5;
  const SAND = 6;
  const COAL = 7;
  const IRON = 8;
  const DIAMOND = 9;
  const BEDROCK = 10;
  const PLANKS = 11;

  const BLOCKS = {
    [AIR]: { name: "공기", color: "#00000000", solid: false, breakable: false },
    [GRASS]: { name: "잔디", color: "#5fae3f", solid: true, breakable: true },
    [DIRT]: { name: "흙", color: "#8a5a33", solid: true, breakable: true },
    [STONE]: { name: "돌", color: "#8d8f99", solid: true, breakable: true },
    [LOG]: { name: "통나무", color: "#6b4a26", solid: true, breakable: true },
    [LEAVES]: { name: "잎", color: "#2f8f3a", solid: true, breakable: true },
    [SAND]: { name: "모래", color: "#e0cf9a", solid: true, breakable: true },
    [COAL]: { name: "석탄광석", color: "#4a4d55", solid: true, breakable: true },
    [IRON]: { name: "철광석", color: "#d8a17a", solid: true, breakable: true },
    [DIAMOND]: { name: "다이아", color: "#5fe3e0", solid: true, breakable: true },
    [BEDROCK]: { name: "기반암", color: "#1c1e24", solid: true, breakable: false },
    [PLANKS]: { name: "판자", color: "#c49a5c", solid: true, breakable: true },
  };

  const HOTBAR = [GRASS, DIRT, STONE, LOG, PLANKS, LEAVES, SAND, COAL];

  const canvas = document.getElementById("game");
  const ctx = canvas.getContext("2d");
  ctx.imageSmoothingEnabled = false;

  const elFps = document.getElementById("stat-fps");
  const elPos = document.getElementById("stat-pos");
  const elTime = document.getElementById("stat-time");
  const elSeed = document.getElementById("stat-seed");
  const elHotbar = document.getElementById("hotbar");
  const elToast = document.getElementById("toast");
  const elHelp = document.getElementById("help");

  let toastTimer = 0;
  function toast(msg) {
    elToast.textContent = msg;
    elToast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => elToast.classList.remove("show"), 1800);
  }

  function mulberry32(seed) {
    let a = seed >>> 0;
    return function () {
      a |= 0;
      a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function hash2(x, y, seed) {
    let h = (x * 374761393 + y * 668265263 + seed * 1442695041) | 0;
    h = Math.imul(h ^ (h >>> 13), 1274126177);
    return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
  }

  const world = {
    seed: 20260201,
    data: new Uint8Array(WORLD_W * WORLD_H),
    surface: new Int16Array(WORLD_W),
  };

  function idx(tx, ty) {
    return ty * WORLD_W + tx;
  }
  function inBounds(tx, ty) {
    return tx >= 0 && ty >= 0 && tx < WORLD_W && ty < WORLD_H;
  }
  function getTile(tx, ty) {
    if (tx < 0 || tx >= WORLD_W) return BEDROCK;
    if (ty < 0) return AIR;
    if (ty >= WORLD_H) return BEDROCK;
    return world.data[idx(tx, ty)];
  }
  function setTile(tx, ty, v) {
    if (!inBounds(tx, ty)) return;
    world.data[idx(tx, ty)] = v;
  }
  function isSolid(tx, ty) {
    const b = getTile(tx, ty);
    return !!BLOCKS[b] && BLOCKS[b].solid;
  }

  function genWorld(seed) {
    world.seed = seed >>> 0;
    world.data.fill(AIR);
    const rand = mulberry32(world.seed);
    const base = Math.floor(WORLD_H * 0.38);
    for (let x = 0; x < WORLD_W; x++) {
      const hill =
        Math.sin((x / WORLD_W) * Math.PI * 4 + world.seed % 7) * 4 +
        Math.sin((x / WORLD_W) * Math.PI * 11) * 2 +
        (hash2(x, 7, world.seed) - 0.5) * 4;
      const s = Math.max(6, Math.min(WORLD_H - 12, Math.round(base + hill)));
      world.surface[x] = s;
      for (let y = s; y < WORLD_H; y++) {
        const depth = y - s;
        let b = STONE;
        if (y === s) b = GRASS;
        else if (depth <= 3) b = DIRT;
        if (y >= WORLD_H - 1) b = BEDROCK;
        else if (y >= WORLD_H - 3 && rand() < 0.3) b = BEDROCK;
        else if (depth > 4) {
          const r = rand();
          const deep = y / WORLD_H;
          if (deep > 0.82 && r < 0.03) b = DIAMOND;
          else if (deep > 0.6 && r < 0.09) b = IRON;
          else if (r < 0.16) b = COAL;
        }
        // 해변 모래
        if (depth <= 4 && s > base + 2 && rand() < 0.6) b = depth === 0 ? GRASS : SAND;
        if (depth <= 3 && s < base - 3 && rand() < 0.5) b = SAND;
        world.data[idx(x, y)] = b;
      }
    }
    // 동굴: 랜덤 워크 6개
    for (let c = 0; c < 7; c++) {
      let cx = Math.floor(rand() * WORLD_W);
      let cy = Math.floor(WORLD_H * 0.5 + rand() * WORLD_H * 0.35);
      for (let s = 0; s < 90; s++) {
        for (let dx = -1; dx <= 1; dx++) {
          for (let dy = -1; dy <= 1; dy++) {
            const tx = cx + dx;
            const ty = cy + dy;
            if (inBounds(tx, ty) && getTile(tx, ty) !== BEDROCK && ty > world.surface[tx] + 3) {
              setTile(tx, ty, AIR);
            }
          }
        }
        cx += Math.floor(rand() * 3) - 1;
        cy += Math.floor(rand() * 3) - 1;
        cx = Math.max(1, Math.min(WORLD_W - 2, cx));
        cy = Math.max(8, Math.min(WORLD_H - 4, cy));
      }
    }
    // 나무
    for (let x = 3; x < WORLD_W - 3; x++) {
      if (rand() < 0.12) {
        const s = world.surface[x];
        if (getTile(x, s) !== GRASS) continue;
        let clear = true;
        for (let dx = -2; dx <= 2; dx++) {
          if (getTile(x + dx, s - 1) !== AIR) { clear = false; break; }
        }
        if (!clear) continue;
        const trunk = 4 + Math.floor(rand() * 2);
        for (let i = 1; i <= trunk; i++) setTile(x, s - i, LOG);
        const top = s - trunk;
        for (let dx = -2; dx <= 2; dx++) {
          for (let dy = -2; dy <= 1; dy++) {
            if (Math.abs(dx) === 2 && dy === -2) continue;
            if (dx === 0 && dy >= -1) continue;
            const tx = x + dx;
            const ty = top + dy;
            if (inBounds(tx, ty) && getTile(tx, ty) === AIR) setTile(tx, ty, LEAVES);
          }
        }
        x += 3;
      }
    }
  }

  const player = {
    x: 0, y: 0, vx: 0, vy: 0,
    w: 22, h: 52,
    onGround: false,
  };

  const inventory = new Map();
  let selected = 0;
  let timeOfDay = 0.3;
  let spawn = { x: 0, y: 0 };

  function addItem(block, n = 1) {
    inventory.set(block, (inventory.get(block) || 0) + n);
  }
  function countOf(block) {
    return inventory.get(block) || 0;
  }
  function takeItem(block, n = 1) {
    const c = countOf(block);
    if (c < n) return false;
    inventory.set(block, c - n);
    return true;
  }
  function starterKit() {
    inventory.clear();
    addItem(DIRT, 32);
    addItem(STONE, 16);
    addItem(PLANKS, 16);
    addItem(LOG, 8);
    addItem(SAND, 8);
  }

  function findSpawn() {
    const cx = Math.floor(WORLD_W / 2);
    for (let r = 0; r < WORLD_W / 2; r++) {
      for (const x of [cx + r, cx - r]) {
        if (x < 1 || x >= WORLD_W - 1) continue;
        const s = world.surface[x];
        const px = x * TILE + (TILE - player.w) / 2;
        const py = s * TILE - player.h - 2;
        if (!collides(px, py, player.w, player.h)) {
          return { x: px, y: py };
        }
      }
    }
    return { x: cx * TILE, y: 40 };
  }

  function collides(px, py, w, h) {
    const x0 = Math.floor(px / TILE);
    const y0 = Math.floor(py / TILE);
    const x1 = Math.floor((px + w - 1) / TILE);
    const y1 = Math.floor((py + h - 1) / TILE);
    for (let ty = y0; ty <= y1; ty++) {
      for (let tx = x0; tx <= x1; tx++) {
        if (isSolid(tx, ty)) return true;
      }
    }
    return false;
  }

  function moveAndCollide(dt) {
    // X축
    let nx = player.x + player.vx * dt;
    if (collides(nx, player.y, player.w, player.h)) {
      const step = player.vx > 0 ? -1 : 1;
      while (!collides(nx + step, player.y, player.w, player.h) && Math.abs(nx - player.x) > 1) nx += step;
      // 한 픽셀씩 보정
      while (collides(nx, player.y, player.w, player.h)) nx += step;
      player.vx = 0;
    }
    player.x = Math.max(0, Math.min(WORLD_W * TILE - player.w, nx));
    // Y축
    let ny = player.y + player.vy * dt;
    player.onGround = false;
    if (collides(player.x, ny, player.w, player.h)) {
      if (player.vy > 0) player.onGround = true;
      const step = player.vy > 0 ? -1 : 1;
      while (collides(player.x, ny, player.w, player.h)) ny += step;
      player.vy = 0;
    }
    player.y = Math.max(-200, ny);
    if (player.y > WORLD_H * TILE) {
      respawn();
    }
  }

  function respawn() {
    player.x = spawn.x;
    player.y = spawn.y;
    player.vx = 0;
    player.vy = 0;
    toast("리스폰했습니다");
  }

  const keys = new Set();
  const touchState = { left: false, right: false, jump: false };
  let mouseTile = null;
  let mouseDownLeft = false;
  let mouseDownRight = false;
  let breakProgress = null;

  function selectedBlock() {
    return HOTBAR[selected];
  }

  function worldFromScreen(sx, sy) {
    const rect = canvas.getBoundingClientRect();
    const cx = (sx - rect.left) * (canvas.width / rect.width);
    const cy = (sy - rect.top) * (canvas.height / rect.height);
    return { x: cx + camera.x, y: cy + camera.y };
  }

  function canReach(tx, ty) {
    const pcx = player.x + player.w / 2;
    const pcy = player.y + player.h / 2;
    const bcx = tx * TILE + TILE / 2;
    const bcy = ty * TILE + TILE / 2;
    const d = Math.hypot(pcx - bcx, pcy - bcy);
    return d <= REACH_TILES * TILE;
  }

  function playerOverlapsTile(tx, ty) {
    const rx = tx * TILE;
    const ry = ty * TILE;
    return player.x < rx + TILE && player.x + player.w > rx && player.y < ry + TILE && player.y + player.h > ry;
  }

  function tryBreak(tx, ty) {
    if (!inBounds(tx, ty)) return;
    const b = getTile(tx, ty);
    if (b === AIR) return;
    if (!BLOCKS[b].breakable) {
      toast("기반암은 캘 수 없어요");
      return;
    }
    if (!canReach(tx, ty)) return;
    setTile(tx, ty, AIR);
    addItem(b, 1);
    renderHotbar();
  }

  function tryPlace(tx, ty) {
    if (!inBounds(tx, ty)) return;
    if (getTile(tx, ty) !== AIR) return;
    if (!canReach(tx, ty)) return;
    if (playerOverlapsTile(tx, ty)) return;
    const b = selectedBlock();
    if (countOf(b) <= 0) {
      toast(`${BLOCKS[b].name}이(가) 없어요. 캐서 모아보세요`);
      return;
    }
    if (!takeItem(b, 1)) return;
    setTile(tx, ty, b);
    renderHotbar();
  }

  const camera = { x: 0, y: 0 };

  function updateCamera() {
    const px = player.x + player.w / 2;
    const py = player.y + player.h / 2;
    camera.x = px - canvas.width / 2;
    camera.y = py - canvas.height / 2;
    camera.x = Math.max(0, Math.min(WORLD_W * TILE - canvas.width, camera.x));
    camera.y = Math.max(-80, Math.min(WORLD_H * TILE - canvas.height + 40, camera.y));
    if (WORLD_W * TILE < canvas.width) camera.x = (WORLD_W * TILE - canvas.width) / 2;
  }

  function resize() {
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    const r = canvas.getBoundingClientRect();
    canvas.width = Math.max(320, Math.floor(r.width * dpr));
    canvas.height = Math.max(240, Math.floor(r.height * dpr));
  }
  window.addEventListener("resize", resize);

  // 입력
  window.addEventListener("keydown", (e) => {
    if (e.repeat) return;
    const k = e.key.toLowerCase();
    if (["arrowleft", "arrowright", "arrowup", "arrowdown", " "].includes(k) || e.key === " ") e.preventDefault();
    keys.add(k);
    keys.add(e.key);
    if (k >= "1" && k <= String(HOTBAR.length)) {
      selected = Number(k) - 1;
      renderHotbar();
    }
    if (k === "h") elHelp.classList.toggle("hidden");
    if (k === "escape") elHelp.classList.add("hidden");
  });
  window.addEventListener("keyup", (e) => {
    keys.delete(e.key.toLowerCase());
    keys.delete(e.key);
  });

  canvas.addEventListener("mousemove", (e) => {
    const w = worldFromScreen(e.clientX, e.clientY);
    mouseTile = { tx: Math.floor(w.x / TILE), ty: Math.floor(w.y / TILE) };
  });
  canvas.addEventListener("mouseleave", () => { mouseTile = null; });
  canvas.addEventListener("mousedown", (e) => {
    if (e.button === 0) mouseDownLeft = true;
    if (e.button === 2) mouseDownRight = true;
  });
  window.addEventListener("mouseup", (e) => {
    if (e.button === 0) mouseDownLeft = false;
    if (e.button === 2) mouseDownRight = false;
  });
  canvas.addEventListener("contextmenu", (e) => e.preventDefault());
  canvas.addEventListener("wheel", (e) => {
    e.preventDefault();
    selected = (selected + (e.deltaY > 0 ? 1 : -1) + HOTBAR.length) % HOTBAR.length;
    renderHotbar();
  }, { passive: false });

  // 터치 버튼
  function bindHold(id, set) {
    const el = document.getElementById(id);
    const on = (e) => { e.preventDefault(); set(true); };
    const off = (e) => { e.preventDefault(); set(false); };
    el.addEventListener("pointerdown", on);
    el.addEventListener("pointerup", off);
    el.addEventListener("pointercancel", off);
    el.addEventListener("pointerleave", off);
  }
  bindHold("t-left", (v) => (touchState.left = v));
  bindHold("t-right", (v) => (touchState.right = v));
  bindHold("t-jump", (v) => (touchState.jump = v));
  document.getElementById("t-break").addEventListener("click", () => {
    if (mouseTile) tryBreak(mouseTile.tx, mouseTile.ty);
    else {
      const pcx = Math.floor((player.x + player.w / 2) / TILE);
      const pcy = Math.floor((player.y + player.h + 4) / TILE);
      tryBreak(pcx, pcy);
    }
  });
  document.getElementById("t-place").addEventListener("click", () => {
    const b = selectedBlock();
    const pcx = Math.floor((player.x + player.w / 2) / TILE);
    const dir = touchState.left ? -1 : 1;
    const targets = [
      [pcx + dir, Math.floor((player.y + player.h / 2) / TILE)],
      [pcx, Math.floor((player.y + player.h / 2) / TILE) - 1],
      [pcx, Math.floor((player.y + player.h + 4) / TILE)],
    ];
    for (const [tx, ty] of targets) {
      if (getTile(tx, ty) === AIR && !playerOverlapsTile(tx, ty) && countOf(b) > 0) {
        tryPlace(tx, ty);
        break;
      }
    }
  });
  canvas.addEventListener("touchstart", (e) => {
    const t = e.touches[0];
    if (t) {
      const w = worldFromScreen(t.clientX, t.clientY);
      mouseTile = { tx: Math.floor(w.x / TILE), ty: Math.floor(w.y / TILE) };
    }
  }, { passive: true });

  document.getElementById("btn-help").addEventListener("click", () => elHelp.classList.remove("hidden"));
  document.getElementById("btn-close-help").addEventListener("click", () => elHelp.classList.add("hidden"));
  elHelp.addEventListener("click", (e) => { if (e.target === elHelp) elHelp.classList.add("hidden"); });
  document.getElementById("btn-save").addEventListener("click", () => { save(); toast("저장했어요"); });
  document.getElementById("btn-respawn").addEventListener("click", respawn);
  document.getElementById("btn-new").addEventListener("click", () => {
    if (!confirm("새 월드를 만들까요? 저장되지 않은 변경은 사라집니다.")) return;
    newGame((Math.random() * 1e9) | 0);
    toast("새 월드 생성!");
  });
  document.getElementById("btn-craft").addEventListener("click", () => {
    if (takeItem(LOG, 1)) {
      addItem(PLANKS, 4);
      renderHotbar();
      toast("통나무 1 → 판자 4 제작!");
    } else {
      toast("통나무가 필요해요");
    }
  });

  elSeed.addEventListener("click", () => {
    const v = prompt("시드 입력 (숫자)", String(world.seed));
    if (v === null) return;
    const n = Number(v);
    if (!Number.isFinite(n)) { toast("숫자 시드만 가능해요"); return; }
    newGame(n | 0);
  });
  elSeed.style.cursor = "pointer";
  elSeed.title = "클릭해서 시드 변경";

  function renderHotbar() {
    elHotbar.innerHTML = "";
    HOTBAR.forEach((b, i) => {
      const d = document.createElement("div");
      d.className = "slot" + (i === selected ? " selected" : "");
      d.innerHTML = `<span class="swatch" style="background:${BLOCKS[b].color}"></span>
        <span class="meta"><span class="name">${BLOCKS[b].name}</span>
        <span class="count">${countOf(b)}</span> <span class="key">${i + 1}</span></span>`;
      d.addEventListener("click", () => { selected = i; renderHotbar(); });
      elHotbar.appendChild(d);
    });
  }

  function save() {
    try {
      const payload = {
        v: 1,
        seed: world.seed,
        data: Array.from(world.data),
        player: { x: player.x, y: player.y },
        inv: Array.from(inventory.entries()),
        time: timeOfDay,
        selected,
      };
      localStorage.setItem(SAVE_KEY, JSON.stringify(payload));
    } catch (err) {
      console.warn("save failed", err);
    }
  }
  function load() {
    try {
      const raw = localStorage.getItem(SAVE_KEY);
      if (!raw) return false;
      const p = JSON.parse(raw);
      if (!p || p.v !== 1 || !Array.isArray(p.data) || p.data.length !== WORLD_W * WORLD_H) return false;
      world.seed = p.seed | 0;
      world.data.set(p.data);
      for (let x = 0; x < WORLD_W; x++) {
        for (let y = 0; y < WORLD_H; y++) {
          if (world.data[idx(x, y)] !== AIR) { world.surface[x] = Math.min(world.surface[x] || y, y); }
        }
      }
      // 표면 복원: 저장된 월드가 있으면 표면 재계산
      recomputeSurface();
      player.x = p.player.x;
      player.y = p.player.y;
      inventory.clear();
      for (const [k, v] of p.inv) inventory.set(Number(k), v);
      timeOfDay = typeof p.time === "number" ? p.time : 0.3;
      selected = p.selected || 0;
      spawn = findSpawn();
      return true;
    } catch (err) {
      console.warn("load failed", err);
      return false;
    }
  }
  function recomputeSurface() {
    for (let x = 0; x < WORLD_W; x++) {
      let s = WORLD_H;
      for (let y = 0; y < WORLD_H; y++) {
        if (world.data[idx(x, y)] !== AIR) { s = y; break; }
      }
      world.surface[x] = s;
    }
  }

  function newGame(seed) {
    genWorld(seed);
    starterKit();
    spawn = findSpawn();
    player.x = spawn.x;
    player.y = spawn.y;
    player.vx = 0;
    player.vy = 0;
    timeOfDay = 0.3;
    selected = 0;
    elSeed.textContent = `seed ${world.seed}`;
    renderHotbar();
    save();
  }

  // 렌더
  function skyColor(t) {
    // t: 0~1, 0.25 정오 가정
    const day = Math.cos((t - 0.3) * Math.PI * 2) * 0.5 + 0.5;
    const top = [26 + day * 90, 38 + day * 120, 70 + day * 150];
    const bottom = [40 + day * 130, 60 + day * 140, 100 + day * 120];
    return { top: `rgb(${top.map(Math.round).join(",")})`, bottom: `rgb(${bottom.map(Math.round).join(",")})`, day };
  }

  function drawBlock(b, sx, sy, tx, ty) {
    const info = BLOCKS[b];
    ctx.fillStyle = info.color;
    ctx.fillRect(sx, sy, TILE, TILE);
    // 질감: 해시 기반 점
    const h1 = hash2(tx, ty, 11);
    const h2 = hash2(tx, ty, 77);
    ctx.fillStyle = "rgba(0,0,0,0.18)";
    ctx.fillRect(sx + Math.floor(h1 * 24), sy + Math.floor(h2 * 24), 5, 5);
    ctx.fillStyle = "rgba(255,255,255,0.12)";
    ctx.fillRect(sx + Math.floor(h2 * 20), sy + Math.floor(h1 * 20), 4, 4);
    if (b === GRASS) {
      ctx.fillStyle = "#4a8f33";
      ctx.fillRect(sx, sy + 20, TILE, TILE - 20);
      ctx.fillStyle = "#6cc24a";
      ctx.fillRect(sx, sy, TILE, 9);
    }
    if (b === LOG) {
      ctx.fillStyle = "rgba(0,0,0,0.3)";
      ctx.fillRect(sx + 6, sy, 4, TILE);
      ctx.fillRect(sx + 22, sy, 4, TILE);
    }
    if (b === COAL || b === IRON || b === DIAMOND) {
      ctx.fillStyle = "#2b2d33";
      ctx.fillRect(sx + 4, sy + 4, TILE - 8, TILE - 8);
      ctx.fillStyle = info.color;
      ctx.fillRect(sx + 8, sy + 8, 6, 6);
      ctx.fillRect(sx + 19, sy + 14, 5, 5);
      ctx.fillRect(sx + 10, sy + 20, 4, 4);
    }
    if (b === PLANKS) {
      ctx.fillStyle = "rgba(0,0,0,0.25)";
      for (let yy = 7; yy < TILE; yy += 8) ctx.fillRect(sx, sy + yy, TILE, 2);
    }
    if (b === BEDROCK) {
      ctx.fillStyle = "rgba(255,255,255,0.08)";
      ctx.fillRect(sx + 5, sy + 5, 8, 8);
      ctx.fillRect(sx + 19, sy + 19, 7, 7);
    }
    ctx.strokeStyle = "rgba(0,0,0,0.25)";
    ctx.lineWidth = 1;
    ctx.strokeRect(sx + 0.5, sy + 0.5, TILE - 1, TILE - 1);
  }

  function render(dt, fps) {
    const sky = skyColor(timeOfDay);
    const g = ctx.createLinearGradient(0, 0, 0, canvas.height);
    g.addColorStop(0, sky.top);
    g.addColorStop(1, sky.bottom);
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 태양/달
    const sunA = (timeOfDay - 0.25) * Math.PI * 2;
    const sunX = canvas.width / 2 + Math.cos(sunA) * canvas.width * 0.4;
    const sunY = canvas.height * 0.45 - Math.sin(sunA) * canvas.height * 0.35;
    ctx.fillStyle = sky.day > 0.5 ? "#ffe27a" : "#e8ecf5";
    ctx.beginPath();
    ctx.arc(sunX, sunY, 26, 0, Math.PI * 2);
    ctx.fill();

    const x0 = Math.max(0, Math.floor(camera.x / TILE));
    const y0 = Math.max(0, Math.floor(camera.y / TILE));
    const x1 = Math.min(WORLD_W - 1, Math.ceil((camera.x + canvas.width) / TILE));
    const y1 = Math.min(WORLD_H - 1, Math.ceil((camera.y + canvas.height) / TILE));
    for (let ty = y0; ty <= y1; ty++) {
      for (let tx = x0; tx <= x1; tx++) {
        const b = world.data[idx(tx, ty)];
        if (b === AIR) continue;
        const sx = Math.round(tx * TILE - camera.x);
        const sy = Math.round(ty * TILE - camera.y);
        drawBlock(b, sx, sy, tx, ty);
      }
    }

    // 플레이어
    const psx = Math.round(player.x - camera.x);
    const psy = Math.round(player.y - camera.y);
    ctx.fillStyle = "#222";
    ctx.fillRect(psx, psy + player.h - 8, player.w, 8); // 다리
    ctx.fillStyle = "#3fa7ff";
    ctx.fillRect(psx, psy + 12, player.w, player.h - 20); // 몸
    ctx.fillStyle = "#f2c89b";
    ctx.fillRect(psx + 2, psy, player.w - 4, 14); // 얼굴
    ctx.fillStyle = "#2b2118";
    ctx.fillRect(psx + 2, psy, player.w - 4, 5); // 머리
    ctx.fillStyle = "#fff";
    ctx.fillRect(psx + 5, psy + 6, 4, 4);
    ctx.fillRect(psx + 13, psy + 6, 4, 4);
    ctx.fillStyle = "#111";
    ctx.fillRect(psx + 6, psy + 7, 2, 2);
    ctx.fillRect(psx + 14, psy + 7, 2, 2);
    // 손에 든 블록
    const held = selectedBlock();
    ctx.fillStyle = BLOCKS[held].color;
    ctx.fillRect(psx + player.w - 2, psy + 22, 12, 12);
    ctx.strokeStyle = "rgba(0,0,0,0.5)";
    ctx.strokeRect(psx + player.w - 2.5, psy + 21.5, 12, 12);

    // 조준 하이라이트
    if (mouseTile && inBounds(mouseTile.tx, mouseTile.ty)) {
      const b = getTile(mouseTile.tx, mouseTile.ty);
      const sx = Math.round(mouseTile.tx * TILE - camera.x);
      const sy = Math.round(mouseTile.ty * TILE - camera.y);
      const ok = b === AIR ? countOf(selectedBlock()) > 0 : BLOCKS[b].breakable;
      ctx.strokeStyle = canReach(mouseTile.tx, mouseTile.ty)
        ? (ok ? "#ffffff" : "#ff5a5a")
        : "rgba(255,255,255,0.25)";
      ctx.lineWidth = 2;
      ctx.strokeRect(sx + 1, sy + 1, TILE - 2, TILE - 2);
    }

    // 밤 오버레이
    const night = 1 - sky.day;
    if (night > 0.15) {
      ctx.fillStyle = `rgba(8,10,40,${(night * 0.45).toFixed(3)})`;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    elFps.textContent = `${Math.round(fps)} FPS`;
    const ptx = Math.floor((player.x + player.w / 2) / TILE);
    const pty = Math.floor((player.y + player.h / 2) / TILE);
    elPos.textContent = `X ${ptx} · Y ${pty}`;
    elTime.textContent = sky.day > 0.65 ? "낮" : sky.day > 0.4 ? "해 질 녘" : "밤";
  }

  let last = performance.now();
  let fpsSmooth = 60;
  let acc = 0;
  let saveTimer = 0;

  function frame(now) {
    let dt = (now - last) / 1000;
    last = now;
    if (dt > 0.1) dt = 0.1;
    fpsSmooth = fpsSmooth * 0.95 + (1 / Math.max(dt, 1e-4)) * 0.05;

    const left = keys.has("a") || keys.has("A") || keys.has("ArrowLeft") || touchState.left;
    const right = keys.has("d") || keys.has("D") || keys.has("ArrowRight") || touchState.right;
    const jump = keys.has(" ") || keys.has("w") || keys.has("W") || keys.has("ArrowUp") || touchState.jump;

    const target = (right ? MOVE_SPEED : 0) - (left ? MOVE_SPEED : 0);
    const accel = player.onGround ? 2600 : 1500;
    if (player.vx < target) player.vx = Math.min(target, player.vx + accel * dt);
    else if (player.vx > target) player.vx = Math.max(target, player.vx - accel * dt);
    player.vy += GRAVITY * dt;
    if (player.vy > 1400) player.vy = 1400;
    if (jump && player.onGround) {
      player.vy = -JUMP_VEL;
      player.onGround = false;
    }

    // 고정 스텝 물리
    acc += dt;
    const step = 1 / 120;
    let n = 0;
    while (acc >= step && n < 8) {
      moveAndCollide(step);
      acc -= step;
      n++;
    }

    if ((mouseDownLeft || touchState.jump === "break") && mouseTile) {
      // 좌클릭 연타 캐기: 0.18초 간격
      if (!breakProgress || now - breakProgress > 180) {
        tryBreak(mouseTile.tx, mouseTile.ty);
        breakProgress = now;
      }
    }
    if (mouseDownRight && mouseTile) {
      if (!breakProgress || now - breakProgress > 200) {
        tryPlace(mouseTile.tx, mouseTile.ty);
        breakProgress = now;
      }
    }

    timeOfDay = (timeOfDay + dt / DAY_SECONDS) % 1;
    updateCamera();
    render(dt, fpsSmooth);

    saveTimer += dt;
    if (saveTimer > 10) {
      saveTimer = 0;
      save();
    }
    requestAnimationFrame(frame);
  }

  window.addEventListener("beforeunload", save);

  // 부트
  resize();
  setTimeout(resize, 50);
  const restored = load();
  if (restored) {
    elSeed.textContent = `seed ${world.seed}`;
    renderHotbar();
    toast("저장된 월드를 불러왔어요");
  } else {
    const params = new URLSearchParams(location.search);
    const s = params.get("seed");
    newGame(s !== null && s !== "" && Number.isFinite(Number(s)) ? Number(s) | 0 : 20260201);
  }
  renderHotbar();
  requestAnimationFrame((t) => { last = t; requestAnimationFrame(frame); });

  // 테스트용 노출
  window.__mc2d = {
    BLOCKS, HOTBAR, TILE, WORLD_W, WORLD_H,
    getTile, setTile, isSolid, genWorld, world, player, inventory,
    newGame, tryBreak, tryPlace, findSpawn, collides,
  };
})();
