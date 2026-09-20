/* Cart: localStorage store + header badge + drawer + add-to-cart forms.
   Loaded on every page from Base.astro. The /sepet page adds the WhatsApp step on top. */

export interface Kalem { slug: string; ad: string; marka: string; boy: string; fiyat: number; adet: number; gorsel: string }
interface Depo { v: 1; kalemler: Kalem[] }

const ANAHTAR = 'ps6-sepet';
const MAX_ADET = 20;

export const tl = (n: number) => new Intl.NumberFormat('tr-TR', { maximumFractionDigits: 0 }).format(n) + ' ₺';

export function oku(): Kalem[] {
  try {
    const ham = localStorage.getItem(ANAHTAR);
    if (!ham) return [];
    const d = JSON.parse(ham) as Depo;
    return Array.isArray(d?.kalemler) ? d.kalemler : [];
  } catch { return []; }
}
function yaz(kalemler: Kalem[]) {
  try { localStorage.setItem(ANAHTAR, JSON.stringify({ v: 1, kalemler } satisfies Depo)); } catch {}
  document.dispatchEvent(new CustomEvent('sepet:degisti', { detail: { kalemler } }));
}
export const toplamAdet = (k = oku()) => k.reduce((t, x) => t + x.adet, 0);
export const toplamTutar = (k = oku()) => k.reduce((t, x) => t + x.adet * x.fiyat, 0);

export function ekle(yeni: Omit<Kalem, 'adet'>, adet = 1) {
  const k = oku();
  const i = k.findIndex((x) => x.slug === yeni.slug && x.boy === yeni.boy);
  if (i >= 0) k[i].adet = Math.min(MAX_ADET, k[i].adet + adet);
  else k.push({ ...yeni, adet: Math.min(MAX_ADET, adet) });
  yaz(k);
}
export function adetAyarla(slug: string, boy: string, adet: number) {
  let k = oku();
  const i = k.findIndex((x) => x.slug === slug && x.boy === boy);
  if (i < 0) return;
  if (adet <= 0) k.splice(i, 1); else k[i].adet = Math.min(MAX_ADET, adet);
  yaz(k);
}
export function temizle() { yaz([]); }

/* ---------- order history (this device only) ---------- */
export interface Siparis { no: string; tarih: string; kalemler: Kalem[]; toplam: number; duzenli?: string; mesaj: string }
const SIPARIS_ANAHTAR = 'ps6-siparisler';
export function siparisler(): Siparis[] {
  try { const d = JSON.parse(localStorage.getItem(SIPARIS_ANAHTAR) || '[]'); return Array.isArray(d) ? d : []; } catch { return []; }
}
export function siparisKaydet(s: Siparis) {
  const liste = [s, ...siparisler().filter((x) => x.no !== s.no)].slice(0, 20);
  try { localStorage.setItem(SIPARIS_ANAHTAR, JSON.stringify(liste)); } catch {}
}
export function siparisSil(no: string) {
  try { localStorage.setItem(SIPARIS_ANAHTAR, JSON.stringify(siparisler().filter((x) => x.no !== no))); } catch {}
}

/* ---------- UI ---------- */

function rozetGuncelle() {
  const n = toplamAdet();
  document.querySelectorAll<HTMLElement>('[data-sepet-sayi]').forEach((el) => {
    el.textContent = String(n);
    el.hidden = n === 0;
  });
  document.querySelectorAll<HTMLElement>('[data-sepet-cubuk]').forEach((el) => { el.hidden = n === 0; });
}

/** Renders the shared line-item list used by the drawer and the /sepet page. */
export function kalemleriCiz(kok: HTMLElement, secenek: { duzenlenebilir: boolean }) {
  const k = oku();
  const bos = kok.querySelector<HTMLElement>('[data-sepet-bos]');
  const liste = kok.querySelector<HTMLElement>('[data-sepet-liste]');
  const dolu = kok.querySelector<HTMLElement>('[data-sepet-dolu]');
  if (!liste) return;
  if (bos) bos.hidden = k.length > 0;
  if (dolu) dolu.hidden = k.length === 0;
  liste.innerHTML = k.map((x) => `
    <li class="kalem" data-slug="${x.slug}" data-boy="${x.boy}">
      <a class="kalem__gorsel" href="/urun/${x.slug}"><img src="${x.gorsel}" alt="" width="72" height="72" loading="lazy"></a>
      <div class="kalem__bilgi">
        <span class="kalem__marka">${x.marka}</span>
        <a class="kalem__ad" href="/urun/${x.slug}">${x.ad}</a>
        <span class="kalem__boy">${x.boy} · ${tl(x.fiyat)}</span>
      </div>
      <div class="kalem__sag">
        ${secenek.duzenlenebilir ? `
        <div class="adet" role="group" aria-label="Adet">
          <button type="button" class="adet__btn" data-adet="-1" aria-label="Azalt">−</button>
          <span class="adet__sayi" aria-live="polite">${x.adet}</span>
          <button type="button" class="adet__btn" data-adet="1" aria-label="Artır">+</button>
        </div>` : `<span class="kalem__adet">${x.adet} adet</span>`}
        <strong class="kalem__tutar">${tl(x.adet * x.fiyat)}</strong>
        ${secenek.duzenlenebilir ? `<button type="button" class="kalem__sil" data-sil aria-label="Sepetten çıkar">Çıkar</button>` : ''}
      </div>
    </li>`).join('');
  kok.querySelectorAll<HTMLElement>('[data-sepet-toplam]').forEach((el) => { el.textContent = tl(toplamTutar(k)); });
  kok.querySelectorAll<HTMLElement>('[data-sepet-adet]').forEach((el) => { el.textContent = String(toplamAdet(k)); });
}

