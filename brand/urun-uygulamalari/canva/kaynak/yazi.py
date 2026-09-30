from PIL import Image, ImageDraw, ImageFont

K = 4                                    # sayfa pikseli başına render pikseli
KAGIT  = (244, 241, 234)
GRI    = (182, 175, 162)
GRI2   = (139, 132, 121)
ALTIN  = (201, 162, 77)

def fnt(yol, idx, boy):
    return ImageFont.truetype(yol, boy, index=idx)

FUTURA = "/System/Library/Fonts/Supplemental/Futura.ttc"
AVENIR = "/System/Library/Fonts/Avenir Next.ttc"

def arali(d, xy, metin, font, renk, bosluk):
    x, y = xy
    for ch in metin:
        d.text((x, y), ch, font=font, fill=renk)
        x += d.textlength(ch, font=font) + bosluk

def arali_en(d, metin, font, bosluk):
    return sum(d.textlength(c, font=font) for c in metin) + bosluk * (len(metin) - 1)

# ---------------------------------------------------------------- kapak yazısı
def kapak():
    EN, BOY = 600 * K, 170 * K
    im = Image.new("RGBA", (EN, BOY), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([EN/2 - 80*K, 0, EN/2 + 80*K, 1.5*K], fill=ALTIN)
    f1 = fnt(FUTURA, 0, 29 * K)
    f2 = fnt(AVENIR, 5, 14 * K)
    f3 = fnt(AVENIR, 5, 12 * K)
    b1 = 6 * K
    w = arali_en(d, "ÜRÜN UYGULAMALARI", f1, b1)
    arali(d, ((EN - w) / 2, 38 * K), "ÜRÜN UYGULAMALARI", f1, KAGIT, b1)
    for metin, f, renk, y in [("Kartvizit · anahtarlık · kalem · masa takvimi", f2, GRI, 96 * K),
                              ("Pet Shop 6 · Bahçelievler, Ankara", f3, GRI2, 126 * K)]:
        w = d.textlength(metin, font=f)
        d.text(((EN - w) / 2, y), metin, font=f, fill=renk)
    im.save("artwork-kapak.png")
    print("kapak", im.size)

# ---------------------------------------------------------------- sayfa etiketi
def etiket(dosya, ad, spec):
    EN, BOY = 560 * K, 86 * K
    im = Image.new("RGBA", (EN, BOY), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 44 * K, 1.5 * K], fill=ALTIN)
    f1 = fnt(FUTURA, 0, 21 * K)
    f2 = fnt(AVENIR, 5, 12.5 * K)
    arali(d, (0, 20 * K), ad.upper().replace("I", "I"), f1, KAGIT, 4.5 * K)
    d.text((0, 60 * K), spec, font=f2, fill=GRI)
    im.save(dosya)
    print(dosya, im.size)

kapak()
etiket("artwork-etiket-kartvizit.png", "KARTVİZİT",
       "85 × 55 mm · mat siyah karton · altın yaldız baskı")
etiket("artwork-etiket-anahtarlik.png", "ANAHTARLIK",
       "50 × 30 mm · siyah eloksal alüminyum · altın baskı")
etiket("artwork-etiket-kalem.png", "KALEM",
       "Mat siyah gövde, altın klips · gövdeye altın baskı")
etiket("artwork-etiket-takvim.png", "MASA TAKVİMİ",
       "21 × 15 cm · spiralli · Ocak 2027, pazar günleri altın")
