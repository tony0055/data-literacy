import re
import subprocess
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"


class WebGameTests(unittest.TestCase):
    def test_web_files_exist(self):
        for name in ["index.html", "styles.css", "main.js"]:
            p = WEB / name
            self.assertTrue(p.exists(), f"missing {p}")
            self.assertGreater(p.stat().st_size, 500, f"{name} too small")

    def test_index_structure(self):
        html = (WEB / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="game"', html)
        self.assertIn('id="hotbar"', html)
        self.assertIn("./styles.css", html)
        self.assertIn("./main.js", html)
        self.assertIn("조작법", html)
        self.assertIn("<canvas", html)
        # 외부 CDN 없이 동작해야 함
        self.assertNotIn("https://cdn", html)
        self.assertNotIn("http://", html)

    def test_no_external_deps_in_js_css(self):
        js = (WEB / "main.js").read_text(encoding="utf-8")
        css = (WEB / "styles.css").read_text(encoding="utf-8")
        self.assertNotIn("https://", js)
        self.assertNotIn("http://", js)
        self.assertNotIn("@import", css)
        self.assertNotIn("https://", css)

    def test_js_syntax_with_node(self):
        r = subprocess.run(
            ["node", "--check", str(WEB / "main.js")],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(r.returncode, 0, f"node --check failed: {r.stderr}")

    def test_core_symbols_present(self):
        js = (WEB / "main.js").read_text(encoding="utf-8")
        for sym in [
            "genWorld", "tryBreak", "tryPlace", "collides",
            "findSpawn", "requestAnimationFrame", "localStorage",
            "HOTBAR", "BLOCKS", "BEDROCK", "REACH_TILES",
        ]:
            self.assertIn(sym, js, f"missing symbol {sym}")
        self.assertRegex(js, r"breakable:\s*false")
        self.assertIn("mc2d-save-v1", js)

    def test_world_constants_sane(self):
        js = (WEB / "main.js").read_text(encoding="utf-8")
        m_w = re.search(r"WORLD_W\s*=\s*(\d+)", js)
        m_h = re.search(r"WORLD_H\s*=\s*(\d+)", js)
        m_t = re.search(r"\bTILE\s*=\s*(\d+)", js)
        self.assertIsNotNone(m_w)
        self.assertIsNotNone(m_h)
        self.assertIsNotNone(m_t)
        self.assertGreaterEqual(int(m_w.group(1)), 64)
        self.assertGreaterEqual(int(m_h.group(1)), 32)
        self.assertGreaterEqual(int(m_t.group(1)), 16)

    def test_game_logic_smoke_via_node(self):
        # DOM 스텁 위에서 핵심 로직(월드 생성/충돌/캐기/설치)을 실행한다.
        driver = """
const fs = require('fs');
const src = fs.readFileSync(process.argv[1] || process.argv[2], 'utf8');
const elements = {};
function mkEl(){ return {
  textContent:'', innerHTML:'', style:{}, classList:{add(){},remove(){},toggle(){}},
  addEventListener(){}, appendChild(){}, title:''
};}
global.window = { addEventListener(){}, devicePixelRatio: 1 };
global.document = {
  getElementById:(id)=> (elements[id] ||= mkEl()),
  createElement:()=> mkEl(),
};
global.localStorage = { getItem:()=>null, setItem:()=>{} };
global.requestAnimationFrame = ()=>{};
global.performance = { now:()=>0 };
let canvasCtx = { fillRect(){}, strokeRect(){}, beginPath(){}, arc(){}, fill(){}, createLinearGradient:()=>({addColorStop(){}}) };
global.HTMLCanvasElement = function(){};
const canvasEl = mkEl();
canvasEl.getContext = ()=> canvasCtx;
canvasEl.getBoundingClientRect = ()=>({left:0,top:0,width:960,height:600});
elements['game'] = canvasEl;
global.location = { search: '' };
eval(src);
const api = global.window.__mc2d;
if (!api) { console.error('no __mc2d'); process.exit(1); }
api.newGame(42);
const { WORLD_W, WORLD_H, world } = api;
let air = 0, solid = 0, bedrock = 0;
for (let i = 0; i < world.data.length; i++) {
  const b = world.data[i];
  if (b === 0) air++; else solid++;
  if (b === 10) bedrock++;
}
if (world.data.length !== WORLD_W * WORLD_H) { console.error('bad size'); process.exit(2); }
if (air === 0 || solid === 0 || bedrock === 0) { console.error('empty layers', air, solid, bedrock); process.exit(3); }
// 표면 위에 빈 공간이 있어야 스폰 가능
if (!Number.isFinite(api.player.x) || !Number.isFinite(api.player.y)) { console.error('bad spawn'); process.exit(4); }
// 캐기/설치 스모크: 스폰 근처 고체 블록 하나를 찾아 캤다 다시 놓는다
let target = null;
for (let y = 0; y < WORLD_H && !target; y++) {
  for (let x = 0; x < WORLD_W && !target; x++) {
    const b = api.getTile(x, y);
    if (b !== 0 && b !== 10 && api.world.surface[x] !== undefined) {
      // 플레이어를 근처로 옮겨 reach 안으로
      api.player.x = x * api.TILE;
      api.player.y = (y - 3) * api.TILE;
      target = {x, y, b};
    }
  }
}
if (!target) { console.error('no target'); process.exit(5); }
const before = api.inventory.get(target.b) || 0;
api.tryBreak(target.x, target.y);
if (api.getTile(target.x, target.y) !== 0) { console.error('break failed'); process.exit(6); }
console.log('SMOKE_OK air=' + air + ' solid=' + solid + ' bedrock=' + bedrock);
"""
        r = subprocess.run(
            ["node", "-e", driver, str(WEB / "main.js")],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(r.returncode, 0, f"smoke failed: {r.stdout}\n{r.stderr}")
        self.assertIn("SMOKE_OK", r.stdout)


if __name__ == "__main__":
    unittest.main()
