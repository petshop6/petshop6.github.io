# -*- coding: utf-8 -*-
"""Builds src/content/urunler.json and downloads the brand packshots listed here.
Run:  python3 tools/katalog.py            (skips images that already exist)
Prices marked with ornek=True are placeholders until the shop's price list arrives."""
import json, os, re, sys, urllib.request, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / 'src/assets/urunler'
IMG.mkdir(parents=True, exist_ok=True)
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
RF = 'https://www.reflexmama.com/'
PU = 'https://www.purina.com.tr'
AD = 'https://www.advance-affinity.com'

def rf(p): return RF + 'upload/product_gallery/' + p
def s(*v): return [{'boy': b, 'fiyat': f} for b, f in v]

# slug, ad, marka, tur, kategori, etiketler, aciklama, secenekler, gorsel-url, kaynak-sayfa, oneCikan
P = []
def add(slug, ad, marka, tur, kat, etk, acik, sec, img, kaynak, one=False):
    P.append(dict(slug=slug, ad=ad, marka=marka, tur=tur, kategori=kat, etiketler=etk, aciklama=acik,
                  secenekler=sec, gorselUrl=img, kaynak=kaynak, oneCikan=one))

# ---------- KEDİ · KURU MAMA ----------
add('pro-plan-sterilised-somonlu', 'Pro Plan Sterilised Somonlu Kısırlaştırılmış Kedi Maması', 'Pro Plan', 'kedi', 'kuru-mama',
    ['kısırlaştırılmış', 'yetişkin', 'somon'], 'Kısırlaştırılmış yetişkin kediler için somon içerikli kuru mama. OptiRenal formülü.',
    s(('1,5 kg', 590), ('3 kg', 1090), ('10 kg', 3290)),
    PU + '/sites/default/files/2023-11/1.jpg',
    PU + '/kedi/kedi-mamasi/urun-proplan-sterilised-somon', True)
add('pro-plan-sterilised-hindili', 'Pro Plan Sterilised Hindili Kısırlaştırılmış Kedi Maması', 'Pro Plan', 'kedi', 'kuru-mama',
    ['kısırlaştırılmış', 'yetişkin', 'hindi'], 'Kısırlaştırılmış yetişkin kediler için hindi eti içerikli kuru mama.',
    s(('1,5 kg', 590), ('3 kg', 1090), ('10 kg', 3290)),
    PU + '/sites/default/files/2023-12/360PRO%20PLAN%C2%AE%20Sterilised%C2%AE%20K%C4%B1s%C4%B1rlas%CC%A7t%C4%B1l%C4%B1lm%C4%B1s%CC%A7%20Yetis%CC%A7kin%20Kediler%20ic%CC%A7in%2C%20Zengin%20Hindi%20Eti%20I%CC%87c%CC%A7erig%CC%86i_4.jpg',
    PU + '/kedi/kedi-mamasi/urun-proplan-sterilised-hindi')
add('pro-plan-kitten-tavuklu', 'Pro Plan Kitten Tavuklu Yavru Kedi Maması', 'Pro Plan', 'kedi', 'kuru-mama',
    ['yavru', 'tavuk'], '1-12 aylık yavru kediler için tavuk içerikli kuru mama. Gebe ve emziren kedilere de uygundur.',
    s(('1,5 kg', 620), ('3 kg', 1140)),
    PU + '/sites/default/files/2023-12/07613036505277_C1N1_44179147.jpg',
    PU + '/kedi/kedi-mamasi/urun-proplan-kitten-tavuk', True)
add('pro-plan-delicate-kuzulu', 'Pro Plan Delicate Kuzulu Hassas Sindirim Kedi Maması', 'Pro Plan', 'kedi', 'kuru-mama',
    ['yetişkin', 'hassas sindirim', 'kuzu'], 'Hassas sindirimli yetişkin kediler için kuzu eti içerikli kuru mama.',
    s(('1,5 kg', 610), ('3 kg', 1120)),
    PU + '/sites/default/files/2023-12/360PRO%20PLAN%C2%AE%20Delicate%C2%AE%20Yetis%CC%A7kin%20Kediler%20ic%CC%A7in%2C%20Zengin%20Kuzu%20Eti%20I%CC%87c%CC%A7erig%CC%86i_1.jpg',
    PU + '/kedi/kedi-mamasi/urun-proplan-delicate-kuzu')
add('pro-plan-derma-care-somonlu', 'Pro Plan Derma Care Somonlu Kedi Maması', 'Pro Plan', 'kedi', 'kuru-mama',
    ['yetişkin', 'deri ve tüy', 'somon'], 'Deri ve tüy sağlığı için somon içerikli yetişkin kedi kuru maması.',
    s(('1,5 kg', 610), ('3 kg', 1120)),
    PU + '/sites/default/files/2023-12/360PRO%20PLAN%C2%AE%20Derma%20Care%C2%AE%20Yetis%CC%A7kin%20Kediler%20ic%CC%A7in%2C%20Zengin%20Somon%20I%CC%87c%CC%A7erig%CC%86i_2.jpg',
    PU + '/kedi/kedi-mamasi/urun-proplan-derma-care-somon')