export function kalemOlaylari(kok: HTMLElement) {
  kok.addEventListener('click', (e) => {
    const t = e.target as HTMLElement;
    const li = t.closest<HTMLElement>('.kalem');
    if (!li) return;
    const { slug, boy } = li.dataset;
    if (!slug || !boy) return;
    const d = t.closest<HTMLElement>('[data-adet]');
    if (d) {
      const mevcut = oku().find((x) => x.slug === slug && x.boy === boy)?.adet ?? 0;
      adetAyarla(slug, boy, mevcut + Number(d.dataset.adet));
    } else if (t.closest('[data-sil]')) {
      adetAyarla(slug, boy, 0);
    }
  });
}

function cekmece() {
  const dlg = document.getElementById('sepet-cekmece') as HTMLDialogElement | null;
  if (!dlg) return;
  const ac = () => {
    kalemleriCiz(dlg, { duzenlenebilir: true });
    const g = dlg.querySelector<HTMLElement>('[data-sepet-gecmis]'); if (g) g.hidden = siparisler().length === 0;
    dlg.showModal(); document.documentElement.classList.add('kilit');
  };
  const kapat = () => { dlg.classList.add('kapaniyor'); setTimeout(() => { dlg.close(); dlg.classList.remove('kapaniyor'); }, 200); };
  document.querySelectorAll('[data-sepet-ac]').forEach((b) => b.addEventListener('click', (e) => { e.preventDefault(); ac(); }));
  dlg.querySelectorAll('[data-sepet-kapat]').forEach((b) => b.addEventListener('click', kapat));
  dlg.addEventListener('click', (e) => { if (e.target === dlg) kapat(); });
  dlg.addEventListener('cancel', (e) => { e.preventDefault(); kapat(); });
  dlg.addEventListener('close', () => document.documentElement.classList.remove('kilit'));
  kalemOlaylari(dlg);
  document.addEventListener('sepet:degisti', () => { if (dlg.open) kalemleriCiz(dlg, { duzenlenebilir: true }); });
  (window as any).__sepetAc = ac;
}

/** <form data-sepete-ekle> with inputs: slug, ad, marka, gorsel, boy (value "boy|fiyat"), adet */
function formlar() {
  document.addEventListener('submit', (e) => {
    const f = e.target as HTMLFormElement;
    if (!f.matches('[data-sepete-ekle]')) return;
    e.preventDefault();
    const fd = new FormData(f);
    const [boy, fiyat] = String(fd.get('boy') || '').split('|');
    if (!boy || !fiyat) return;
    ekle({
      slug: String(fd.get('slug')), ad: String(fd.get('ad')), marka: String(fd.get('marka')),
      gorsel: String(fd.get('gorsel')), boy, fiyat: Number(fiyat),
    }, Math.max(1, Number(fd.get('adet') || 1)));
    const btn = f.querySelector<HTMLButtonElement>('button[type="submit"]');
    if (btn) {
      btn.classList.add('eklendi'); btn.disabled = true;
      setTimeout(() => { btn.classList.remove('eklendi'); btn.disabled = false; }, 900);
    }
    if (f.dataset.sepeteEkle === 'ac') (window as any).__sepetAc?.();
    else tost(`Sepete eklendi (${boy})`);
  });
}

/** Size <select> inside a card or the product page updates the price shown next to it. */
function boySecimi() {
  document.addEventListener('change', (e) => {
    const el = e.target as HTMLInputElement | HTMLSelectElement;
    if (!el.matches('[data-boy-sec]')) return;
    const kok = el.closest('form') || document;
    const g = kok.querySelector<HTMLElement>('[data-fiyat-goster]');
    const src = el instanceof HTMLSelectElement ? el.selectedOptions[0] : el;
    const f = src?.dataset.fiyat;
    if (g && f) g.textContent = f;
    const eski = kok.querySelector<HTMLElement>('[data-eski-goster]');
    if (eski) { eski.textContent = src?.dataset.eski || ''; eski.hidden = !src?.dataset.eski; }
  });
}

/** Bottom toast after "Sepete ekle" + a bump on the header badge. */
let tostZaman = 0;
function tost(metin: string) {
  let el = document.querySelector<HTMLElement>('.tost');
  if (!el) {
    el = document.createElement('div'); el.className = 'tost'; el.setAttribute('role', 'status');
    document.body.appendChild(el);
  }
  el.innerHTML = `<svg class="ikon" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M232.49 80.49l-128 128a12 12 0 0 1-17 0l-56-56a12 12 0 1 1 17-17L96 183 215.51 63.51a12 12 0 0 1 17 17Z"/></svg><span>${metin}</span><a href="/sepet">Sepete git</a>`;
  requestAnimationFrame(() => el!.classList.add('acik'));
  clearTimeout(tostZaman);
  tostZaman = window.setTimeout(() => el!.classList.remove('acik'), 2600);
  document.querySelectorAll<HTMLElement>('[data-sepet-sayi]').forEach((r) => {
    r.classList.remove('rozet-zipla'); void r.offsetWidth; r.classList.add('rozet-zipla');
  });
}

export function baslat() {
  if ((document.documentElement as any).__sepet) return;
  (document.documentElement as any).__sepet = true;
  rozetGuncelle();
  document.addEventListener('sepet:degisti', rozetGuncelle);
  window.addEventListener('storage', (e) => { if (e.key === ANAHTAR) rozetGuncelle(); });
  cekmece();
  formlar();
  boySecimi();
}
