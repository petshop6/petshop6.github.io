# Görsel kaynakları

Ürün görselleri markaların kendi Türkiye sitelerindeki ambalaj görselleridir (packshot). Her ürünün
`src/content/urunler.json` kaydındaki `kaynak` alanı, görselin alındığı ürün sayfasını gösterir.
Mağaza kendi çekimlerini gönderdiğinde `src/assets/urunler/<slug>.png` dosyasını değiştirmek yeterlidir.

| Marka | Site | Ürün sayısı |
| --- | --- | --- |
| Reflex, Reflex Plus (Lider Pet Food) | reflexmama.com | 38 |
| Pro Plan (Purina Türkiye) | purina.com.tr | 11 |
| Advance (Affinity) | advance-affinity.com/tr | 9 |

`tools/katalog.py` görselleri indirir ve ürün listesini yazar; `tools/seffaf.py` beyaz zeminli
görselleri şeffaf PNG'ye çevirir; `tools/og.py` paylaşım kartlarını (`public/og/*.jpg`) üretir.

Mağaza fotoğrafları (`src/assets/dukkan/`): Yandex Haritalar'daki işletme fotoğrafları, 2024. Mağaza
kendi fotoğraflarını gönderdiğinde değiştirilecek.

İkonlar: Phosphor Icons (MIT). Yazı tipleri: Archivo (OFL), Hanken Grotesk (OFL), Fontsource paketleri.
