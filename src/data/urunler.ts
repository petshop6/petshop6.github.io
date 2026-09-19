import type { ImageMetadata } from 'astro';
import ham from '../content/urunler.json';
import { markaSlug, type Kategori, type MarkaSlug, type Tur } from './site';

export interface Secenek { boy: string; fiyat: number }
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
  /** lowest price across sizes */
  baslangic: number;
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
  secenekler: u.secenekler,
  gorsel: gorselBul(u.gorsel),
  kaynak: u.kaynak,
  oneCikan: !!u.oneCikan,
  baslangic: Math.min(...u.secenekler.map((s: Secenek) => s.fiyat)),
}));

export const urunBul = (slug: string) => urunler.find((u) => u.slug === slug);
export const oneCikanlar = urunler.filter((u) => u.oneCikan);