add('reflex-plus-longevity-kisirlastirilmis', 'Reflex Plus Longevity Kısırlaştırılmış Yetişkin Kedi Maması', 'Reflex Plus', 'kedi', 'kuru-mama',
    ['kısırlaştırılmış', 'yetişkin'], 'Kısırlaştırılmış yetişkin kediler için kuru mama. Tahılsız, tavuk içerikli.',
    s(('1,5 kg', 390), ('15 kg', 2690)),
    rf('product_gallery_2025-12-15_11-16-28.png'), RF + 'reflex-plus-longevity-kisirlastirilmis-yetiskin-kedi-mamasi', True)
add('reflex-plus-longevity-yetiskin', 'Reflex Plus Longevity Yetişkin Kedi Maması', 'Reflex Plus', 'kedi', 'kuru-mama',
    ['yetişkin'], 'Yetişkin kediler için kuru mama. Tahılsız, tavuk içerikli.',
    s(('1,5 kg', 390), ('15 kg', 2690)),
    rf('product_gallery_2025-12-15_10-51-02.png'), RF + 'reflex-plus-longevity-yetiskin-kedi-mamasi')
add('reflex-plus-longevity-yavru', 'Reflex Plus Longevity Yavru Kedi Maması', 'Reflex Plus', 'kedi', 'kuru-mama',
    ['yavru'], '12 aya kadar yavru kediler için kuru mama. Tahılsız, tavuk içerikli.',
    s(('1,5 kg', 410)),
    rf('product_gallery_2025-12-10_17-16-09.png'), RF + 'reflex-plus-longevity-yavru-kedi-mamasi')
add('reflex-crunchy-bubble-kisirlastirilmis-somonlu', 'Reflex Crunchy Bubble Kısırlaştırılmış Somonlu Kedi Maması', 'Reflex', 'kedi', 'kuru-mama',
    ['kısırlaştırılmış', 'yetişkin', 'somon'], 'Kısırlaştırılmış yetişkin kediler için somonlu kuru mama.',
    s(('1,5 kg', 340), ('15 kg', 2390)),
    rf('product_gallery_2026-07-24_14-18-291.png'), RF + 'reflex-crunchy-bubble-adult-cat-sterilized-salmon')
add('reflex-crunchy-bubble-kisirlastirilmis-tavuklu', 'Reflex Crunchy Bubble Kısırlaştırılmış Tavuklu Kedi Maması', 'Reflex', 'kedi', 'kuru-mama',
    ['kısırlaştırılmış', 'yetişkin', 'tavuk'], 'Kısırlaştırılmış yetişkin kediler için tavuklu kuru mama.',
    s(('1,5 kg', 340), ('15 kg', 2390)),
    rf('product_gallery_2026-07-24_14-18-401.png'), RF + 'eflex-crunchy-bubble-adult-cat-sterilized-chicken')
add('reflex-crunchy-bubble-yetiskin-tavuklu', 'Reflex Crunchy Bubble Yetişkin Tavuklu Kedi Maması', 'Reflex', 'kedi', 'kuru-mama',
    ['yetişkin', 'tavuk'], 'Yetişkin kediler için tavuklu kuru mama.',
    s(('1,5 kg', 330), ('15 kg', 2290)),
    rf('product_gallery_2026-07-24_14-18-431.png'), RF + 'reflex-crunchy-bubble-adult-cat-chicken')
add('reflex-crunchy-bubble-urinary-tavuklu', 'Reflex Crunchy Bubble Urinary Tavuklu Kedi Maması', 'Reflex', 'kedi', 'kuru-mama',
    ['yetişkin', 'üriner', 'tavuk'], 'İdrar yolu sağlığı için formüle edilmiş tavuklu yetişkin kedi maması.',
    s(('1,5 kg', 350)),
    rf('product_gallery_2026-07-24_14-18-361.png'), RF + 'reflex-crunchy-bubble-adult-cat-urinary-chicken')
add('reflex-somonlu-hamsili', 'Reflex Somonlu ve Hamsili Yetişkin Kedi Maması', 'Reflex', 'kedi', 'kuru-mama',
    ['yetişkin', 'somon'], 'Yetişkin kediler için somon ve hamsi içerikli kuru mama.',
    s(('1,5 kg', 320), ('15 kg', 2190)),
    rf('product_gallery_2025-11-21_15-53-34.png'), RF + 'reflex-somonlu-ve-hamsili-yetiskin-kedi-mamasi')
