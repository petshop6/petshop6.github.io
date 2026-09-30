# -*- coding: utf-8 -*-
"""Pet Shop 6 · logonun ürün üzerindeki uygulamaları (kartvizit, anahtarlık, kalem, takvim).
   Tek bir çok sayfalı PDF ve her sayfanın PNG'sini üretir."""
import calendar, datetime, pathlib, zlib
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np

KOK = pathlib.Path(__file__).resolve().parent
LOGO = KOK.parent / 'logo-yeni'
CIK = KOK / 'cikti'; CIK.mkdir(exist_ok=True)

DPI = 250
EN, BOY = int(297 / 25.4 * DPI), int(210 / 25.4 * DPI)      # A4 yatay
ZEMIN = (14, 13, 11)
ALTIN = (201, 162, 77)
ALTIN_ACIK = (230, 203, 135)
KEMIK = (244, 241, 234)
GRI = (138, 132, 121)
FUTURA = '/System/Library/Fonts/Supplemental/Futura.ttc'
AVENIR = '/System/Library/Fonts/Avenir Next.ttc'

def buyuk(s):
    return s.replace('i', 'İ').replace('ı', 'I').upper()

def f_baslik(px, kalin=False):
    return ImageFont.truetype(FUTURA, px, index=1 if kalin else 0)
def f_govde(px, kalin=False):
    return ImageFont.truetype(AVENIR, px, index=1 if kalin else 0)

def arali(d, xy, metin, font, renk, aralik=0):
    """harf aralıklı yazı"""
    x, y = xy
    for ch in metin:
        d.text((x, y), ch, font=font, fill=renk)
        x += d.textlength(ch, font=font) + aralik
    return x - xy[0]

def arali_en(d, metin, font, aralik=0):
    return sum(d.textlength(c, font=font) + aralik for c in metin) - aralik

def golge(boyut, maske, bulanik=26, koyu=150):
    """maske tam sayfa boyutunda ve yerine yerleştirilmiş olmalı"""
    g = maske.filter(ImageFilter.GaussianBlur(bulanik))
    return Image.merge('RGBA', (Image.new('L', boyut, 0),) * 3 + (g.point(lambda v: int(v * koyu / 255)),))

def yuvarlak(boyut, r, dolgu, cerceve=None, kalinlik=2):
    im = Image.new('RGBA', boyut, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, boyut[0] - 1, boyut[1] - 1], r, fill=dolgu, outline=cerceve, width=kalinlik)
    return im

def logo_yerlestir(hedef, kutu, dosya='PetShop6-Logo-seffaf.png', pay=0.0):
    """logoyu verilen kutuya (x0,y0,x1,y1) sığdırıp ortalar"""
    lg = Image.open(LOGO / dosya).convert('RGBA')
    x0, y0, x1, y1 = kutu
    w, h = int((x1 - x0) * (1 - pay)), int((y1 - y0) * (1 - pay))
    lg.thumbnail((w, h), Image.LANCZOS)
    hedef.alpha_composite(lg, (int(x0 + ((x1 - x0) - lg.width) / 2), int(y0 + ((y1 - y0) - lg.height) / 2)))

def sayfa(baslik=None, alt=None):
    im = Image.new('RGBA', (EN, BOY), ZEMIN + (255,))
    d = ImageDraw.Draw(im)
    if baslik:
        f = f_baslik(34)
        arali(d, (150, 120), buyuk(baslik), f, ALTIN, 7)
        d.line([150, 178, 150 + 120, 178], fill=ALTIN, width=3)
    if alt:
        d.text((150, 196), alt, font=f_govde(26), fill=GRI)
    # altbilgi
    d.line([150, BOY - 118, EN - 150, BOY - 118], fill=(46, 43, 38), width=2)
    d.text((150, BOY - 100), 'Pet Shop 6 Bahçelievler · 54. Cadde No: 3/B, Çankaya, Ankara', font=f_govde(22), fill=GRI)
    return im, d

