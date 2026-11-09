// The study's explorer (five sentiment readings) and the index chart's readout.
// data/sentiment.json is built from fear_greed_index.csv and output/sentiment_performance_metrics.csv.

const COLOUR = { 'Extreme Fear': 'var(--s-ef)', Fear: 'var(--s-f)', Neutral: 'var(--s-n)', Greed: 'var(--s-g)', 'Extreme Greed': 'var(--s-eg)' };
const RANGE = { 'Extreme Fear': '0 to 24', Fear: '25 to 44', Neutral: '45 to 54', Greed: '55 to 74', 'Extreme Greed': '75 to 100' };
const ORD = ['Highest', 'Second', 'Third', 'Fourth', 'Lowest'];
const $ = (id) => document.getElementById(id);
const money = (v) => (Math.abs(v) >= 1e6 ? `$${(v / 1e6).toFixed(Math.abs(v) >= 1e8 ? 1 : 2)}M` : `$${v.toLocaleString('en-US', { maximumFractionDigits: v < 100 ? 2 : 0, minimumFractionDigits: v < 100 ? 2 : 0 })}`);
const int = (v) => v.toLocaleString('en-US');

function rankText(values, name, low) {
  const sorted = Object.entries(values).sort((a, b) => (low ? a[1] - b[1] : b[1] - a[1]));
  const i = sorted.findIndex(([k]) => k === name);
  if (low) return i === 0 ? 'Smallest of the five' : `${ORD[i]} of the five`;
  return i === 0 ? 'Highest of the five' : i === 4 ? 'Lowest of the five' : `${ORD[i]} of the five`;
}

function explorer(data) {
  const list = $('sx-list');
  const m = data.metrics;
  const names = [...data.classes].reverse(); // Extreme Greed first
  const allFills = Object.values(m).reduce((s, x) => s + x.fills, 0);
  const pick = (key) => Object.fromEntries(Object.entries(m).map(([k, v]) => [k, v[key]]));
  const max = (key) => Math.max(...Object.values(m).map((v) => v[key]));

  list.innerHTML = names.map((n, i) => `<li class="ui-win__row${i === 0 ? ' is-sel' : ''}" data-row data-name="${n}" tabindex="0" role="button" aria-label="${n}: ${m[n].win_rate.toFixed(2)}% of fills in profit">`
    + `<span class="sdot" style="--c:${COLOUR[n]}" aria-hidden="true"></span>`
    + `<span class="ui-win__txt"><span class="ui-win__who">${n}</span><span class="ui-win__sub">${int(m[n].fills)} fills · ${data.days[n]} days · index ${RANGE[n]}</span></span>`
    + `<span class="ui-win__st">${m[n].win_rate.toFixed(2)}%</span></li>`).join('');

  const show = (n) => {
    const x = m[n];
    const c = COLOUR[n];
    $('sx-name').textContent = n;
    $('sx-days').textContent = `${data.days[n]} days · index ${RANGE[n]}`;
    const card = (label, value, w, note) => `<div class="mx__card"><span>${label}</span><b>${value}</b><i style="--w:${Math.round(w * 100)}%;--c:${c}"></i><small>${note}</small></div>`;
    $('sx-grid').innerHTML = [
      card('Closed in profit', `${x.win_rate.toFixed(2)}%`, x.win_rate / max('win_rate'), rankText(pick('win_rate'), n)),
      card('Fills', int(x.fills), x.fills / max('fills'), `${Math.round((x.fills / allFills) * 100)}% of all fills`),
      card('Total closed PnL', money(x.pnl_total), x.pnl_total / max('pnl_total'), rankText(pick('pnl_total'), n)),
      card('Closed PnL per fill', money(x.pnl_mean), x.pnl_mean / max('pnl_mean'), rankText(pick('pnl_mean'), n)),
      card('Average size', money(x.size_mean), x.size_mean / max('size_mean'), x.size_mean === Math.min(...Object.values(pick('size_mean'))) ? 'Smallest of the five' : rankText(pick('size_mean'), n)),
      card('Volume', money(x.size_total), x.size_total / max('size_total'), rankText(pick('size_total'), n)),
    ].join('');
  };
  const choose = (li) => {
    list.querySelectorAll('.is-sel').forEach((el) => el.classList.remove('is-sel'));
    li.classList.add('is-sel');
    show(li.dataset.name);
  };
  list.addEventListener('click', (e) => { const li = e.target.closest('[data-row]'); if (li) choose(li); });
  list.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    const li = e.target.closest('[data-row]');
    if (li) { e.preventDefault(); choose(li); }
  });
}

function chart(data) {
  const box = $('fgc');
  const svg = box.querySelector('svg');
  const tip = $('fgc-tip');
  const dot = $('fgc-dot');
  const pts = data.index;
  const t0 = Date.parse(pts[0][0]);
  const span = Date.parse(pts[pts.length - 1][0]) - t0;
  const fmt = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' });
  const hide = () => { tip.hidden = true; dot.hidden = true; };
  box.addEventListener('pointermove', (e) => {
    const r = svg.getBoundingClientRect();
    const f = (e.clientX - r.left) / r.width;
    if (f < 0 || f > 1) { hide(); return; }
    const t = t0 + f * span;
    let lo = 0;
    let hi = pts.length - 1;
    while (hi - lo > 1) { const mid = (lo + hi) >> 1; if (Date.parse(pts[mid][0]) < t) lo = mid; else hi = mid; }
    const p = Math.abs(Date.parse(pts[lo][0]) - t) < Math.abs(Date.parse(pts[hi][0]) - t) ? pts[lo] : pts[hi];
    const b = box.getBoundingClientRect();
    const x = r.left - b.left + ((Date.parse(p[0]) - t0) / span) * r.width;
    const y = r.top - b.top + (1 - p[1] / 100) * r.height;
    dot.style.left = `${x}px`; dot.style.top = `${y}px`;
    tip.style.left = `${Math.min(Math.max(x, 90), b.width - 90)}px`; tip.style.top = `${y}px`;
    tip.textContent = `${fmt.format(new Date(p[0]))} · ${p[1]}, ${p[2]}`;
    tip.hidden = false; dot.hidden = false;
  });
  box.addEventListener('pointerleave', hide);
}

fetch('data/sentiment.json')
  .then((r) => r.json())
  .then((data) => { explorer(data); chart(data); })
  .catch((err) => console.error('study: could not load data/sentiment.json', err));
