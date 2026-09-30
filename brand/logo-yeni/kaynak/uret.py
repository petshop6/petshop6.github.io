# -*- coding: utf-8 -*-
"""Pet Shop 6 · logoyu yüksek çözünürlüklü PNG ve baskıya hazır PDF olarak üretir.
   Tasarıma dokunulmaz: sadece JPEG bozulmaları temizlenir, çözünürlük büyütülür
   (iterative back-projection) ve çerçeve dengelenir."""
import datetime, pathlib, zlib
import numpy as np, cv2
from restore import oku, temizle, ibp

CIK = pathlib.Path(__file__).parent / 'cikti'
CIK.mkdir(exist_ok=True)
DPI = 300

def keskinlestir(x):
    """çok hafif, halo yapmayan netleştirme"""
    b = cv2.GaussianBlur(x, (0, 0), 2.0)
    return np.clip(cv2.addWeighted(x, 1.22, b, -0.22, 0), 0, 255)

def kirp(img, pay=0.08, esik=20):
    lum = img.max(axis=2)
    ys, xs = np.nonzero(lum > esik)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    m = int((x1 - x0) * pay)
    h, w = img.shape[:2]
    return img[max(0, y0 - m):min(h, y1 + m + 1), max(0, x0 - m):min(w, x1 + m + 1)]

def pdf_yaz(yol, rgb, alpha=None, baslik='Pet Shop 6 logo', dpi=DPI):
    """Tek sayfalık, kayıpsız (FlateDecode) PDF; istenirse şeffaf zemin (SMask)."""
    h, w = rgb.shape[:2]
    W, H = w * 72.0 / dpi, h * 72.0 / dpi
    nesne, tampon = [], bytearray(b'%PDF-1.7\n%\xe2\xe3\xcf\xd3\n')
    def ekle(govde):
        nesne.append(len(tampon))
        tampon.extend(f'{len(nesne)} 0 obj\n'.encode() + govde + b'\nendobj\n')
        return len(nesne)
    def akis(sozluk, veri):
        return f'<<{sozluk}/Length {len(veri)}>>\nstream\n'.encode() + veri + b'\nendstream'
    kat = ekle(b'<</Type/Catalog/Pages 2 0 R>>')
    sayfalar = ekle(b'<</Type/Pages/Kids[3 0 R]/Count 1>>')
    ekle(f'<</Type/Page/Parent 2 0 R/MediaBox[0 0 {W:.4f} {H:.4f}]'
         f'/Resources<</XObject<</Im0 4 0 R>>>>/Contents 5 0 R>>'.encode())
    smask = ''
    if alpha is not None:
        smask = '/SMask 6 0 R'
    ekle(akis(f'/Type/XObject/Subtype/Image/Width {w}/Height {h}/ColorSpace/DeviceRGB'
              f'/BitsPerComponent 8/Filter/FlateDecode{smask}',
              zlib.compress(rgb.astype(np.uint8).tobytes(), 9)))
    icerik = f'q {W:.4f} 0 0 {H:.4f} 0 0 cm /Im0 Do Q'.encode()
    ekle(akis('/Filter/FlateDecode', zlib.compress(icerik, 9)))
    if alpha is not None:
        ekle(akis(f'/Type/XObject/Subtype/Image/Width {w}/Height {h}/ColorSpace/DeviceGray'
                  f'/BitsPerComponent 8/Filter/FlateDecode',
                  zlib.compress(alpha.astype(np.uint8).tobytes(), 9)))
    t = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    bilgi = ekle(f'<</Title({baslik})/Producer(Pet Shop 6)/CreationDate(D:{t})>>'.encode())
    xref = len(tampon)
    tampon.extend(f'xref\n0 {len(nesne)+1}\n0000000000 65535 f \n'.encode())
    for off in nesne:
        tampon.extend(f'{off:010d} 00000 n \n'.encode())
    tampon.extend(f'trailer\n<</Size {len(nesne)+1}/Root {kat} 0 R/Info {bilgi} 0 R>>\n'
                  f'startxref\n{xref}\n%%EOF\n'.encode())
    pathlib.Path(yol).write_bytes(bytes(tampon))
    return W / 72 * 25.4, H / 72 * 25.4

def kaydet(ad, bgr, baslik):
    rgb = cv2.cvtColor(bgr.astype(np.uint8), cv2.COLOR_BGR2RGB)
    cv2.imwrite(str(CIK / f'{ad}.png'), bgr.astype(np.uint8), [cv2.IMWRITE_PNG_COMPRESSION, 9])
    # şeffaf sürüm: alfa = parlaklık (altın ve hâle kalır, siyah zemin gider)
    a = np.clip(bgr.max(axis=2).astype(np.float32) * 1.35, 0, 255).astype(np.uint8)
    bgra = np.dstack([bgr.astype(np.uint8), a])
    cv2.imwrite(str(CIK / f'{ad}-seffaf.png'), bgra, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    mm = pdf_yaz(CIK / f'{ad}.pdf', rgb, None, baslik)
    pdf_yaz(CIK / f'{ad}-seffaf.pdf', rgb, a, baslik + ' (seffaf zemin)')
    print(f'{ad}: {bgr.shape[1]}x{bgr.shape[0]} px · {mm[0]:.0f}x{mm[1]:.0f} mm @ {DPI} dpi')

if __name__ == '__main__':
    panel = oku()
    buyuk = keskinlestir(ibp(temizle(panel)))
    tam = kirp(buyuk)
    kaydet('PetShop6-Logo', tam, 'Pet Shop 6 logo')
    # amblem: yazının üstünde kalan 6 + kedi-köpek işareti
    lum = tam.max(axis=2)
    satir = (lum > 10).sum(axis=1)
    orta = len(satir) // 2
    bosluk = [y for y in range(orta, len(satir)) if satir[y] < 2]
    kes = bosluk[0] if bosluk else len(satir)
    kaydet('PetShop6-Amblem', kirp(tam[:kes]), 'Pet Shop 6 amblem')
