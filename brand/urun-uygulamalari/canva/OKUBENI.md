# Ürün uygulamaları · Canva sürümü

Logonun kartvizit, anahtarlık, kalem ve masa takvimi üzerindeki kullanımı.
Bu klasör, `../cikti/` içindeki ilk (elle çizilmiş) sürümün yerine geçer.

**Dosya:** `PetShop6-Urun-Uygulamalari-Canva.pdf` — A4 yatay, 5 sayfa, 297 × 210 mm.
Her sayfanın JPEG'i de yanında (2246 × 1588 px).
Düzenlenebilir hâli Canva hesabınızda duruyor; bağlantı repoya konmadı, çünkü repo herkese açık.

| Sayfa | İçerik |
| --- | --- |
| 1 | Kapak |
| 2 | **Kartvizit** · 85 × 55 mm |
| 3 | **Anahtarlık** · 50 × 30 mm |
| 4 | **Kalem** · gövdeye yazı baskısı |
| 5 | **Masa takvimi** · 21 × 15 cm, Ocak 2027 |

## Nasıl yapıldı

1. Ürün fotoğrafları Canva'nın görsel üretimiyle **boş** olarak üretildi — üzerlerinde yazı,
   logo ya da baskı yok. Hepsi tepeden/karşıdan, perspektifsiz çekim istendi ki logo düz
   yerleşsin.
2. Logo bu fotoğrafların üzerine olduğu gibi kondu
   (`../../logo-yeni/web/petshop6-logo-seffaf-1200.png`). Yapay zekâya logo **çizdirilmedi**;
   tasarıma dokunulmadı. Kalemde gövde ince olduğu için logonun altındaki "PET SHOP 6" şeridi
   ayrı kesilip kullanıldı (`kaynak/artwork-wordmark.png`).
3. Sayfa yazıları ve takvim tablosu şeffaf PNG olarak üretilip yerleştirildi:
   `kaynak/yazi.py` (kapak ve sayfa etiketleri), `kaynak/hazirla.py` (Ocak 2027 takvimi ve
   yazı şeridi). Yazı tipleri Futura + Avenir Next. Canva bağlantısı üzerinden punto
   ayarlanamadığı için yazılar metin kutusu yerine görsel olarak konuldu.

Takvimin ayını değiştirmek için `kaynak/hazirla.py` içinde `takvim(2027, 1)` satırını
düzenleyip `python3 hazirla.py` çalıştırın, çıkan PNG'yi Canva'da eskisinin yerine koyun.

## Matbaaya verirken

- Bu sayfalar sunum içindir, **baskı dosyası değildir.** Matbaa taşma payı (bleed), kesim
  çizgisi ve CMYK/Pantone ister.
- Altın için yaldız (folyo) sorun. Ekrandaki altın bir gradyandır; düz CMYK basıldığında sönük
  çıkar.
- Anahtarlıkta siyah eloksal alüminyuma lazer gravür **gümüş** çıkar. Altın isteniyorsa tampon
  baskı ya da altın folyo sorun.
- Ürün görselleri temsilidir; üretici kendi kalıbına göre yerleşim isteyecektir.
