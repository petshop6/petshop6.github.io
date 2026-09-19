/* Header search: fetches /urunler.json once, shows up to 6 matches under the input. */
interface Kayit { slug: string; ad: string; marka: string; tur: string; kategori: string; etiketler: string[]; baslangic: number; gorsel: string }
let veri: Kayit[] | null = null;
const tl = (n: number) => new Intl.NumberFormat('tr-TR', { maximumFractionDigits: 0 }).format(n) + ' ₺';

const kucult = (s: string) => s.toLocaleLowerCase('tr-TR').replace(/[̇]/g, '');
export function eslesir(k: Kayit, q: string) {
  const h = kucult(`${k.marka} ${k.ad} ${k.etiketler.join(' ')} ${k.tur === 'kedi' ? 'kedi' : 'köpek'} ${k.kategori.replace('-', ' ')}`);
  return kucult(q).split(/\s+/).filter(Boolean).every((p) => h.includes(p));
}

export function baslat() {
  const form = document.querySelector<HTMLFormElement>('[data-ara]');
  if (!form || form.dataset.init) return;
  form.dataset.init = '1';
  const giris = form.querySelector<HTMLInputElement>('input')!;
  const kutu = form.querySelector<HTMLElement>('[data-ara-sonuc]')!;
  let zaman = 0;

  async function yukle() {
    if (veri) return veri;
    const r = await fetch('/urunler.json');
    veri = (await r.json()) as Kayit[];
    return veri;
  }
  async function ciz() {
    const q = giris.value.trim();
    if (q.length < 2) { kutu.hidden = true; kutu.innerHTML = ''; return; }
    const v = await yukle();
    const hits = v.filter((k) => eslesir(k, q)).slice(0, 6);
    kutu.innerHTML = hits.length
      ? hits.map((k) => `<a class="ara__satir" href="/urun/${k.slug}"><img src="${k.gorsel}" alt="" width="40" height="40"><span><small>${k.marka}</small>${k.ad}</span><b>${tl(k.baslangic)}</b></a>`).join('') +
        `<a class="ara__tum" href="/urunler?q=${encodeURIComponent(q)}">Tüm sonuçlar</a>`
      : `<p class="ara__yok">"${q}" için sonuç yok. <a href="https://wa.me/905442131332?text=${encodeURIComponent('Merhaba, ' + q + ' var mı?')}" target="_blank" rel="noopener">WhatsApp'tan sorun</a></p>`;
    kutu.hidden = false;
  }
  giris.addEventListener('input', () => { clearTimeout(zaman); zaman = window.setTimeout(ciz, 120); });
  giris.addEventListener('focus', () => { if (giris.value.trim().length >= 2) ciz(); });
  document.addEventListener('click', (e) => { if (!form.contains(e.target as Node)) kutu.hidden = true; });
  giris.addEventListener('keydown', (e) => { if (e.key === 'Escape') kutu.hidden = true; });
}
