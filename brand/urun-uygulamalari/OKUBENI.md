# Ürün uygulamaları

Logonun müşteriye verilecek ürünler üzerindeki kullanımı. Dosya: `cikti/PetShop6-Urun-Uygulamalari.pdf`
(A4 yatay, 4 sayfa, 250 dpi) ve her sayfanın PNG'si.

| Sayfa | İçerik |
| --- | --- |
| 1 | Kapak |
| 2 | **Kartvizit** · 85 × 55 mm, ön yüz mürekkep + logo, arka yüz kemik + iletişim |
| 3 | **Anahtarlık ve kalem** · anahtarlık görseli mağazanın kendi fotoğrafı (3 kat büyütülmüş), kalem çizim |
| 4 | **Masa takvimi** · 21 × 15 cm, Ocak 2027, spiralli, pazar günleri altın |

Hepsi `mockup.py` ile üretiliyor: `python3 mockup.py`. Logo dosyaları `../logo-yeni/` içinden okunur,
yazı tipleri sistemden gelir (başlık Futura — logodaki geometrik yazıya en yakın sistem fontu, metin
Avenir Next). Takvimin ayı/yılı `takvim_ciz(yil, ay)` ile değişir.

**Matbaaya verirken:** bu sayfalar sunum içindir, baskı dosyası değildir. Matbaa taşma payı (bleed),
kesim çizgisi ve CMYK/Pantone ister; altın için yaldız (folyo) sorun — ekrandaki altın gradyanı
basıldığında sönük kalır. Anahtarlık ve kalem görselleri temsilidir; üretici kendi kalıbına göre
yerleşim isteyecektir.
