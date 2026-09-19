import type { APIRoute } from 'astro';
import { getImage } from 'astro:assets';
import { urunler } from '../data/urunler';

/** Compact catalog for the header search and cart (name, price, small image). */
export const GET: APIRoute = async () => {
  const liste = await Promise.all(urunler.map(async (u) => {
    const img = await getImage({ src: u.gorsel, width: 160, height: 160, fit: 'contain', format: 'webp' });
    return { slug: u.slug, ad: u.ad, marka: u.marka, tur: u.tur, kategori: u.kategori, etiketler: u.etiketler, baslangic: u.baslangic, gorsel: img.src };
  }));
  return new Response(JSON.stringify(liste), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
};
