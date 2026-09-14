/* Bizimkent FEST — 1080x1350 sosyal medya görsel üreteci
   Kullanım:  node sosyal-medya/olustur.mjs
   Gerekli:   playwright (global kurulu) + fontlar.css (gömülü Poppins / Instrument Serif) */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';
import { POSTLAR, FEST } from './veri.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const KOK = path.join(__dirname, '..');
const CIKTI = path.join(__dirname, 'gorseller');
const W = 1080, H = 1350;

const FONTLAR = fs.readFileSync(path.join(__dirname, 'fontlar.css'), 'utf8');
const LOGO = 'data:image/png;base64,' +
  fs.readFileSync(path.join(KOK, 'img', 'bizimkent-fest-logo.png')).toString('base64');

const RENK = {
  red:'#F0403A', orange:'#F5871F', yellow:'#FFC220', green:'#3DAE3A',
  blue:'#0E9DE0', purple:'#7B3FA0', pink:'#EC4899', navy:'#141C4E'
};
/* Sarı zeminde okunabilirlik için metin rengi ayrımı */
const METIN = { ...RENK, yellow:'#8a5d00' };

/* Deterministik konfeti — her post aynı çıktı versin diye id'den tohumlanır */
function tohum(s){ let h = 2166136261; for (const c of s){ h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return () => { h ^= h << 13; h ^= h >>> 17; h ^= h << 5; return ((h >>> 0) % 10000) / 10000; }; }

function konfeti(id){
  const rnd = tohum(id);
  const renkler = Object.values(RENK).slice(0, 7);
  let s = '';
  for (let i = 0; i < 26; i++){
    const x = rnd() * 100, y = rnd() * 100;
    // orta bölgeyi (metin alanı) boş bırak
    if (x > 14 && x < 86 && y > 12 && y < 88) continue;
    const c = renkler[Math.floor(rnd() * renkler.length)];
    const d = 10 + rnd() * 20;
    const rot = Math.floor(rnd() * 90);
    const kare = rnd() > .55;
    s += `<span style="left:${x.toFixed(2)}%;top:${y.toFixed(2)}%;width:${d.toFixed(0)}px;height:${d.toFixed(0)}px;background:${c};
      border-radius:${kare ? '4px' : '50%'};transform:rotate(${rot}deg);opacity:${(0.5 + rnd() * 0.4).toFixed(2)}"></span>`;
  }
  return `<div class="konfeti">${s}</div>`;
}

const esc = t => String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const satirla = t => esc(t).replace(/\n/g, '<br>');

function ustBant(){
  return `<header class="ust">
    <img class="logo" src="${LOGO}" alt="Bizimkent FEST">
    <span class="tarih">${esc(FEST.tarih)}</span>
  </header>`;
}

function altBant(){
  return `<footer class="alt">
    <span><i style="background:${RENK.yellow}"></i>${esc(FEST.yer)}</span>
    <span><i style="background:${RENK.green}"></i>Ücretsiz katılım</span>
    <span><i style="background:${RENK.pink}"></i>${esc(FEST.ig)}</span>
  </footer>`;
}

function govdeEtkinlik(p){
  const zamanlar = p.zamanlar.map(z => `
    <div class="zaman">
      <div class="zsol"><b>${esc(z.gun)}</b><small>${esc(z.alt)}</small></div>
      <div class="zsag">${esc(z.saat)}</div>
    </div>`).join('');
  return `
    <main class="govde">
      <div class="etiketler">
        <span class="kat">${esc(p.kat)}</span>
        ${p.rozet ? `<span class="rozet">${esc(p.rozet)}</span>` : ''}
      </div>
      <h1 class="baslik">${satirla(p.baslik)}</h1>
      <p class="serif">${esc(p.serif)}</p>
    </main>
    <section class="zamanlar">${zamanlar}</section>
    ${p.not ? `<p class="not">${esc(p.not)}</p>` : ''}`;
}

function govdeGun(p){
  const satirlar = p.program.map(([saat, ad]) => `
    <div class="psatir"><span class="psaat">${esc(saat)}</span><span class="pad">${esc(ad)}</span></div>`).join('');
  return `
    <main class="govde gun">
      <div class="etiketler"><span class="kat">GÜNÜN PROGRAMI</span><span class="rozet">${esc(p.sira)}</span></div>
      <h1 class="baslik gunbaslik">${esc(p.tarih)}<br><span class="gunad">${esc(p.gun)}</span></h1>
      <p class="serif">${esc(p.serif)}</p>
    </main>
    <section class="program">${satirlar}</section>`;
}

function govdeDuyuru(p){
  const gunRenk = [RENK.red, RENK.green, RENK.blue, RENK.purple];
  const kutu = p.gunler.map(([g, k, ad], i) => `
    <div class="dgun" style="--c:${gunRenk[i]}">
      <b>${esc(g)}</b><small>${esc(k)}</small><span>${esc(ad)}</span>
    </div>`).join('');
  return `
    <main class="govde duyuru">
      <div class="etiketler"><span class="kat">BEYLİKDÜZÜ MAHALLE FESTİVALİ</span></div>
      <h1 class="baslik dbaslik">Bizimkent<br><span class="grad">FEST</span></h1>
      <p class="serif">${esc(p.serif)}</p>
      <div class="dtarih">24<span>–</span>27 <em>EYLÜL 2026</em></div>
    </main>
    <section class="dgunler">${kutu}</section>
    ${p.not ? `<p class="not">${esc(p.not)}</p>` : ''}`;
}

function html(p){
  const c = RENK[p.renk], m = METIN[p.renk];
  const govde = p.tip === 'gun' ? govdeGun(p) : p.tip === 'duyuru' ? govdeDuyuru(p) : govdeEtkinlik(p);
  return `<!doctype html><html lang="tr"><head><meta charset="utf-8">
<style>
${FONTLAR}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:${W}px;height:${H}px}
body{font-family:'Poppins',sans-serif;-webkit-font-smoothing:antialiased}
.post{position:relative;width:${W}px;height:${H}px;overflow:hidden;background:#FBF8F1;color:#161618;
  display:flex;flex-direction:column;padding:64px 70px 58px;--c:${c};--m:${m}}
.post > img.filigran{position:absolute;width:880px;right:-300px;top:-190px;opacity:.06;transform:rotate(9deg);z-index:1}
.post::before{content:'';position:absolute;width:820px;height:820px;right:-300px;top:-330px;border-radius:50%;
  background:radial-gradient(circle,var(--c) 0%,rgba(255,255,255,0) 68%);opacity:.22}
.post::after{content:'';position:absolute;width:700px;height:700px;left:-320px;bottom:-300px;border-radius:50%;
  background:radial-gradient(circle,var(--c) 0%,rgba(255,255,255,0) 70%);opacity:.14}
.konfeti span{position:absolute;display:block}
.konfeti{position:absolute;inset:0;pointer-events:none}
.post > *{position:relative;z-index:2}

.ust{display:flex;align-items:center;justify-content:space-between;gap:20px}
.logo{height:118px;width:auto;display:block}
.tarih{font-size:19px;font-weight:700;letter-spacing:.17em;padding:13px 22px;border-radius:100px;
  border:1.6px solid rgba(20,28,78,.22);color:#141C4E;background:rgba(255,255,255,.72);white-space:nowrap}

.govde{flex:1;display:flex;flex-direction:column;justify-content:flex-end;padding:40px 0 38px}
.etiketler{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:24px}
.kat{font-size:21px;font-weight:800;letter-spacing:.2em;color:var(--m)}
.rozet{font-size:17px;font-weight:800;letter-spacing:.14em;color:#fff;background:var(--c);
  padding:9px 16px;border-radius:100px}
.baslik{font-size:124px;font-weight:800;letter-spacing:-.045em;line-height:.95}
.serif{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-size:44px;line-height:1.16;
  color:#4a4a55;margin-top:24px;max-width:26ch}

.zamanlar{display:flex;flex-direction:column;gap:14px;margin-top:8px}
.zaman{display:flex;align-items:center;justify-content:space-between;gap:18px;background:#fff;
  border:1.5px solid #e7e3da;border-left:10px solid var(--c);border-radius:22px;padding:22px 28px}
.zsol b{display:block;font-size:31px;font-weight:700;letter-spacing:-.02em;line-height:1.1}
.zsol small{display:block;font-size:19px;font-weight:600;color:#7a7a83;margin-top:3px;letter-spacing:.02em}
.zsag{font-size:35px;font-weight:800;letter-spacing:-.02em;color:var(--m);white-space:nowrap}
.not{margin-top:22px;font-size:22px;font-weight:600;color:#55555f;padding-left:16px;border-left:4px solid var(--c)}

.gun .baslik{font-size:96px}
.gunad{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-weight:400;
  letter-spacing:-.01em;color:var(--m)}
.program{display:flex;flex-direction:column;gap:9px;margin-top:6px}
.psatir{display:flex;align-items:center;gap:20px;background:#fff;border:1.5px solid #e7e3da;
  border-radius:18px;padding:16px 22px}
.psaat{font-size:22px;font-weight:800;color:var(--m);white-space:nowrap;letter-spacing:-.01em;min-width:210px}
.pad{font-size:24px;font-weight:600;letter-spacing:-.015em;line-height:1.2}

.duyuru{justify-content:flex-end}
.dbaslik{font-size:150px;line-height:.9}
.grad{background:linear-gradient(100deg,${RENK.red},${RENK.orange} 28%,${RENK.yellow} 46%,${RENK.green} 68%,${RENK.blue} 100%);
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.dtarih{margin-top:34px;font-size:64px;font-weight:800;letter-spacing:-.03em;color:#141C4E;display:flex;
  align-items:baseline;gap:10px}
.dtarih span{color:var(--c)}
.dtarih em{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-weight:400;font-size:52px;
  letter-spacing:0;color:#4a4a55}
.dgunler{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:30px}
.dgun{background:#fff;border:1.5px solid #e7e3da;border-top:9px solid var(--c);border-radius:20px;padding:20px 16px}
.dgun b{display:block;font-size:46px;font-weight:800;letter-spacing:-.04em;line-height:1}
.dgun small{display:block;font-size:17px;font-weight:700;letter-spacing:.14em;color:var(--c);margin-top:4px}
.dgun span{display:block;font-size:19px;font-weight:600;color:#55555f;margin-top:12px;line-height:1.25}

.alt{margin-top:26px;background:#141C4E;color:#fff;border-radius:26px;padding:26px 30px;
  display:flex;align-items:center;justify-content:space-between;gap:16px;font-size:21px;font-weight:600}
.alt span{display:inline-flex;align-items:center;gap:11px;white-space:nowrap}
.alt i{width:11px;height:11px;border-radius:50%;display:inline-block}
</style></head><body>
<div class="post" id="post">
  ${konfeti(p.id)}
  <img class="filigran" src="${LOGO}" alt="">
  ${ustBant()}
  ${govde}
  ${altBant()}
</div>
</body></html>`;
}

/* Fontlar yüklendikten sonra çalışır: içerik 1080x1350'yi aşarsa başlığı/serif satırı kademeli küçültür */
function sigdir(H){
  const post = document.getElementById('post');
  const alt = post.querySelector('.alt');
  const h1 = post.querySelector('.baslik');
  const serif = post.querySelector('.serif');
  const sinir = H - parseFloat(getComputedStyle(post).paddingBottom) + 2;
  const tasiyor = () => alt.getBoundingClientRect().bottom > sinir;
  let s = parseFloat(getComputedStyle(h1).fontSize);
  while (tasiyor() && s > 44){ s -= 2; h1.style.fontSize = s + 'px'; }
  if (serif){
    let t = parseFloat(getComputedStyle(serif).fontSize);
    while (tasiyor() && t > 26){ t -= 2; serif.style.fontSize = t + 'px'; }
  }
  return { tasan: tasiyor(), baslikPx: parseFloat(getComputedStyle(h1).fontSize) };
}

const tarayici = await chromium.launch();
const sayfa = await tarayici.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
fs.mkdirSync(CIKTI, { recursive: true });

for (const p of [...POSTLAR].sort((a, b) => a.id.localeCompare(b.id))){
  await sayfa.setContent(html(p), { waitUntil: 'load' });
  await sayfa.evaluate(() => document.fonts.ready.then(() => true));
  const o = await sayfa.evaluate(sigdir, H);
  await sayfa.screenshot({ path: path.join(CIKTI, p.id + '.png'), clip: { x: 0, y: 0, width: W, height: H } });
  console.log(`${o.tasan ? '⚠ TAŞMA' : '✓'}  ${p.id}.png  (başlık ${o.baslikPx}px)`);
}
await tarayici.close();
console.log(`\n${POSTLAR.length} görsel üretildi → sosyal-medya/gorseller/`);
