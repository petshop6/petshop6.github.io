import type { ImageMetadata } from 'astro';
import ham from '../content/urunler.json';
import { markaSlug, type Kategori, type MarkaSlug, type Tur } from './site';

export interface Secenek { boy: string }
export interface Urun {
  slug: string;
  ad: string;
  marka: string;
  markaSlug: MarkaSlug;
  tur: Tur;
  kategori: Kategori;
  etiketler: string[];
  aciklama: string;
  secenekler: Secenek[];
  gorsel: ImageMetadata;
  kaynak: string;
  oneCikan: boolean;
  /** false = "rafta yok": no add button, WhatsApp ask instead */
  stok: boolean;
}

const gorseller = import.meta.glob<{ default: ImageMetadata }>('/src/assets/urunler/*.{png,jpg}', { eager: true });

function gorselBul(dosya: string): ImageMetadata {
  const hit = Object.entries(gorseller).find(([p]) => p.endsWith('/' + dosya));
  if (!hit) throw new Error(`Görsel bulunamadı: ${dosya}`);
  return hit[1].default;
}

export const urunler: Urun[] = (ham as any[]).map((u) => ({
  slug: u.slug,
  ad: u.ad,
  marka: u.marka,
  markaSlug: markaSlug(u.marka),
  tur: u.tur,
  kategori: u.kategori,
  etiketler: u.etiketler,
  aciklama: u.aciklama,
  // price fields stay in urunler.json but never reach the browser: the shop quotes on WhatsApp
  secenekler: u.secenekler.map((s: { boy: string }) => ({ boy: s.boy })),
  gorsel: gorselBul(u.gorsel),
  kaynak: u.kaynak,
  oneCikan: !!u.oneCikan,
  stok: u.stok !== false,
}));

export const urunBul = (slug: string) => urunler.find((u) => u.slug === slug);
export const oneCikanlar = urunler.filter((u) => u.oneCikan);
