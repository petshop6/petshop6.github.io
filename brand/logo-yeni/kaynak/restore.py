# -*- coding: utf-8 -*-
"""Faithful restoration of the supplied Pet Shop 6 logo JPEG.
   1) JPEG artefact removal (edge-preserving, black background flattened)
   2) 4x upscale by iterative back-projection: the result is forced to match the
      original when it is scaled back down, so nothing is invented."""
import numpy as np, cv2

SRC = '/private/tmp/claude-501/-Users-huseyinolmez-Desktop-web-sitesi-g-rselleri/be682ed0-cbd3-476e-8a12-1afcafb9db49/images/1.jpg'
S = 4  # scale

def oku():
    im = cv2.imread(SRC, cv2.IMREAD_COLOR)
    return im[:, :742]                      # left panel = the logo artwork

def temizle(bgr):
    """JPEG blocking/ringing removal that keeps the gold edges and the halo.
       Faint noise far from the artwork is removed, the glow around it is kept."""
    f = cv2.fastNlMeansDenoisingColored(bgr, None, 3, 3, 7, 21)
    lum = f.max(axis=2).astype(np.float32)
    k = np.clip((lum - 5.0) / 9.0, 0, 1)                      # soft black floor
    yakin = cv2.GaussianBlur((lum > 20).astype(np.float32), (0, 0), 25)
    k *= np.clip(yakin * 6.0, 0, 1)                            # only near the mark
    k = np.maximum(k, np.clip((lum - 20.0) / 6.0, 0, 1))       # never touch the artwork
    return (f.astype(np.float32) * k[..., None]).astype(np.uint8)

def ibp(low, s=S, it=24, lam=1.0):
    h, w = low.shape[:2]
    lo = low.astype(np.float32)
    x = cv2.resize(lo, (w * s, h * s), interpolation=cv2.INTER_LANCZOS4)
    for i in range(it):
        d = cv2.resize(x, (w, h), interpolation=cv2.INTER_AREA)
        err = lo - d
        x += lam * cv2.resize(err, (w * s, h * s), interpolation=cv2.INTER_CUBIC)
        if i % 6 == 5:
            x = cv2.bilateralFilter(x, 5, 18, 5)   # keep ringing in check, edges intact
        x = np.clip(x, 0, 255)
    return x

if __name__ == '__main__':
    panel = oku()
    clean = temizle(panel)
    cv2.imwrite('clean.png', clean)
    big = ibp(clean)
    cv2.imwrite('big-ibp.png', big.astype(np.uint8))
    lanc = cv2.resize(clean, (panel.shape[1] * S, panel.shape[0] * S), interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite('big-lanczos.png', lanc)
    # side-by-side of the same detail: Lanczos (left) vs back-projection (right)
    for ad, (x0, y0, x1, y1) in {'muzzle': (430, 330, 560, 420), 'type': (150, 590, 420, 650)}.items():
        a = lanc[y0*S:y1*S, x0*S:x1*S]; b = big[y0*S:y1*S, x0*S:x1*S].astype(np.uint8)
        sep = np.full((a.shape[0], 8, 3), 60, np.uint8)
        cv2.imwrite(f'kiyas-{ad}.png', np.hstack([a, sep, b]))
    print('panel', panel.shape, '-> big', big.shape)
