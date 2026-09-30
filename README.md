# Pet Shop 6 · petshop6-web

Bahçelievler'deki Pet Shop 6 için sipariş sitesi. Müşteri sepetini doldurur, adresini yazar,
"Siparişi WhatsApp'tan gönder" der; sipariş mesajı mağazanın WhatsApp hattında hazır açılır.
Sunucu, üyelik ve online ödeme yok: sepet ve adres tarayıcıda (localStorage) tutulur, ödeme kapıda.

Astro 7, statik çıktı. Node 22 (`~/.local/node22`) npm script'lerine gömülü.

**Yayın:** https://petshop6.github.io (GitHub Pages, repo `petshop6/petshop6.github.io`). `main`'e her
push `.github/workflows/deploy.yml` ile yayınlanır. Alan adı bağlanınca Settings → Pages'te custom
domain girin ve repo değişkeni `SITE_URL`'i o adrese ayarlayın.

```bash
npm run dev      # http://localhost:4328
npm run build    # dist/
npm run preview
```

## Mağazadan beklenenler (site yayına çıkmadan)

1. **Fiyat listesi.** `src/content/urunler.json` içindeki fiyatlar piyasa seviyesinde örnek
   değerlerdir. Gerçek fiyatlar girildikten sonra `src/content/ayarlar.json` içinde
   `"fiyatlarOrnek": false` yapın; sarı uyarı şeridi kalkar.
2. **WhatsApp numarası.** Tabeladaki 0544 213 13 32 kullanıldı (`ayarlar.json` → `whatsapp`).
   Farklı bir hat kullanılacaksa oradan değiştirin; tüm bağlantılar oradan beslenir.
3. **Teslimat bölgesi ve kuralları.** "Ankara içi ücretsiz" varsayıldı; minimum tutar yok.
   `ayarlar.json` → `teslimat` ve `/teslimat`, `/sss` sayfaları.
4. **Değişim/iade kuralı.** `/teslimat` sayfasında yalnızca "teslimatta kontrol edin, yanlış ürünü
   kuryeye geri verin" yazıyor; mağazanın kendi kuralı eklenecek.
5. **Fotoğraf.** Vitrin fotoğrafları geçici (bkz. KAYNAKLAR.md). Mağazanın kendi çekimleri gelince
   `src/assets/dukkan/` altındakiler değişecek.
6. **Ürün listesi.** 58 ürün: kedi/köpek kuru ve yaş mama, ödül, kedi kumu. Kuş, akvaryum,
   aksesuar kategorileri sitede yok; ana sayfa ve mağaza sayfası WhatsApp'a yönlendiriyor.
7. **Alan adı.** Instagram biyosundaki petshop6.com çözümlenmiyor ve kayıtlı görünmüyor; alınmalı.
   `astro.config.mjs` `SITE_URL` ile başka bir hosta da kurulabilir.

## Ürün ekleme / düzenleme

`src/content/urunler.json` bir dizi; her kayıt:

```json
{
  "id": "slug", "slug": "slug", "ad": "Ürün adı", "marka": "Reflex Plus",
  "tur": "kedi | kopek", "kategori": "kuru-mama | yas-mama | odul | kedi-kumu",
  "etiketler": ["yetişkin", "kısırlaştırılmış"], "aciklama": "Kısa, olgusal.",
  "secenekler": [{ "boy": "1,5 kg", "fiyat": 390 }, { "boy": "15 kg", "fiyat": 2490, "eskiFiyat": 2690 }],
  "gorsel": "slug.png", "kaynak": "https://...", "oneCikan": false, "stok": true
}
```

- **Kampanya:** bir boya `eskiFiyat` yazın; kart ve ürün sayfası üstü çizili eski fiyatı ve kırmızı yeni
  fiyatı gösterir, o boy varsayılan seçili gelir, ana sayfada "Kampanya" şeridi ve katalogda
  "Kampanyalı" filtresi kendiliğinden açılır. Şu an iki üründe **örnek** kampanya var
  (Reflex Crunchy Bubble Kısır Somonlu 15 kg, Reflex Aktif Karbonlu kum); gerçek liste gelince silin.
- **Rafta yok:** `"stok": false` yazın; sepete ekle yerine "Gelince haber ver" WhatsApp bağlantısı
  çıkar, görsel soluklaşır, "Rafta yok" etiketi gelir. Örnek: Reflex Plus Tavuklu Mini Yavru.
- **Düzenli sipariş:** sepet sayfasındaki "Bunu düzenli getirin" kutusu ve aralık seçimi WhatsApp
  mesajına `Düzenli sipariş: 4 haftada bir` satırını ekler. Takip mağazada; site bir şey göndermez.
- **Siparişlerim** (`/siparislerim`): gönderilen siparişler cihazda (localStorage, son 20) tutulur;
  "Tekrar sipariş ver" sepeti aynı ürünlerle doldurur, "Mesajı WhatsApp'ta aç" aynı metni yeniden açar.

Görsel `src/assets/urunler/` altına konur (şeffaf PNG tercih). Yeni marka için
`src/data/site.ts` → `markalar`. `tools/katalog.py` bu dosyayı sıfırdan üretir; elle düzenlenen
listeyi ezmemek için önce oradaki listeyi güncelleyin.

## Tasarım dili