add('advance-adult-tavuklu', 'Advance Adult Tavuklu Yetişkin Kedi Maması', 'Advance', 'kedi', 'kuru-mama',
    ['yetişkin', 'tavuk'], 'Yetişkin kediler için tavuk ve pirinç içerikli kuru mama.',
    s(('1,5 kg', 720), ('3 kg', 1320)),
    AD + '/dw/image/v2/bdgx_prd/on/demandware.static/-/Sites-ADVANCE-m-catalog/default/dwe16cf7de/images/affinitypetcare/db2495b7-4100-4e54-9ff7-b300004fa17a/D245EF16E3A0B03BFB0E0CB7286042273C0EA9DFC98D_Resized.png?sw=900&q=100',
    AD + '/tr/kedi/yemek-kedi/adult-1000379.html')
add('advance-kitten', 'Advance Kitten Tavuklu Yavru Kedi Maması', 'Advance', 'kedi', 'kuru-mama',
    ['yavru', 'tavuk'], 'Yavru kediler ile gebe ve emziren kediler için tavuk ve pirinç içerikli kuru mama.',
    s(('400 g', 260), ('1,5 kg', 760)),
    AD + '/dw/image/v2/bdgx_prd/on/demandware.static/-/Sites-ADVANCE-m-catalog/default/dw69eadb83/images/affinitypetcare/9605a33d-d505-49e2-bcef-b3000053952a/D443F6672E5F8A96C5FE61D50961B799F2A5D9CC2234_Resized.png?sw=900&q=100',
    AD + '/tr/kedi/yemek-kedi/kitten-1000382.html')
add('advance-sensitive-care-somonlu', 'Advance Sensitive Care Somonlu Kedi Maması', 'Advance', 'kedi', 'kuru-mama',
    ['yetişkin', 'hassas sindirim', 'somon'], 'Hassas sindirim ve deri için somon ve pirinç içerikli yetişkin kedi maması.',
    s(('1,5 kg', 760), ('3 kg', 1390)),
    AD + '/dw/image/v2/bdgx_prd/on/demandware.static/-/Sites-ADVANCE-m-catalog/default/dwa3903f22/images/affinitypetcare/d98b1c4d-e674-4529-8922-b3000054ddd4/D4E9E249BA39D177BBB42C563F957717BFAC19493370_Resized.png?sw=900&q=100',
    AD + '/tr/kedi/yemek-kedi/sensitive-1000380.html')

# ---------- KEDİ · YAŞ MAMA ----------
add('reflex-plus-pramy-somonlu-tavuklu', 'Reflex Plus Pramy Jöle İçinde Somonlu ve Tavuklu Yaş Kedi Maması', 'Reflex Plus', 'kedi', 'yas-mama',
    ['yetişkin', 'pouch', 'somon'], 'Jöle içinde somonlu ve tavuklu pouch. Yetişkin kediler için tamamlayıcı mama.',
    s(('85 g', 42), ('12×85 g', 480)),
    rf('product_gallery_2025-11-18_14-34-23.png'), RF + 'reflex-plus-pramy-jole-icinde-somonlu-ve-tavuklu', True)
add('reflex-plus-pramy-ton-balikli-tavuklu', 'Reflex Plus Pramy Jöle İçinde Ton Balıklı ve Tavuklu Yaş Kedi Maması', 'Reflex Plus', 'kedi', 'yas-mama',
    ['yetişkin', 'pouch', 'ton balığı'], 'Jöle içinde ton balıklı ve tavuklu pouch.',
    s(('85 g', 42), ('12×85 g', 480)),
    rf('product_gallery_2025-11-18_10-31-43.png'), RF + 'reflex-plus-pramy-jole-icinde-ton-balikli-ve-tavuklu')
add('reflex-plus-pramy-yagsiz-ton-balikli', 'Reflex Plus Pramy Jöle İçinde Yağsız Ton Balıklı Yaş Kedi Maması', 'Reflex Plus', 'kedi', 'yas-mama',
    ['yetişkin', 'pouch', 'ton balığı'], 'Jöle içinde yağsız ton balıklı pouch.',
    s(('85 g', 42), ('12×85 g', 480)),
    rf('product_gallery_2025-11-18_10-19-23.png'), RF + 'reflex-plus-pramy-jole-icinde-yagsiz-ton-balikli')
add('reflex-plus-pramy-sos-tavuklu-balkabakli', 'Reflex Plus Pramy Sos İçinde Tavuklu, Bal Kabaklı ve Havuçlu Yaş Kedi Maması', 'Reflex Plus', 'kedi', 'yas-mama',
    ['yetişkin', 'pouch', 'tavuk'], 'Sos içinde tavuklu, bal kabaklı ve havuçlu pouch.',
    s(('85 g', 42), ('12×85 g', 480)),
    rf('product_gallery_2025-11-18_10-13-46.png'), RF + 'reflex-plus-pramy-sos-icinde-tavuklu-bal-kabakli-ve-havuclu')
