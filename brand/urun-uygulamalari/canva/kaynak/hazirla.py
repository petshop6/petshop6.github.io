import calendar
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ALTIN  = (201, 162, 77)
ALTIN2 = (230, 203, 135)
KAGIT  = (233, 229, 220)
GRI    = (150, 144, 132)

def fnt(ad, boy):
    for yol, idx in ad:
        try:
            return ImageFont.truetype(yol, boy, index=idx)
        except Exception:
            pass
    return ImageFont.load_default()

BASLIK = [("/System/Library/Fonts/Supplemental/Futura.ttc", 0)]
ORTA   = [("/System/Library/Fonts/Supplemental/Futura.ttc", 0)]   # italik yok
GOVDE  = [("/System/Library/Fonts/Avenir Next.ttc", 0)]
GOVDE_M= [("/System/Library/Fonts/Avenir Next.ttc", 2)]

def arali(d, xy, metin, font, renk, bosluk):
    x, y = xy
    for ch in metin:
        d.text((x, y), ch, font=font, fill=renk)
        x += d.textlength(ch, font=font) + bosluk
    return x - bosluk - xy[0]

def arali_en(d, metin, font, bosluk):
    return sum(d.textlength(c, font=font) for c in metin) + bosluk * (len(metin) - 1)

# ---------------------------------------------------------------- 1. wordmark şeridi
def wordmark():
    im = Image.open("PetShop6-Logo-seffaf.png")
    a = np.asarray(im)[:, :, 3]
    H, W = a.shape
    rows = (a > 16).sum(axis=1)
    kes = 1980 + int(np.argmin(rows[1980:2100]))          # işaretle yazı arasındaki boşluk
    alt = im.crop((0, kes, W, H))
    b = np.asarray(alt)[:, :, 3]
    ys, xs = np.where(b > 16)
    kutu = (xs.min() - 6, ys.min() - 6, xs.max() + 7, ys.max() + 7)
    cikti = alt.crop(kutu)
    cikti.save("artwork-wordmark.png")
    print("wordmark", cikti.size, "kesim y =", kes)

# ---------------------------------------------------------------- 2. masa takvimi işi
def takvim(yil=2027, ay=1):
    EN, BOY = 2400, 1440
    im = Image.new("RGBA", (EN, BOY), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    # logo, sol üst
    logo = Image.open("PetShop6-Logo-seffaf.png")
    lh = 430
    lw = round(logo.width * lh / logo.height)
    im.alpha_composite(logo.resize((lw, lh), Image.LANCZOS), (0, 0))

    # ay + yıl, sağ üst
    f_ay  = fnt(BASLIK, 150)
    f_yil = fnt(ORTA, 88)
    adlar = ["OCAK", "ŞUBAT", "MART", "NİSAN", "MAYIS", "HAZİRAN",
             "TEMMUZ", "AĞUSTOS", "EYLÜL", "EKİM", "KASIM", "ARALIK"]
    ad = adlar[ay - 1]
    gen_ay  = arali_en(d, ad, f_ay, 16)
    gen_yil = arali_en(d, str(yil), f_yil, 10)
    SAG = 46                                            # sağ pay: harf aralığı taşmasın
    x = EN - SAG - gen_ay
    arali(d, (x, 96), ad, f_ay, KAGIT, 16)
    arali(d, (EN - SAG - gen_yil, 268), str(yil), f_yil, ALTIN, 10)
    d.line([x - 60, 120, x - 60, 350], fill=(92, 86, 74), width=3)

    # ızgara
    ust = 560
    d.line([0, ust - 90, EN, ust - 90], fill=(92, 86, 74), width=3)
    sut = EN / 7
    gunler = ["PZT", "SAL", "ÇAR", "PER", "CUM", "CMT", "PAZ"]
    f_gun = fnt(GOVDE_M, 46)
    for i, g in enumerate(gunler):
        w = arali_en(d, g, f_gun, 8)
        arali(d, (sut * i + (sut - w) / 2, ust - 56), g, f_gun,
              ALTIN if i == 6 else GRI, 8)

    calendar.setfirstweekday(calendar.MONDAY)
    haftalar = calendar.monthcalendar(yil, ay)
    f_say = fnt(ORTA, 84)
    satir_y = ust + 40
    yuk = (BOY - satir_y - 110) / len(haftalar)
    for r, hafta in enumerate(haftalar):
        for c, gun in enumerate(hafta):
            if not gun:
                continue
            s = str(gun)
            w = d.textlength(s, font=f_say)
            d.text((sut * c + (sut - w) / 2, satir_y + r * yuk),
                   s, font=f_say, fill=ALTIN2 if c == 6 else KAGIT)
    im.save("artwork-takvim.png")
    print("takvim", im.size)

wordmark()
takvim()
