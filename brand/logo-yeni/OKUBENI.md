# Pet Shop 6 · logo dosyaları

Hüseyin'in 30 Eylül 2026'da gönderdiği logonun **tasarımına dokunulmadan** hazırlanmış
yüksek çözünürlüklü sürümleri. Orijinal dosya `kaynak/orijinal-gonderilen.jpg` (1280×853 JPEG;
logo alanı yalnızca 556×522 piksel).

## Ne yapıldı

1. **JPEG bozulmaları temizlendi.** Siyah zemindeki blok/kar gürültüsü kaldırıldı, işaretin
   çevresindeki altın hâle korundu.
2. **4 kat büyütüldü** (iterative back-projection). Bu yöntem sonucu her adımda küçültüp
   orijinalle karşılaştırır; yani detay uydurmaz, var olanı keskinleştirir.
   Kontrol: küçültülüp orijinalle karşılaştırıldığında PSNR 29,6 dB, altın rengi farkı 2,3/255.
3. **Çerçeve dengelendi.** Çizim ortalandı, kenar boşlukları eşitlendi. Renk, biçim, yazı
   tipi, hiçbir öğe değiştirilmedi.

## Dosyalar

| Dosya | Ne için |
| --- | --- |
| `PetShop6-Logo.pdf` | **Ana dosya.** Baskı için; 219×208 mm @ 300 dpi, kayıpsız. |
| `PetShop6-Logo.png` | 2584×2454 px, siyah zemin. |
| `PetShop6-Logo-seffaf.pdf/.png` | Zemini şeffaf. **Yalnızca koyu zeminlerde** kullanın: tasarımdaki kedi ve köpek gövdeleri siyahtır, açık zeminde boş görünür. |
| `PetShop6-Amblem.pdf/.png` | Yazısız, sadece 6 + kedi-köpek işareti. 155×168 mm @ 300 dpi. |
| `PetShop6-Amblem-seffaf.pdf/.png` | Aynısı, şeffaf zeminli. |
| `web/petshop6-logo-1200.png` | Site, sosyal medya, e-posta imzası. |
| `web/petshop6-amblem-512.png`, `-180.png` | Profil resmi, favicon, uygulama simgesi. |

PDF'ler 300 dpi'de yukarıdaki ölçülerde açılır; matbaa büyütüp küçültebilir. A4'e sığar.

## Baskıya verirken

- Tabela, kupa, anahtarlık gibi işlerde matbaa çoğu zaman **vektör (AI/EPS/SVG)** ister. Elimizdeki
  logo çizilmiş bir vektör değil, **render edilmiş bir görsel**: metalik parlaklık ve gölgeler
  pikselden geliyor. Vektöre çevirmek bu parlaklığı düzleştirir, yani tasarımı değiştirir —
  bu yüzden yapılmadı. Matbaa vektör şart koşarsa ayrıca çizilmesi gerekir.
- Altın, ekranda gördüğünüz gradyandır. Gerçek baskıda altın yaldız (folyo) ya da Pantone
  metalik mürekkep çok daha iyi durur; matbaaya "altın yaldız" olarak sorun.

## Yeniden üretmek

`kaynak/restore.py` + `kaynak/uret.py` (Python, OpenCV). `python3 uret.py` bütün dosyaları
yeniden üretir.