add('reflex-plus-pramy-yavru-somonlu-mousse', 'Reflex Plus Pramy Yavru Kediler için Somonlu Mousse', 'Reflex Plus', 'kedi', 'yas-mama',
    ['yavru', 'somon'], 'Yavru kediler için somonlu mousse kıvamında yaş mama.',
    s(('85 g', 45)),
    rf('product_gallery_2025-11-18_09-16-26.png'), RF + 'reflex-plus-pramy-yavru-kediler-icin-somonlu-mousse')
add('reflex-essential-tavuk-goguslu', 'Reflex Essential Et Suyu İçinde Tavuk Göğüslü Yetişkin Kedi Maması', 'Reflex', 'kedi', 'yas-mama',
    ['yetişkin', 'tavuk'], 'Et suyu içinde tavuk göğüslü konserve. Yetişkin kediler için tamamlayıcı mama.',
    s(('70 g', 38)),
    rf('product_gallery_2025-11-10_14-02-15.png'), RF + 'essential-/-et-suyu-icinde-tavuk-goguslu-yetiskin-kedi-mamasi')
add('reflex-essentials-yavru-ton-somon', 'Reflex Essentials Et Suyu İçinde Ton Balıklı ve Somonlu Yavru Kedi Maması', 'Reflex', 'kedi', 'yas-mama',
    ['yavru', 'ton balığı', 'somon'], 'Et suyu içinde ton balıklı ve somonlu konserve. Yavru kediler için.',
    s(('70 g', 38)),
    rf('product_gallery_2025-11-10_14-33-27.png'), RF + 'essentials-/-et-suyu-icinde-ton-balikli-ve-somonlu-yavru-kedi-mamasi')
add('pro-plan-adult-7-ton-balikli', 'Pro Plan Adult 7+ Kıyılmış Ton Balıklı Yaş Kedi Maması', 'Pro Plan', 'kedi', 'yas-mama',
    ['7+ yaş', 'pouch', 'ton balığı'], '7 yaş ve üzeri kediler için kıyılmış ton balıklı pouch.',
    s(('85 g', 48)),
    PU + '/sites/default/files/2023-12/Pro-Plan-Cat-Adult7%2B-Tuna-85g-43607838-360x360px_3.png',
    PU + '/kedi/kedi-mamasi/urun-proplan-adult-ton-balikli')
add('advance-adult-chicken-yas', 'Advance Adult Tavuklu Yaş Kedi Maması', 'Advance', 'kedi', 'yas-mama',
    ['yetişkin', 'pouch', 'tavuk'], 'Yetişkin kediler için tavuklu pouch.',
    s(('85 g', 52)),
    AD + '/dw/image/v2/bdgx_prd/on/demandware.static/-/Sites-ADVANCE-m-catalog/default/dw03bc5d25/images/affinitypetcare/6696f3bf-1f60-460d-b530-b46a00b6a075/MATERIALS_130344_ADVANCE_WET_ADULT_CHICKEN_85GR_2D_Resized.png?sw=900&q=100',
    AD + '/tr/kedi/yemek-kedi/adult-chicken-1000393.html')
add('advance-kitten-chicken-yas', 'Advance Kitten Tavuklu Yaş Yavru Kedi Maması', 'Advance', 'kedi', 'yas-mama',
    ['yavru', 'pouch', 'tavuk'], 'Yavru kediler için tavuklu pouch.',
    s(('85 g', 52)),
    AD + '/dw/image/v2/bdgx_prd/on/demandware.static/-/Sites-ADVANCE-m-catalog/default/dwd1a11d2b/images/affinitypetcare/18e3176f-9a9c-4d60-b41e-b30000591869/D73352A579D9CA9DCD6CCBD669A5DE0CCC4819888246_Resized.png?sw=900&q=100',
    AD + '/tr/kedi/yemek-kedi/kitten-chicken-1000394.html')

# ---------- KEDİ · ÖDÜL ----------
add('reflex-happy-hour-kisirlastirilmis', 'Reflex Happy Hour Kısırlaştırılmış Kediler için Ödül Maması', 'Reflex', 'kedi', 'odul',
    ['kısırlaştırılmış', 'ödül'], 'Kısırlaştırılmış kediler için kıtır ödül maması.',
    s(('60 g', 65)),
    rf('product_gallery_2025-03-06_16-10-351.png'), RF + 'happy-hour-/-kisirlastirilmis-kediler-icin-odul-mamasi')
