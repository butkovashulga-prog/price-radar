<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Price Radar — моніторинг цін конкурентів</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#17191d;
  --panel:#1f2229;
  --panel-2:#262a33;
  --line:#333845;
  --text:#e8eaef;
  --muted:#8b92a1;
  --accent:#ffb020;          /* сигнальний жовтий інструментального класу */
  --accent-ink:#17191d;
  --ok:#4cd08a;
  --bad:#ff6b6b;
  --radius:10px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{
  background:var(--bg);
  color:var(--text);
  font-family:'IBM Plex Sans',system-ui,sans-serif;
  font-size:15px;
  line-height:1.55;
  min-height:100vh;
}
.wrap{max-width:1060px;margin:0 auto;padding:36px 20px 80px}

/* ---------- шапка ---------- */
header{display:flex;align-items:baseline;gap:14px;margin-bottom:6px;flex-wrap:wrap}
h1{
  font-family:'Oswald',sans-serif;
  font-weight:600;
  font-size:clamp(26px,4vw,36px);
  letter-spacing:.04em;
  text-transform:uppercase;
}
h1 .dot{color:var(--accent)}
.tagline{color:var(--muted);font-size:14px}
.scan-line{
  height:3px;width:100%;margin:18px 0 28px;border-radius:2px;
  background:linear-gradient(90deg,var(--accent) 0 42px,var(--line) 42px 100%);
}

/* ---------- форма ---------- */
.card{
  background:var(--panel);
  border:1px solid var(--line);
  border-radius:var(--radius);
  padding:22px;
}
label{display:block;font-weight:600;margin-bottom:8px;font-size:14px}
label span{color:var(--muted);font-weight:400}
textarea{
  width:100%;min-height:150px;resize:vertical;
  background:var(--panel-2);
  border:1px solid var(--line);
  border-radius:8px;
  color:var(--text);
  font-family:'IBM Plex Mono',monospace;
  font-size:13px;line-height:1.7;
  padding:14px 16px;
}
textarea:focus{outline:2px solid var(--accent);outline-offset:1px;border-color:transparent}
.actions{display:flex;gap:12px;margin-top:16px;flex-wrap:wrap;align-items:center}
button{
  font-family:'IBM Plex Sans',sans-serif;
  font-weight:600;font-size:14px;
  border:none;border-radius:8px;
  padding:12px 22px;cursor:pointer;
  transition:transform .12s ease, filter .12s ease;
}
button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
button:active{transform:translateY(1px)}
.btn-primary{background:var(--accent);color:var(--accent-ink)}
.btn-primary:hover{filter:brightness(1.08)}
.btn-primary[disabled]{opacity:.55;cursor:wait}
.btn-ghost{background:transparent;color:var(--muted);border:1px solid var(--line)}
.btn-ghost:hover{color:var(--text);border-color:var(--muted)}
.hint{color:var(--muted);font-size:13px}

/* ---------- статус ---------- */
#status{margin:20px 0 0;font-size:14px;color:var(--muted);min-height:22px}
#status.scanning::before{
  content:"";display:inline-block;width:10px;height:10px;margin-right:9px;
  border-radius:50%;background:var(--accent);
  animation:pulse 1s ease-in-out infinite;
}
@keyframes pulse{0%,100%{opacity:.25}50%{opacity:1}}
@media (prefers-reduced-motion:reduce){ #status.scanning::before{animation:none} }

/* ---------- результати ---------- */
#results{margin-top:26px;display:none}
.results-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:10px}
.results-head h2{font-family:'Oswald',sans-serif;font-weight:500;font-size:19px;letter-spacing:.05em;text-transform:uppercase}
.table-scroll{overflow-x:auto;border:1px solid var(--line);border-radius:var(--radius)}
table{width:100%;border-collapse:collapse;min-width:760px;background:var(--panel)}
th,td{padding:13px 16px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:none}
th{
  font-size:12px;letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted);font-weight:600;background:var(--panel-2);
}
td.num{font-family:'IBM Plex Mono',monospace;font-weight:600;white-space:nowrap}
.store{color:var(--muted);font-size:13px}
.name{max-width:340px}
.name a{color:var(--text);text-decoration:none;border-bottom:1px dashed var(--line)}
.name a:hover{border-bottom-color:var(--accent)}
.old{color:var(--muted);text-decoration:line-through;font-weight:400;font-size:12.5px;display:block}
.badge{
  display:inline-block;font-size:12px;font-weight:600;
  border-radius:6px;padding:3px 9px;white-space:nowrap;
}
.badge.ok{background:rgba(76,208,138,.14);color:var(--ok)}
.badge.warn{background:rgba(255,176,32,.14);color:var(--accent)}
.badge.bad{background:rgba(255,107,107,.14);color:var(--bad)}
.badge.best{background:var(--accent);color:var(--accent-ink)}
tr.best-row td{background:rgba(255,176,32,.05)}
.delta{font-size:12.5px;color:var(--muted);display:block;margin-top:2px;font-family:'IBM Plex Mono',monospace}
.err{color:var(--bad);font-size:13px}

