/* Catalog filters + sort + search query, all client-side over the server-rendered cards. */
import { eslesir } from './ara';

export function baslat() {
  const kok = document.querySelector<HTMLElement>('[data-katalog]');
  if (!kok || kok.dataset.init) return;
  kok.dataset.init = '1';
  const form = kok.querySelector<HTMLFormElement>('[data-filtre-form]')!;
  const izgara = kok.querySelector<HTMLElement>('[data-katalog-izgara]')!;
  const kartlar = Array.from(izgara.querySelectorAll<HTMLElement>('[data-urun]'));
  const sirala = kok.querySelector<HTMLSelectElement>('[data-sirala]')!;
  const bos = kok.querySelector<HTMLElement>('[data-katalog-bos]')!;
  const notu = kok.querySelector<HTMLElement>('[data-arama-notu]');
  const url = new URL(location.href);
  const q = (url.searchParams.get('q') || '').trim();
  const sira0 = kartlar.slice();

  // restore state from URL (?tur=kedi&marka=reflex,advance&sirala=fiyat-artan)
  for (const alan of ['tur', 'kategori', 'marka', 'etiket']) {
    const v = url.searchParams.get(alan);
    if (!v) continue;
    v.split(',').forEach((deger) => {
      const i = form.querySelector<HTMLInputElement>(`input[name="${alan}"][value="${CSS.escape(deger)}"]`);
      if (i) i.checked = true;
    });
  }
  const s0 = url.searchParams.get('sirala');
  if (s0 && [...sirala.options].some((o) => o.value === s0)) sirala.value = s0;

  function secili(alan: string) {
    return Array.from(form.querySelectorAll<HTMLInputElement>(`input[name="${alan}"]:checked`)).map((i) => i.value);
  }
  function uygula() {
    const f = { tur: secili('tur'), kategori: secili('kategori'), marka: secili('marka'), etiket: secili('etiket') };
    let n = 0;
    kartlar.forEach((k) => {
      const et = (k.dataset.etiket || '').split('|');
      let ok = (!f.tur.length || f.tur.includes(k.dataset.tur!))
        && (!f.kategori.length || f.kategori.includes(k.dataset.kategori!))
        && (!f.marka.length || f.marka.includes(k.dataset.marka!))
        && (!f.etiket.length || f.etiket.every((e) => et.includes(e)));
      if (ok && q) {
        ok = eslesir({ slug: '', ad: k.dataset.ad || '', marka: k.dataset.marka || '', tur: k.dataset.tur || '', kategori: k.dataset.kategori || '', etiketler: et, baslangic: 0, gorsel: '' }, q);
      }
      k.hidden = !ok;
      if (ok) n++;
    });
    kok!.querySelectorAll<HTMLElement>('[data-katalog-sayi]').forEach((el) => { el.textContent = String(n); });
    bos.hidden = n > 0;
    izgara.hidden = n === 0;
    if (notu) { notu.hidden = !q; notu.textContent = q ? `· "${q}" için` : ''; }

    // url
    const u = new URL(location.href);
    for (const alan of ['tur', 'kategori', 'marka', 'etiket'] as const) {
      if (f[alan].length) u.searchParams.set(alan, f[alan].join(',')); else u.searchParams.delete(alan);
    }
    if (sirala.value !== 'onerilen') u.searchParams.set('sirala', sirala.value); else u.searchParams.delete('sirala');
    history.replaceState(null, '', u);
  }
  function sirayaKoy() {
    const v = sirala.value;
    const liste = sira0.slice();
    const ad = (k: HTMLElement) => k.dataset.ad || '';
    const fi = (k: HTMLElement) => Number(k.dataset.fiyat || 0);
    if (v === 'fiyat-artan') liste.sort((a, b) => fi(a) - fi(b));
    else if (v === 'fiyat-azalan') liste.sort((a, b) => fi(b) - fi(a));
    else if (v === 'ad') liste.sort((a, b) => ad(a).localeCompare(ad(b), 'tr'));
    liste.forEach((k) => izgara.appendChild(k));
  }

  form.addEventListener('change', uygula);
  sirala.addEventListener('change', () => { sirayaKoy(); uygula(); });
  kok.querySelectorAll('[data-filtre-sifirla]').forEach((b) => b.addEventListener('click', () => {
    form.querySelectorAll<HTMLInputElement>('input:checked').forEach((i) => { i.checked = false; });
    uygula();
  }));
  kok.querySelectorAll('[data-filtre-ac]').forEach((b) => b.addEventListener('click', () => { kok.classList.add('filtre-acik'); document.documentElement.classList.add('kilit'); }));
  kok.querySelectorAll('[data-filtre-kapat]').forEach((b) => b.addEventListener('click', () => { kok.classList.remove('filtre-acik'); document.documentElement.classList.remove('kilit'); }));

  sirayaKoy();
  uygula();
}