add('reflex-pocket-treats-tuy-yumagi', 'Reflex Pocket Treats Tüy Yumağı Kontrolü Kedi Ödül Maması', 'Reflex', 'kedi', 'odul',
    ['ödül', 'tüy yumağı'], 'Tüy yumağı kontrolüne yardımcı kıtır ödül maması.',
    s(('60 g', 65)),
    rf('product_gallery_2024-08-01_10-02-32.png'), RF + 'pocket-treats-/-tuy-yumagi-kontrolu-icin-kedi-odul-mamasi')
add('reflex-pocket-treats-agiz-dis', 'Reflex Pocket Treats Ağız ve Diş Sağlığı Kedi Ödül Maması', 'Reflex', 'kedi', 'odul',
    ['ödül', 'diş'], 'Ağız ve diş sağlığı için kıtır ödül maması.',
    s(('60 g', 65)),
    rf('product_gallery_2024-08-01_09-37-59.png'), RF + 'pocket-treats-agiz-ve-dis-sagligi')
add('reflex-meaty-sticks-somonlu', 'Reflex Meaty Sticks Somonlu Kedi Ödül Çubuğu', 'Reflex', 'kedi', 'odul',
    ['ödül', 'çubuk', 'somon'], 'Somonlu etli ödül çubuğu, 3 adet.',
    s(('3×5 g', 32)),
    rf('product_gallery_2024-08-06_14-11-51.png'), RF + 'meaty-sticks-/-somonlu-cubuk-2', True)
add('reflex-meaty-sticks-yavru-hindi', 'Reflex Meaty Sticks Yavru Kediler için Hindi Etli Çubuk', 'Reflex', 'kedi', 'odul',
    ['yavru', 'ödül', 'çubuk'], 'Yavru kediler için hindi etli ödül çubuğu, 3 adet.',
    s(('3×5 g', 32)),
    rf('product_gallery_2024-08-06_09-45-08.png'), RF + 'meaty-sticks-/-yavru-kediler-icin-hindi-etli-cubuk')
add('reflex-meat-fillet-tavuk', 'Reflex Meat Fillet Tavuk Fileto Kedi Ödülü', 'Reflex', 'kedi', 'odul',
    ['ödül', 'tavuk'], 'Kedi ödülü olarak tavuk fileto.',
    s(('20 g', 45)),
    rf('product_gallery_2025-05-27_11-08-47.png'), RF + 'meat-fillet-/-tavuk-fileto')

# ---------- KEDİ · KUM ----------
add('reflex-aktif-karbonlu-kedi-kumu', 'Reflex Aktif Karbonlu Topaklanan Kedi Kumu', 'Reflex', 'kedi', 'kedi-kumu',
    ['topaklanan', 'aktif karbon'], 'Doğal aktif karbonlu, hızlı topaklanan bentonit kedi kumu. Amonyak kokusunu bloke eder.',
    s(('10 L', 290), ('20 L', 540)),
    rf('product_gallery_2021-05-17_14-58-05.png'), RF + 'reflex-kedi-kumlari', True)
add('reflex-aktif-karbon-granullu-kedi-kumu', 'Reflex Aktif Karbon Granüllü Topaklanan Kedi Kumu', 'Reflex', 'kedi', 'kedi-kumu',
    ['topaklanan', 'aktif karbon'], 'Aktif karbon tanecikli topaklanan bentonit kedi kumu.',
    s(('10 L', 290), ('20 L', 540)),
    rf('product_gallery_2021-05-17_14-57-12.png'), RF + 'reflex-kedi-kumlari')
add('reflex-klinik-kedi-kumu', 'Reflex Klinik Topaklanan Kedi Kumu', 'Reflex', 'kedi', 'kedi-kumu',
    ['topaklanan', 'klinik'], 'Özel formüllü tanecikli topaklanan kedi kumu. Kapalı ortamda beslenen kediler için.',
    s(('10 L', 300), ('20 L', 560)),
    rf('product_gallery_2021-05-17_14-58-52.png'), RF + 'reflex-kedi-kumlari')
add('reflex-parfumsuz-kedi-kumu', 'Reflex Hassas Kediler İçin Parfümsüz Topaklanan Kedi Kumu', 'Reflex', 'kedi', 'kedi-kumu',
    ['topaklanan', 'parfümsüz'], 'Parfümsüz, kompakt taneli doğal bentonit kedi kumu. Patiye yapışmaz.',
    s(('10 L', 280), ('20 L', 520)),
    rf('product_gallery_2021-05-17_15-00-04.png'), RF + 'reflex-kedi-kumlari')