footer{margin-top:40px;color:var(--muted);font-size:13px}
</style>
</head>
<body>
<div class="wrap">

  <header>
    <h1>Price Radar<span class="dot">.</span></h1>
    <span class="tagline">ціни конкурентів по одному товару — за хвилину</span>
  </header>
  <div class="scan-line" aria-hidden="true"></div>

  <div class="card">
    <label for="links">Посилання на сторінки товарів <span>— по одному в рядку</span></label>
    <textarea id="links" placeholder="https://rozetka.com.ua/...&#10;https://dnipro-m.ua/tovar/...&#10;https://makita.market/..." spellcheck="false"></textarea>
    <div class="actions">
      <button class="btn-primary" id="scanBtn">Зібрати ціни</button>
      <button class="btn-ghost" id="clearBtn">Очистити</button>
      <span class="hint">До 30 посилань за раз. Список зберігається у браузері.</span>
    </div>
  </div>

  <p id="status"></p>

  <section id="results">
    <div class="results-head">
      <h2>Результати</h2>
      <button class="btn-ghost" id="exportBtn">Завантажити CSV (Excel)</button>
    </div>
    <div class="table-scroll">
      <table id="resultsTable">
        <thead>
          <tr>
            <th>Магазин</th>
            <th>Товар</th>
            <th>Ціна</th>
            <th>Різниця з мін.</th>
            <th>Наявність</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>
  </section>

  <footer>Дані збираються з відкритих сторінок магазинів у момент запиту. Якщо магазин не віддає ціну — він, ймовірно, блокує автоматичні запити.</footer>
</div>

<script>
const $links  = document.getElementById('links');
const $status = document.getElementById('status');
const $scan   = document.getElementById('scanBtn');
const $clear  = document.getElementById('clearBtn');
const $export = document.getElementById('exportBtn');
const $results= document.getElementById('results');
const $tbody  = document.querySelector('#resultsTable tbody');

let lastResults = [];

/* збереження списку лінків між сесіями */
$links.value = localStorage.getItem('priceRadarLinks') || '';
$links.addEventListener('input', () => localStorage.setItem('priceRadarLinks', $links.value));

const fmt = n => n == null ? '—' : new Intl.NumberFormat('uk-UA').format(n) + ' ₴';

function availabilityBadge(a){
  if(!a) return '<span class="badge warn">невідомо</span>';
  const low = a.toLowerCase();
  if(low.includes('в наявності') || low.includes('обмежена'))
    return `<span class="badge ok">${a}</span>`;
  if(low.includes('нема') || low.includes('очікується') || low.includes('знято'))
    return `<span class="badge bad">${a}</span>`;
  return `<span class="badge warn">${a}</span>`;
}

function render(results){
  lastResults = results;
  const priced = results.filter(r => r.price != null);
  const minPrice = priced.length ? Math.min(...priced.map(r => r.price)) : null;

  $tbody.innerHTML = results.map(r => {
    if(r.status !== 'ok' || r.price == null){
      return `<tr>
        <td class="store">${r.store}</td>
        <td class="name">${r.name ? r.name : '<span class="store">без назви</span>'}<br>
            <span class="err">${r.error || 'Ціну не знайдено'}</span></td>
        <td class="num">—</td><td>—</td><td>—</td>
      </tr>`;
    }
    const isBest = r.price === minPrice;
    const delta  = minPrice != null ? r.price - minPrice : null;
    return `<tr class="${isBest ? 'best-row' : ''}">
      <td class="store">${r.store}</td>
      <td class="name"><a href="${r.url}" target="_blank" rel="noopener">${r.name || r.url}</a></td>
      <td class="num">${fmt(r.price)}
          ${r.old_price ? `<span class="old">${fmt(r.old_price)}</span>` : ''}</td>
      <td class="num">${isBest
          ? '<span class="badge best">найдешевше</span>'
          : `+${fmt(delta)}<span class="delta">+${minPrice ? Math.round(delta/minPrice*100) : 0}%</span>`}</td>
      <td>${availabilityBadge(r.availability)}</td>
    </tr>`;
  }).join('');

  $results.style.display = 'block';
}

$scan.addEventListener('click', async () => {
  const urls = $links.value.split('\n').map(s => s.trim()).filter(Boolean);
  if(!urls.length){
    $status.textContent = 'Додайте хоча б одне посилання.';
    return;
  }
  $scan.disabled = true;
  $status.className = 'scanning';
  $status.textContent = `Сканую ${urls.length} ${urls.length === 1 ? 'сторінку' : 'сторінок'}…`;

  try{
    const resp = await fetch('/api/parse', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({urls})
    });
    const data = await resp.json();
    if(!resp.ok) throw new Error(data.error || 'Помилка сервера');
    render(data.results);
    const ok = data.results.filter(r => r.price != null).length;
    $status.className = '';
    $status.textContent = `Готово: ціни знайдено на ${ok} з ${data.results.length} сторінок.`;
  }catch(e){
    $status.className = '';
    $status.textContent = 'Не вдалося зібрати дані: ' + e.message;
  }finally{
    $scan.disabled = false;
  }
});

$clear.addEventListener('click', () => {
  $links.value = '';
  localStorage.removeItem('priceRadarLinks');
  $links.focus();
});

/* CSV з BOM — відкривається в Excel з кирилицею без проблем */
$export.addEventListener('click', () => {
  if(!lastResults.length) return;
  const head = ['Магазин','Товар','Ціна, грн','Стара ціна, грн','Наявність','Посилання','Дата збору'];
  const today = new Date().toLocaleDateString('uk-UA');
  const esc = v => `"${String(v ?? '').replace(/"/g,'""')}"`;
  const rows = lastResults.map(r => [
    r.store, r.name || '', r.price ?? '', r.old_price ?? '',
    r.availability || r.error || '', r.url, today
  ].map(esc).join(';'));
  const csv = '\uFEFF' + head.map(esc).join(';') + '\n' + rows.join('\n');
  const blob = new Blob([csv], {type:'text/csv;charset=utf-8'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `price-radar_${new Date().toISOString().slice(0,10)}.csv`;
  a.click();
  URL.revokeObjectURL(a.href);
});
</script>
</body>
</html>