Logo altın-siyah olduğu için site de o dünyada: **mürekkep zemin (#0e0d0b), altın vurgu (#c9a24d),
kemik yazı (#f4f1ea)**. Kırmızı bırakıldı. Yüzeyler `--zemin` (sayfa), `--yuzey` (kart, bölüm),
`--yuzey-2` (girdi, öne çıkan panel); ayırıcı olarak gölge değil `--cizgi` saç teli çizgiler.
Tipografi **Jost** (başlık ve kapitaller; logodaki geometrik yazının akrabası) + **Schibsted Grotesk**
(okuma). İtalik yüklenmiyor. Birincil buton dolu altın, ikincil buton saç teli çerçeve; ürün
kartlarındaki "Sepete ekle" hayalet buton, üzerine gelince altına dönüyor — böylece ızgara altın
yağmuruna dönmüyor. Bütün renk kararları `src/styles/global.css` içindeki `:root` bloğunda.

**İki tema.** Koyu varsayılan; üst bardaki güneş/ay düğmesi (ve mobil menüdeki buton) açık temaya geçirir,
seçim `localStorage` (`ps6-tema`) içinde saklanır ve `Base.astro` içindeki satır içi betikle sayfa boyanmadan
uygulanır, böylece geçiş sırasında yanıp sönme olmaz. İşletim sistemi tercihi takip edilmez; seçim kullanıcınındır.
Açık tema `:root[data-tema="acik"]` altında sadece jetonları değiştirir ve **siyah-beyaz**tır: beyaz
sayfa, siyah üst bar (kategori satırı dahil), siyah yazı, siyah butonlar; altın yalnızca logoda kalır.
Üst barın kendi jetonları var (`--ust-zemin`, `--ust-metin`, `--ust-metin-2`, `--ust-cizgi`, `--ust-vurgu`),
böylece bar sayfadan bağımsız koyu kalabiliyor. Roller ayrı tutulur: `--altin` dolgu, `--altin-hover` dolgu vurgusu, `--altin-yazi` yazı
olarak altın; açık temada üçü de siyaha döner. Bunların dışında **iki temada da altın kalan** iki jeton var:
`--altin-detay` (siyah barın altındaki ince çizgi, sepet rozeti, aktif menü, ikonlar, seçili beden, odak halkası)
ve `--altin-detay-yazi` (Kampanya etiketi, indirimli fiyat, küçük vurgu bağlantıları; açık temada `#8a6a22`).
Böylece taban siyah-beyaz kalırken logo sayfada yankılanıyor. Logo altın-siyah olduğu için koyu
zemine ihtiyaç duyar: üst bar ve altbilgi her iki temada da siyah, mobil menü başlığı açık temada koyu şerit.

## Logo

Mağazanın 30 Eylül 2026'da verdiği altın logo kullanılıyor. Baskıya hazır dosyalar ve ne yapıldığı:
`brand/logo-yeni/` (bkz. `OKUBENI.md`). Sitedeki kaynaklar `src/assets/logo/amblem.png` (üst bar) ve
`logo.png` (altbilgi, mobil menü); ikisi de şeffaf zeminli, **koyu zemin için**. Bu yüzden üst bar ve
mobil menü başlığı siyah (`--murekkep`); kırmızı vurgu rengi olarak kaldı (butonlar, sepet rozeti,
Kampanya bağlantısı). Favicon ve uygulama simgesi `public/favicon-32.png`, `favicon-192.png`,
`apple-touch-icon.png` — amblemden, siyah zeminli üretildi.

## Rehber

`src/content/rehber/*.md`: mağazanın kendi Instagram paylaşımlarından dört bakım yazısı (2017), metin
aynen, yalnızca yazım düzeltmeleriyle; her yazının altında kaynak bağlantısı ve "veteriner tavsiyesi
değildir" notu var. Yeni yazı için aynı ön bilgi alanlarıyla (baslik, ozet, tarih, kaynak, gorsel,
gorselAlt, etiket) bir `.md` dosyası eklemek yeterli. "Hayvan beslemenin faydaları" gönderisi sağlık
iddiaları içerdiği için alınmadı.

## Arama

`src/scripts/ara.ts` Türkçe harfleri katlar (kopek = köpek, kisir = kısır), eş anlamlıları açar
(proplan, sterilised, kitten, kum, indirim …), çoğul eklerini atar ve "için/ve/mama" gibi dolgu
sözcüklerini yok sayar. Katalog sayfasındaki `?q=` de aynı eşleştirmeyi kullanır.

## Yapı

- `src/pages/` sayfalar: `/`, `/urunler`, `/kedi`, `/kopek`, `/kedi/<kategori>`, `/kopek/<kategori>`,
  `/marka/<marka>`, `/urun/<slug>`, `/sepet`, `/magaza`, `/teslimat`, `/sss`, `/kvkk`, `404`,
  `/urunler.json` (arama ve sepet için küçük katalog).
- `src/scripts/sepet.ts` sepet deposu, çekmece, sepete ekle formları, sipariş geçmişi; `katalog.ts`
  filtre ve sıralama; `ara.ts` üst arama.
- `src/content/ayarlar.json` mağaza bilgileri; `src/data/site.ts` sabitler ve yardımcılar.
- Sipariş mesajı formatı `src/pages/sepet.astro` içindeki `mesaj()` fonksiyonunda.