# ---------- KÖPEK · KURU MAMA ----------
add('pro-plan-medium-adult-somonlu', 'Pro Plan Medium Adult Sensitive Skin Somonlu Köpek Maması', 'Pro Plan', 'kopek', 'kuru-mama',
    ['yetişkin', 'orta ırk', 'hassas deri', 'somon'], 'Orta ırk yetişkin köpekler için somon içerikli kuru mama. Hassas deri için.',
    s(('3 kg', 990), ('14 kg', 3890)),
    PU + '/sites/default/files/2023-08/1_17.jpg',
    PU + '/kopek/kopek-mamasi/urun-proplan-medium-adult-somon', True)
add('pro-plan-medium-puppy-kuzulu', 'Pro Plan Medium Puppy Kuzulu Yavru Köpek Maması', 'Pro Plan', 'kopek', 'kuru-mama',
    ['yavru', 'orta ırk', 'kuzu'], 'Orta ırk yavru köpekler için kuzu eti içerikli kuru mama.',
    s(('3 kg', 990), ('12 kg', 3490)),
    PU + '/sites/default/files/2023-08/1_14.jpg',
    PU + '/kopek/kopek-mamasi/urun-proplan-medium-puppy-kuzueti')
add('pro-plan-small-mini-adult-somonlu', 'Pro Plan Small & Mini Adult Sensitive Skin Somonlu Köpek Maması', 'Pro Plan', 'kopek', 'kuru-mama',
    ['yetişkin', 'küçük ırk', 'somon'], 'Küçük ırk yetişkin köpekler için somon içerikli kuru mama.',
    s(('3 kg', 1040)),
    PU + '/sites/default/files/2023-08/1_20.jpg',
    PU + '/kopek/kopek-mamasi/urun-proplan-small-mini-adult-somon')
add('pro-plan-large-athletic-somonlu', 'Pro Plan Large Athletic Adult Sensitive Skin Somonlu Köpek Maması', 'Pro Plan', 'kopek', 'kuru-mama',
    ['yetişkin', 'büyük ırk', 'somon'], 'Büyük ırk, atletik yapılı yetişkin köpekler için somon içerikli kuru mama.',
    s(('14 kg', 3990)),
    PU + '/sites/default/files/2023-08/1_11.jpg',
    PU + '/kopek/kopek-mamasi/urun-proplan-large-athletic-somon')
add('pro-plan-all-size-light', 'Pro Plan All Size Adult Light Tavuklu Köpek Maması', 'Pro Plan', 'kopek', 'kuru-mama',
    ['yetişkin', 'kilo kontrolü', 'tavuk'], 'Kilo kontrolü için düşük yağlı, tavuk içerikli yetişkin köpek maması.',
    s(('14 kg', 3890)),
    PU + '/sites/default/files/2023-08/1_12.jpg',
    PU + '/kopek/kopek-mamasi/urun-proplan-allsize-tavuk')
add('reflex-plus-longevity-orta-buyuk-yetiskin', 'Reflex Plus Longevity Orta ve Büyük Irk Yetişkin Köpek Maması', 'Reflex Plus', 'kopek', 'kuru-mama',
    ['yetişkin', 'orta ırk', 'büyük ırk'], 'Orta ve büyük ırk yetişkin köpekler için kuru mama.',
    s(('3 kg', 520), ('15 kg', 2290)),
    rf('product_gallery_2025-12-10_16-33-42.png'), RF + 'reflex-plus-longevity-orta-ve-buyuk-irk-yetiskin-kopek-mamasi', True)
add('reflex-plus-longevity-mini-kucuk-yetiskin', 'Reflex Plus Longevity Mini ve Küçük Irk Yetişkin Köpek Maması', 'Reflex Plus', 'kopek', 'kuru-mama',
    ['yetişkin', 'küçük ırk'], 'Mini ve küçük ırk yetişkin köpekler için kuru mama.',
    s(('3 kg', 540)),
    rf('product_gallery_2025-12-10_14-41-43.png'), RF + 'reflex-plus-longevity-mini-ve-kucuk-irk-yetiskin-kopek-mamasi')
add('reflex-plus-kuzu-orta-buyuk-yavru', 'Reflex Plus Kuzu Etli Orta ve Büyük Irk Yavru Köpek Maması', 'Reflex Plus', 'kopek', 'kuru-mama',
    ['yavru', 'orta ırk', 'büyük ırk', 'kuzu'], 'Orta ve büyük ırk yavru köpekler için kuzu etli kuru mama.',
    s(('3 kg', 540), ('15 kg', 2390)),
    rf('product_gallery_2025-11-17_16-11-44.png'), RF + 'reflex-plus-kuzu-etli-orta-ve-buyuk-irk-yavru-kopek-mamasi')