# ---------------------------------------------------------------- kapak
def kapak():
    im, d = Image.new('RGBA', (EN, BOY), ZEMIN + (255,)), None
    d = ImageDraw.Draw(im)
    logo_yerlestir(im, (150, 470, 150 + 900, 470 + 900))
    f = f_baslik(56)
    arali(d, (1250, 730), 'ÜRÜN UYGULAMALARI', f, KEMIK, 10)
    d.line([1250, 822, 1250 + 260, 822], fill=ALTIN, width=4)
    for i, satir in enumerate(['Logonun kartvizit, anahtarlık, kalem ve',
                               'takvim üzerindeki kullanımı. Ölçüler matbaa',
                               'için baskı ölçüleridir.']):
        d.text((1250, 872 + i * 46), satir, font=f_govde(28), fill=GRI)
    d.text((150, BOY - 150), datetime.date.today().strftime('%d.%m.%Y'), font=f_govde(24), fill=(74, 70, 63))
    return im

# ---------------------------------------------------------------- kartvizit
def kartvizit():
    im, d = sayfa('Kartvizit', '85 × 55 mm · ön yüz mürekkep, arka yüz kemik · mat lamine, altın yaldız önerilir')
    KW, KH, R = 1150, 744, 26                                   # 85×55 oranı
    def golgeli(kart, konum):
        m = Image.new('L', (EN, BOY), 0)
        mk = Image.new('L', (KW, KH), 0); ImageDraw.Draw(mk).rounded_rectangle([0, 0, KW - 1, KH - 1], R, fill=210)
        m.paste(mk, (konum[0] + 8, konum[1] + 30))
        im.alpha_composite(golge((EN, BOY), m, 34, 165))
        im.alpha_composite(kart, konum)
    # ön yüz
    on = yuvarlak((KW, KH), R, (18, 17, 14, 255), (58, 52, 40, 255), 2)
    logo_yerlestir(on, (KW * 0.18, KH * 0.14, KW * 0.82, KH * 0.86))
    golgeli(on, (190, 640))
    # arka yüz
    arka = yuvarlak((KW, KH), R, KEMIK + (255,), (226, 220, 206, 255), 2)
    da = ImageDraw.Draw(arka)
    karo = yuvarlak((160, 160), 14, (18, 17, 14, 255))
    logo_yerlestir(karo, (14, 14, 146, 146), 'PetShop6-Amblem-seffaf.png')
    arka.alpha_composite(karo, (70, 62))
    arali(da, (240, 92), 'PET SHOP 6', f_baslik(40), (23, 21, 15), 6)
    da.text((242, 146), 'Bahçelievler', font=f_govde(26), fill=(120, 114, 104))
    da.line([70, 300, KW - 70, 300], fill=(224, 216, 200), width=2)
    satirlar = [('Alo Mama', '0312 213 13 32'), ('WhatsApp', '0544 213 13 32'),
                ('Adres', '54. Cadde No: 3/B, Çankaya'), ('Web', 'petshop6.github.io')]
    for i, (etiket, deger) in enumerate(satirlar):
        y = 348 + i * 76
        da.text((70, y), etiket, font=f_govde(24), fill=(150, 144, 132))
        da.text((300, y - 4), deger, font=f_govde(30), fill=(23, 21, 15))
    golgeli(arka, (EN - 190 - KW, 640))
    d.text((190, 640 + KH + 52), 'Ön yüz', font=f_govde(26), fill=GRI)
    d.text((EN - 190 - KW, 640 + KH + 52), 'Arka yüz', font=f_govde(26), fill=GRI)
    return im

# ---------------------------------------------------------------- anahtarlık fotoğrafı (kullanıcının kendi dosyasından)
def anahtarlik_gorsel():
    hedef = KOK / 'anahtarlik.png'
    if hedef.exists():
        return Image.open(hedef).convert('RGBA')
    import cv2
    kaynak = cv2.imread(str(LOGO / 'kaynak' / 'orijinal-gonderilen.jpg'), cv2.IMREAD_COLOR)[:, 742:]
    f = cv2.fastNlMeansDenoisingColored(kaynak, None, 3, 3, 7, 21).astype(np.float32)
    h, w = f.shape[:2]; S = 3
    x = cv2.resize(f, (w * S, h * S), interpolation=cv2.INTER_LANCZOS4)
    for i in range(18):                                   # geri yansıtma: orijinale sadık büyütme
        d = cv2.resize(x, (w, h), interpolation=cv2.INTER_AREA)
        x += cv2.resize(f - d, (w * S, h * S), interpolation=cv2.INTER_CUBIC)
        if i % 6 == 5: x = cv2.bilateralFilter(x, 5, 18, 5)
        x = np.clip(x, 0, 255)
    im = Image.fromarray(cv2.cvtColor(x.astype(np.uint8), cv2.COLOR_BGR2RGB)).convert('RGBA')
    im.save(hedef); return im

