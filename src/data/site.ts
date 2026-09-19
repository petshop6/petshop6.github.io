import ayarlar from '../content/ayarlar.json';

export const site = ayarlar;

export const turler = {
  kedi: { ad: 'Kedi', tekil: 'kedi', baslik: 'Kedi ürünleri' },
  kopek: { ad: 'Köpek', tekil: 'köpek', baslik: 'Köpek ürünleri' },
} as const;
export type Tur = keyof typeof turler;

export const kategoriler = {
  'kuru-mama': { ad: 'Kuru Mama' },
  'yas-mama': { ad: 'Yaş Mama' },
  odul: { ad: 'Ödül Maması' },
  'kedi-kumu': { ad: 'Kedi Kumu' },
} as const;
export type Kategori = keyof typeof kategoriler;

export const markalar = {
  'pro-plan': { ad: 'Pro Plan' },
  reflex: { ad: 'Reflex' },
  'reflex-plus': { ad: 'Reflex Plus' },
  advance: { ad: 'Advance' },
} as const;
export type MarkaSlug = keyof typeof markalar;

export function markaSlug(ad: string): MarkaSlug {
  const s = ad.toLowerCase().replace(/\s+/g, '-') as MarkaSlug;
  if (!(s in markalar)) throw new Error(`Bilinmeyen marka: ${ad}`);
  return s;
}

/** 1090 -> "1.090 ₺" */
export function fiyat(n: number): string {
  return new Intl.NumberFormat('tr-TR', { maximumFractionDigits: 0 }).format(n) + ' ₺';
}

export const whatsappUrl = (metin?: string) =>
  `https://wa.me/${site.whatsapp}` + (metin ? `?text=${encodeURIComponent(metin)}` : '');