add('reflex-plus-tavuklu-orta-buyuk-yetiskin', 'Reflex Plus Tavuklu Orta ve Büyük Irk Yetişkin Köpek Maması', 'Reflex Plus', 'kopek', 'kuru-mama',
    ['yetişkin', 'orta ırk', 'büyük ırk', 'tavuk'], 'Orta ve büyük ırk yetişkin köpekler için tavuklu kuru mama.',
    s(('3 kg', 490), ('15 kg', 2190)),
    rf('product_gallery_2025-11-17_13-59-36.png'), RF + 'reflex-plus-tavuklu-orta-ve-buyuk-irk-yetiskin-kopek-mamasi-2')
add('reflex-plus-tavuklu-mini-kucuk-yavru', 'Reflex Plus Tavuklu Mini ve Küçük Irk Yavru Köpek Maması', 'Reflex Plus', 'kopek', 'kuru-mama',
    ['yavru', 'küçük ırk', 'tavuk'], 'Mini ve küçük ırk yavru köpekler için tavuklu kuru mama.',
    s(('3 kg', 520)),
    rf('product_gallery_2025-11-17_17-05-11.png'), RF + 'reflex-plus-tavuklu-mini-ve-kucuk-irk-yavru-kopek-mamasi-2')
add('reflex-somonlu-kuzulu-yetiskin-kopek', 'Reflex Somonlu ve Kuzu Etli Yetişkin Köpek Maması', 'Reflex', 'kopek', 'kuru-mama',
    ['yetişkin', 'somon', 'kuzu'], 'Yetişkin köpekler için somon ve kuzu etli kuru mama.',
    s(('3 kg', 440), ('15 kg', 1890)),
    rf('product_gallery_2025-11-26_10-02-17.png'), RF + 'reflex-somonlu-ve-kuzu-etli-yetiskin-kopek-mamasi')
add('advance-adult-medium', 'Advance Adult Medium Tavuklu Köpek Maması', 'Advance', 'kopek', 'kuru-mama',
    ['yetişkin', 'orta ırk', 'tavuk'], 'Orta ırk yetişkin köpekler için tavuk ve pirinç içerikli kuru mama.',
    s(('3 kg', 1190), ('14 kg', 4490)),
    AD + '/dw/image/v2/bdgx_prd/on/demandware.static/-/Sites-ADVANCE-m-catalog/default/dw551c52b3/images/affinitypetcare/713c9886-068d-4761-8abf-b30000663b73/DE1DAC91F33CCD4FB800FEB066B31F92BD0E8F4117D2_Resized.png?sw=900&q=100',
    AD + '/tr/k%C3%B6pek/yemek-k%C3%B6pek/adult-medium-1000414.html')
add('advance-adult-mini', 'Advance Adult Mini Tavuklu Köpek Maması', 'Advance', 'kopek', 'kuru-mama',
    ['yetişkin', 'küçük ırk', 'tavuk'], 'Küçük ırk yetişkin köpekler için tavuk ve pirinç içerikli kuru mama.',
    s(('800 g', 420), ('3 kg', 1240)),
    AD + '/dw/image/v2/bdgx_prd/on/demandware.static/-/Sites-ADVANCE-m-catalog/default/dwc32f85d1/images/affinitypetcare/3e5401c3-489c-4551-8f8c-b300004fe38e/D2676CC8985D534FA31292D61B89F6BE46E18AB2698A_Resized.png?sw=900&q=100',
    AD + '/tr/k%C3%B6pek/yemek-k%C3%B6pek/adult-mini-1000404.html')
add('advance-adult-maxi', 'Advance Adult Maxi Tavuklu Köpek Maması', 'Advance', 'kopek', 'kuru-mama',
    ['yetişkin', 'büyük ırk', 'tavuk'], 'Büyük ırk yetişkin köpekler için tavuk ve pirinç içerikli kuru mama.',
    s(('14 kg', 4490)),
    AD + '/dw/image/v2/bdgx_prd/on/demandware.static/-/Sites-ADVANCE-m-catalog/default/dwca0d6127/images/affinitypetcare/4608e5cf-4012-474f-b1ae-b30000585d07/D6CA3420B2062A7891CB62E5EE78EA619E49E189D58D_Resized.png?sw=900&q=100',
    AD + '/tr/k%C3%B6pek/yemek-k%C3%B6pek/adult-maxi-1000419.html')
add('advance-sensitive-care-kuzulu', 'Advance Adult Sensitive Care Kuzulu Köpek Maması', 'Advance', 'kopek', 'kuru-mama',
    ['yetişkin', 'hassas sindirim', 'kuzu'], 'Hassas sindirim ve deri için kuzu ve pirinç içerikli yetişkin köpek maması.',
    s(('3 kg', 1290), ('12 kg', 4290)),
    AD + '/dw/image/v2/bdgx_prd/on/demandware.static/-/Sites-ADVANCE-m-catalog/default/dw5ba56eee/images/affinitypetcare/d6029861-684b-4503-9600-b3000069e86b/DFC86FD4E9232E4A7397CC27971D6FA6A7E1E79838F4_Resized.png?sw=900&q=100',
    AD + '/tr/k%C3%B6pek/yemek-k%C3%B6pek/adult-sensitive-care-lamb-1000428.html')