# ---------------------------------------------------------------- kalem
def kalem_ciz(uzunluk=1560, kalinlik=104):
    """yandan görünüm: mat siyah gövde, altın klips, bilezik ve uç"""
    im = Image.new('RGBA', (uzunluk, kalinlik + 70), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y0 = 40; y1 = y0 + kalinlik; orta = (y0 + y1) // 2
    govde_sol, govde_sag = 40, uzunluk - 190
    # gövde
    d.rounded_rectangle([govde_sol, y0, govde_sag, y1], kalinlik // 2, fill=(22, 21, 18))
    # silindir ışığı (üst üçte bir)
    hh = kalinlik
    kolon = np.clip(1.0 - np.abs(np.linspace(0, 1, hh) - 0.30) * 3.6, 0, 1) * 52
    serit = np.repeat(kolon.reshape(hh, 1), govde_sag - govde_sol, axis=1).astype(np.uint8)
    maske = Image.new('L', (govde_sag - govde_sol, hh), 0)
    ImageDraw.Draw(maske).rounded_rectangle([0, 0, govde_sag - govde_sol - 1, hh - 1], kalinlik // 2, fill=255)
    a = Image.fromarray(np.minimum(serit, np.array(maske)), 'L')
    isik = Image.new('RGBA', (govde_sag - govde_sol, hh), (255, 242, 220, 255)); isik.putalpha(a)
    im.alpha_composite(isik, (govde_sol, y0))
    # kapak bileziği (kapak ile gövdenin birleştiği yer)
    d.rectangle([560, y0, 588, y1], fill=(176, 141, 62))
    d.rectangle([560, y0 + 10, 588, y0 + 40], fill=ALTIN_ACIK)
    # klips: kapağın üstüne oturur
    d.rounded_rectangle([132, y0 - 14, 470, y0 + 18], 16, fill=ALTIN)
    d.rounded_rectangle([132, y0 + 2, 470, y0 + 18], 8, fill=(176, 141, 62))
    d.rectangle([146, y0 - 6, 176, y0 + 30], fill=ALTIN)
    # ön bilezik + kısa konik uç
    d.rectangle([govde_sag - 40, y0, govde_sag, y1], fill=(176, 141, 62))
    d.rectangle([govde_sag - 40, y0 + 10, govde_sag, y0 + 40], fill=ALTIN_ACIK)
    konik_son = govde_sag + 118
    d.polygon([(govde_sag, y0 + 4), (govde_sag, y1 - 4), (konik_son, orta + 13), (konik_son, orta - 13)], fill=ALTIN)
    d.polygon([(govde_sag, orta + 14), (govde_sag, y1 - 4), (konik_son, orta + 13)], fill=(148, 118, 50))
    d.polygon([(konik_son, orta - 6), (konik_son, orta + 6), (konik_son + 34, orta + 2), (konik_son + 34, orta - 2)], fill=(40, 37, 31))
    # baskı
    amb = Image.open(LOGO / 'PetShop6-Amblem-seffaf.png').convert('RGBA'); amb.thumbnail((66, 66), Image.LANCZOS)
    im.alpha_composite(amb, (660, orta - amb.height // 2))
    arali(d, (752, orta - 20), 'PET SHOP 6', f_baslik(36), ALTIN_ACIK, 6)
    return im

# ---------------------------------------------------------------- sayfa: anahtarlık + kalem
def anahtarlik_kalem():
    im, d = sayfa('Anahtarlık ve kalem', 'Müşteriye verilen hediyelik · anahtarlık 45 mm çap, kalem gövdesine altın yaldız baskı')
    ah = anahtarlik_gorsel()
    oran = 980 / ah.height
    ah = ah.resize((int(ah.width * oran), 980), Image.LANCZOS)
    m = Image.new('L', (EN, BOY), 0)
    mk = Image.new('L', ah.size, 0); ImageDraw.Draw(mk).rounded_rectangle([0, 0, ah.width - 1, ah.height - 1], 18, fill=150)
    m.paste(mk, (160 + 10, 470 + 34)); im.alpha_composite(golge((EN, BOY), m, 40, 150))
    kirp = Image.new('RGBA', ah.size, (0, 0, 0, 0))
    yk = Image.new('L', ah.size, 0); ImageDraw.Draw(yk).rounded_rectangle([0, 0, ah.width - 1, ah.height - 1], 18, fill=255)
    kirp.paste(ah, (0, 0), yk)
    im.alpha_composite(kirp, (160, 470))
    d.text((160, 470 + 980 + 44), 'Anahtarlık · metal kasa, mürekkep zemin, altın kabartma', font=f_govde(26), fill=GRI)
    kl = kalem_ciz().rotate(-11, resample=Image.BICUBIC, expand=True)
    kx, ky = EN - 210 - kl.width, 470 + (980 - kl.height) // 2
    gm = Image.new('L', (EN, BOY), 0)
    gm.paste(kl.getchannel('A').point(lambda v: int(v * 0.75)), (kx + 10, ky + 34))
    im.alpha_composite(golge((EN, BOY), gm, 26, 150))
    im.alpha_composite(kl, (kx, ky))
    d.text((kx + 40, ky + kl.height + 40), 'Kalem · mat siyah gövde, altın klips ve bilezik', font=f_govde(26), fill=GRI)
    return im

# ---------------------------------------------------------------- takvim
GUNLER = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz']
AYLAR = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
         'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']

def takvim_ciz(yil=2027, ay=1, W=1560, H=1120):
    im = Image.new('RGBA', (W, H + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    bas_h = 330
    # üst mürekkep bandı
    d.rounded_rectangle([0, 0, W - 1, bas_h + 40], 18, fill=(18, 17, 14))
    d.rectangle([0, bas_h - 20, W - 1, bas_h + 40], fill=(18, 17, 14))
    logo_yerlestir(im, (70, 46, 70 + 430, 46 + 240))
    fy = f_baslik(72)
    ad = buyuk(AYLAR[ay - 1])
    gen = arali_en(d, ad, fy, 10)
    arali(d, (W - 90 - gen, 120), ad, fy, ALTIN, 10)
    d.text((W - 90 - gen, 218), str(yil), font=f_govde(44), fill=(150, 128, 84))
    # kemik gövde
    d.rounded_rectangle([0, bas_h, W - 1, H - 1], 18, fill=KEMIK)
    d.rectangle([0, bas_h, W - 1, bas_h + 30], fill=KEMIK)
    # spiral
    for i in range(11):
        x = 90 + i * (W - 180) / 10
        d.rounded_rectangle([x - 13, bas_h - 34, x + 13, bas_h + 26], 12, fill=(206, 203, 196), outline=(150, 147, 140), width=2)
    # gün başlıkları
    sol, sag, ust = 80, W - 80, bas_h + 96
    hucre = (sag - sol) / 7
    for i, g in enumerate(GUNLER):
        f = f_govde(30, True)
        gw = d.textlength(g, font=f)
        d.text((sol + hucre * i + (hucre - gw) / 2, ust), g, font=f, fill=(150, 112, 32) if i == 6 else (140, 134, 124))
    d.line([sol, ust + 56, sag, ust + 56], fill=(224, 218, 204), width=2)
    # günler
    hafta = calendar.Calendar(firstweekday=0).monthdayscalendar(yil, ay)
    fy = f_baslik(46)
    for r, satir in enumerate(hafta):
        for c, gun in enumerate(satir):
            if gun == 0: continue
            t = str(gun)
            tw = d.textlength(t, font=fy)
            x = sol + hucre * c + (hucre - tw) / 2
            y = ust + 92 + r * 96
            d.text((x, y), t, font=fy, fill=(150, 112, 32) if c == 6 else (26, 24, 20))
    # alt şerit
    d.line([sol, H - 108, sag, H - 108], fill=(228, 222, 208), width=2)
    d.text((sol, H - 88), 'Alo Mama 0312 213 13 32 · WhatsApp 0544 213 13 32', font=f_govde(28), fill=(96, 91, 83))
    sw = d.textlength('Ankara içi ücretsiz teslimat', font=f_govde(28))
    d.text((sag - sw, H - 88), 'Ankara içi ücretsiz teslimat', font=f_govde(28), fill=(150, 112, 32))
    return im

def takvim_sayfasi():
    im, d = sayfa('Masa takvimi', '21 × 15 cm · üst blok mürekkep, altın yaldız ay adı · spiralli, müşteriye yılbaşı hediyesi')
    tk = takvim_ciz()
    tx, ty = (EN - tk.width) // 2, 470
    gm = Image.new('L', (EN, BOY), 0)
    mk = Image.new('L', tk.size, 0); ImageDraw.Draw(mk).rounded_rectangle([0, 0, tk.width - 1, tk.height - 1], 18, fill=170)
    gm.paste(mk, (tx + 8, ty + 34)); im.alpha_composite(golge((EN, BOY), gm, 38, 160))
    im.alpha_composite(tk, (tx, ty))
    d.text((tx, ty + tk.height + 40), 'Her ay bir sayfa · ay adı altın, pazar günleri altın', font=f_govde(26), fill=GRI)
    return im

# ---------------------------------------------------------------- çok sayfalı PDF
def pdf_yaz(yol, sayfalar, baslik='Pet Shop 6 urun uygulamalari', dpi=DPI):
    nesne, tampon = [], bytearray(b'%PDF-1.7\n%\xe2\xe3\xcf\xd3\n')
    def ekle(govde):
        nesne.append(len(tampon))
        tampon.extend(f'{len(nesne)} 0 obj\n'.encode() + govde + b'\nendobj\n')
        return len(nesne)
    def akis(sozluk, veri):
        return f'<<{sozluk}/Length {len(veri)}>>\nstream\n'.encode() + veri + b'\nendstream'
    n = len(sayfalar)
    kat = ekle(b'<</Type/Catalog/Pages 2 0 R>>')
    kids = ' '.join(f'{3 + i * 3} 0 R' for i in range(n))
    ekle(f'<</Type/Pages/Kids[{kids}]/Count {n}>>'.encode())
    for i, sf in enumerate(sayfalar):
        rgb = np.asarray(sf.convert('RGB'), dtype=np.uint8)
        h, w = rgb.shape[:2]
        W, H = w * 72.0 / dpi, h * 72.0 / dpi
        im_no, ic_no = 3 + i * 3 + 1, 3 + i * 3 + 2
        ekle(f'<</Type/Page/Parent 2 0 R/MediaBox[0 0 {W:.3f} {H:.3f}]'
             f'/Resources<</XObject<</Im0 {im_no} 0 R>>>>/Contents {ic_no} 0 R>>'.encode())
        ekle(akis(f'/Type/XObject/Subtype/Image/Width {w}/Height {h}/ColorSpace/DeviceRGB'
                  f'/BitsPerComponent 8/Filter/FlateDecode', zlib.compress(rgb.tobytes(), 9)))
        ekle(akis('/Filter/FlateDecode', zlib.compress(f'q {W:.3f} 0 0 {H:.3f} 0 0 cm /Im0 Do Q'.encode(), 9)))
    t = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    bilgi = ekle(f'<</Title({baslik})/Producer(Pet Shop 6)/CreationDate(D:{t})>>'.encode())
    xref = len(tampon)
    tampon.extend(f'xref\n0 {len(nesne)+1}\n0000000000 65535 f \n'.encode())
    for off in nesne:
        tampon.extend(f'{off:010d} 00000 n \n'.encode())
    tampon.extend(f'trailer\n<</Size {len(nesne)+1}/Root {kat} 0 R/Info {bilgi} 0 R>>\n'
                  f'startxref\n{xref}\n%%EOF\n'.encode())
    pathlib.Path(yol).write_bytes(bytes(tampon))

if __name__ == '__main__':
    sayfalar = [kapak(), kartvizit(), anahtarlik_kalem(), takvim_sayfasi()]
    for ad, sf in zip(['1-kapak', '2-kartvizit', '3-anahtarlik-kalem', '4-takvim'], sayfalar):
        sf.convert('RGB').save(CIK / f'{ad}.png', optimize=True)
    pdf_yaz(CIK / 'PetShop6-Urun-Uygulamalari.pdf', sayfalar)
    print('PDF:', (CIK / 'PetShop6-Urun-Uygulamalari.pdf').stat().st_size // 1024, 'KB ·', len(sayfalar), 'sayfa')
