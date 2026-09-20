/* Header search: fetches /urunler.json once, shows up to 6 matches under the input.
   Matching folds Turkish letters (kopek = köpek, kisir = kısır), expands common synonyms and
   strips plural suffixes, so "proplan kisir somon" and "kediler için kum" both work. */
interface Kayit { slug: string; ad: string; marka: string; tur: string; kategori: string; etiketler: string[]; baslangic: number; gorsel: string; stok?: boolean; kampanya?: boolean }
let veri: Kayit[] | null = null;
const tl = (n: number) => new Intl.NumberFormat('tr-TR', { maximumFractionDigits: 0 }).format(n) + ' ₺';

const HARF: Record<string, string> = { ı: 'i', i̇: 'i', ş: 's', ğ: 'g', ç: 'c', ö: 'o', ü: 'u', â: 'a', î: 'i', û: 'u' };
/** lower-case + fold Turkish diacritics, so both sides compare on the same alphabet */
export const katla = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFC').replace(/[ışğçöüâîûi̇]/g, (c) => HARF[c] ?? c);

/** query-side synonyms, written folded */
const ES_ANLAM: Record<string, string[]> = {
  kisir: ['kisirlastirilmis'], kisirlastirilmis: ['kisirlastirilmis'], steril: ['kisirlastirilmis'], sterilised: ['kisirlastirilmis'], sterilized: ['kisirlastirilmis'], sterilize: ['kisirlastirilmis'],
  proplan: ['pro plan'], purina: ['pro plan'], reflexplus: ['reflex plus'], advanced: ['advance'],
  kitten: ['yavru'], puppy: ['yavru'], junior: ['yavru'], adult: ['yetiskin'], yetiskin: ['yetiskin'],
  senior: ['7+'], yasli: ['7+'],
  kum: ['kedi kumu'], kumu: ['kedi kumu'], topaklanan: ['topaklanan'], bentonit: ['kedi kumu'],
  konserve: ['konserve', 'yas mama'], pouch: ['pouch', 'yas mama'], yas: ['yas mama'], islak: ['yas mama'],
  kuru: ['kuru mama'], odul: ['odul'], treat: ['odul'], snack: ['odul'], cubuk: ['cubuk', 'meaty'], stick: ['cubuk'],
  dis: ['dis', 'denta'], diş: ['dis'], kemik: ['bisküvi', 'bones'],
  hassas: ['hassas sindirim'], sindirim: ['hassas sindirim'], sensitive: ['hassas sindirim', 'sensitive'],
  kucuk: ['kucuk irk'], mini: ['kucuk irk', 'mini'], orta: ['orta irk'], medium: ['orta irk', 'medium'], buyuk: ['buyuk irk'], large: ['buyuk irk', 'large'], maxi: ['buyuk irk', 'maxi'],
  somon: ['somon'], salmon: ['somon'], tavuk: ['tavuk'], chicken: ['tavuk'], kuzu: ['kuzu'], lamb: ['kuzu'], hindi: ['hindi'], turkey: ['hindi'], ton: ['ton bal'], tuna: ['ton bal'],
  indirim: ['kampanya'], indirimli: ['kampanya'], kampanya: ['kampanya'],
  cubugu: ['cubuk'], cubuklari: ['cubuk'], bisküvi: ['cookie', 'bones'], biskuvi: ['cookie', 'bones'],
};
/** words that carry no meaning for matching */
const DUR = new Set(['icin', 've', 'ile', 'mi', 'mi̇', 'var', 'olan', 'bir', 'en', 'iyi', 'ucuz', 'fiyat', 'mamasi', 'mama']);
/** strip plural / common suffixes so "kediler" and "mamalari" still hit "kedi" and "mama" */
const kok = (t: string) => t.replace(/(lari|leri|lar|ler|dan|den|lik|lık|si|sı)$/u, (m) => (t.length - m.length >= 3 ? '' : m));

function yiginOlustur(k: Kayit) {
  return katla(`${k.marka} ${k.ad} ${k.etiketler.join(' ')} ${k.tur === 'kedi' ? 'kedi' : 'köpek'} ${k.kategori.replace('-', ' ')} ${k.kampanya ? 'kampanya indirim' : ''}`);
}
export function eslesir(k: Kayit, q: string) {
  const h = yiginOlustur(k);
  const parcalar = katla(q).split(/\s+/).filter(Boolean);
  const anlamli = parcalar.filter((p) => !DUR.has(p) && !DUR.has(kok(p)));
  return (anlamli.length ? anlamli : parcalar).every((p) => {
    const adaylar = [p, kok(p), ...(ES_ANLAM[p] ?? []), ...(ES_ANLAM[kok(p)] ?? [])];
    return adaylar.some((a) => a && h.includes(a));
  });
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
      ? hits.map((k) => `<a class="ara__satir" href="/urun/${k.slug}"><img src="${k.gorsel}" alt="" width="40" height="40"><span><small>${k.marka}${k.stok === false ? ' · rafta yok' : ''}</small>${k.ad}</span><b>${tl(k.baslangic)}</b></a>`).join('') +
        `<a class="ara__tum" href="/urunler?q=${encodeURIComponent(q)}">Tüm sonuçlar</a>`
      : `<p class="ara__yok">"${q}" için sonuç yok. <a href="https://wa.me/905442131332?text=${encodeURIComponent('Merhaba, ' + q + ' var mı?')}" target="_blank" rel="noopener">WhatsApp'tan sorun</a></p>`;
    kutu.hidden = false;
  }
  giris.addEventListener('input', () => { clearTimeout(zaman); zaman = window.setTimeout(ciz, 120); });
  giris.addEventListener('focus', () => { if (giris.value.trim().length >= 2) ciz(); });
  document.addEventListener('click', (e) => { if (!form.contains(e.target as Node)) kutu.hidden = true; });
  giris.addEventListener('keydown', (e) => { if (e.key === 'Escape') kutu.hidden = true; });
}