# ---------- KÖPEK · ÖDÜL ----------
add('reflex-dentastar-mini-kucuk', 'Reflex Dentastar Çiğnemelik Diş Çubukları · Mini ve Küçük Irk', 'Reflex', 'kopek', 'odul',
    ['ödül', 'diş', 'küçük ırk'], 'Küçük ırk yetişkin köpekler için çiğnemelik diş çubuğu.',
    s(('7 adet', 95)),
    rf('product_gallery_2025-04-18_15-13-27.png'), RF + 'dentastar-/-cignemelik-dis-cubuklari-mini-ve-kucuk-irk-yetiskin-kopek-odul-mamasi', True)
add('reflex-dentastar-buyuk', 'Reflex Dentastar Çiğnemelik Diş Çubukları · Büyük Irk', 'Reflex', 'kopek', 'odul',
    ['ödül', 'diş', 'büyük ırk'], 'Büyük ırk yetişkin köpekler için çiğnemelik diş çubuğu.',
    s(('7 adet', 135)),
    rf('product_gallery_2025-04-18_15-23-31.png'), RF + 'dentastar-/-cignemelik-dis-cubuklari-buyuk-irk-yetiskin-kopek-odul-mamasi')
add('reflex-cookie-bites-mini-bones', 'Reflex Cookie Bites Mini Bones Köpek Bisküvisi', 'Reflex', 'kopek', 'odul',
    ['ödül', 'bisküvi'], 'Kemik şeklinde köpek bisküvisi.',
    s(('180 g', 85)),
    rf('product_gallery_2025-06-04_10-20-58.png'), RF + 'cookie-bites-/-mini-bones')
add('reflex-twix-tavuklu-biftekli', 'Reflex Twix Tavuklu & Biftekli Çiğneme Çubukları', 'Reflex', 'kopek', 'odul',
    ['ödül', 'çiğneme'], 'Yetişkin köpekler için tavuklu ve biftekli çiğneme çubuğu.',
    s(('75 g', 75)),
    rf('product_gallery_2025-04-18_14-21-09.png'), RF + 'twix-/-tavuklu-biftekli-cigneme-cubuklari-yetiskin-kopek-odul-mamasi')
add('reflex-bacon-chips', 'Reflex Bacon Chips Çiğnemelik Jambon Dilimleri', 'Reflex', 'kopek', 'odul',
    ['ödül', 'çiğneme'], 'Yetişkin köpekler için çiğnemelik jambon dilimi.',
    s(('75 g', 75)),
    rf('product_gallery_2025-04-18_11-04-14.png'), RF + 'bacon-chips-/-cignemelik-jambon-dilimleri-yetiskin-kopek-odul-mamasi')
add('reflex-pocket-treats-eklem', 'Reflex Pocket Treats Eklem Sağlığı Köpek Ödül Maması', 'Reflex', 'kopek', 'odul',
    ['ödül', 'eklem'], 'Eklem sağlığına destek için kıtır ödül maması.',
    s(('75 g', 70)),
    rf('product_gallery_2025-06-03_16-31-07.png'), RF + 'pocket-treats-/-eklem-sagligi-icin-kopek-odul-mamasi')
add('reflex-semi-moist-peynirli', 'Reflex Semi Moist Peynirli Köpek Ödül Maması', 'Reflex', 'kopek', 'odul',
    ['ödül', 'peynir'], 'Yarı nemli peynirli ödül maması.',
    s(('80 g', 70)),
    rf('product_gallery_2026-02-20_14-48-291.png'), RF + 'semi-moist-peynirli-kopek-odul-mamasi')

# ---------- download + write ----------
out = []
for p in P:
    url = p['gorselUrl']
    ext = '.png' if '.png' in url.lower().split('?')[0] else '.jpg'
    fn = p['slug'] + ext
    dest = IMG / fn
    if ext == '.jpg' and (IMG / (p['slug'] + '.png')).exists():  # already converted by tools/seffaf.py
        fn = p['slug'] + '.png'; dest = IMG / fn
    if not dest.exists():
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': url.split('/', 3)[0] + '//' + url.split('/', 3)[2] + '/'})
        try:
            with urllib.request.urlopen(req, timeout=40) as r, open(dest, 'wb') as f:
                f.write(r.read())
            print('ok ', fn, dest.stat().st_size)
        except Exception as e:
            print('ERR', fn, e)
    q = dict(p); q['gorsel'] = fn; del q['gorselUrl']
    out.append(q)

(ROOT / 'src/content/urunler.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(len(out), 'ürün yazıldı')
