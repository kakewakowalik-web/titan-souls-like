# Propozycje postaci v2 — 24×32, 3 tony cieniowania, obrys. python3 make.py
from PIL import Image, ImageDraw, ImageFont
W, H = 24, 32
FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
def hx(c): return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
def shade(c, f): return tuple(max(0, min(255, int(v * f))) for v in c)

class Spr:
    def __init__(s): s.px = {}  # (x,y) -> (rgb, region, flat)
    def put(s, x, y, c, reg, flat=False):
        if 0 <= x < W and 0 <= y < H: s.px[(x, y)] = (hx(c) if isinstance(c, str) else c, reg, flat)
    def rect(s, x0, y0, x1, y1, c, reg, flat=False):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): s.put(x, y, c, reg, flat)
    def ell(s, cx, cy, rx, ry, c, reg, flat=False):
        for y in range(int(cy - ry), int(cy + ry) + 1):
            for x in range(int(cx - rx), int(cx + rx) + 1):
                if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1: s.put(x, y, c, reg, flat)
    def line(s, pts, c, reg, flat=True):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(abs(x1 - x0), abs(y1 - y0), 1)
            for i in range(n + 1): s.put(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c, reg, flat)
    def render(s, outline='14121a', rim=None, hi=1.25, lo=0.68):
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        reg = lambda p: s.px[p][1] if p in s.px else None
        for (x, y), (c, r, flat) in s.px.items():
            col = c
            if not flat:
                if reg((x + 1, y)) != r or reg((x, y + 1)) != r: col = shade(c, lo)       # cień prawo/dół
                elif reg((x - 1, y)) != r or reg((x, y - 1)) != r: col = shade(c, hi)     # światło lewo/góra
            im.putpixel((x, y), col + (255,))
        out = im.copy()
        for y in range(H):
            for x in range(W):
                if im.getpixel((x, y))[3] == 0 and any(0 <= x + dx < W and 0 <= y + dy < H and im.getpixel((x + dx, y + dy))[3] for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))):
                    out.putpixel((x, y), hx(outline) + (255,))
        if rim:  # jasny obrys od strony światła (góra-lewo) — czytelność na ciemnym tle
            for y in range(H):
                for x in range(W):
                    if out.getpixel((x, y))[3] and (x == 0 or y == 0 or out.getpixel((x - 1, y))[3] == 0 or out.getpixel((x, y - 1))[3] == 0) and (x + y) < 30:
                        out.putpixel((x, y), hx(rim) + (255,))
        return out

def shadow(s): s.ell(12, 30, 7, 1.6, '000000', 'sh', True)

def A():  # krępy 16-bit, Titan Souls
    s = Spr()
    s.rect(7, 25, 10, 29, '3a3040', 'legL'); s.rect(13, 25, 16, 29, '3a3040', 'legR')
    s.rect(7, 28, 10, 29, '2a2026', 'bootL'); s.rect(13, 28, 16, 29, '2a2026', 'bootR')
    s.ell(12, 20, 7, 6, '9a2f3a', 'body')
    s.line([(6, 15), (17, 24)], 'c8a060', 'strap')
    s.rect(7, 24, 16, 25, '5a3a24', 'belt'); s.put(12, 24, 'e0c060', 'buckle', True)
    s.ell(4, 20, 2, 3, 'e8b48a', 'handL'); s.ell(19, 20, 2, 3, 'e8b48a', 'handR')
    s.line([(21, 12), (22, 16), (22, 22), (21, 26)], '8a5a30', 'bow'); s.line([(21, 12), (20, 19), (21, 26)], 'd8d0b0', 'str')
    s.ell(12, 9, 7, 7, 'e8b48a', 'face')
    s.ell(12, 6, 7.5, 5, '6a3a2a', 'hair'); s.rect(5, 6, 6, 11, '6a3a2a', 'hairL'); s.rect(18, 6, 19, 11, '6a3a2a', 'hairR')
    s.rect(9, 10, 9, 11, '1a1620', 'eyeL', True); s.rect(14, 10, 14, 11, '1a1620', 'eyeR', True)
    s.put(8, 12, 'e88a7a', 'ch', True); s.put(15, 12, 'e88a7a', 'ch', True)
    shadow(s); return s.render()

def B():  # smukły, Zelda LttP
    s = Spr()
    s.rect(9, 24, 10, 29, 'e8d8b0', 'legL'); s.rect(13, 24, 14, 29, 'e8d8b0', 'legR')
    s.rect(8, 27, 10, 29, '7a4a22', 'bootL'); s.rect(13, 27, 15, 29, '7a4a22', 'bootR')
    s.rect(8, 15, 15, 24, '3a9a3a', 'tunic'); s.rect(7, 22, 16, 24, '3a9a3a', 'skirt')
    s.rect(8, 20, 15, 20, '6a4a22', 'belt', True); s.put(11, 20, 'e0c060', 'b', True)
    s.rect(6, 16, 7, 21, '3a9a3a', 'armL'); s.rect(16, 16, 17, 21, '3a9a3a', 'armR')
    s.rect(6, 22, 7, 23, 'f0c8a0', 'hL'); s.rect(16, 22, 17, 23, 'f0c8a0', 'hR')
    s.line([(5, 13), (4, 18), (4, 24), (5, 28)], '9a6a30', 'bow'); s.line([(5, 13), (6, 20), (5, 28)], 'e0e0d0', 'str')
    s.ell(12, 10, 5, 5, 'f0c8a0', 'face')
    s.rect(7, 6, 16, 8, 'e8b040', 'hair'); s.rect(7, 8, 8, 12, 'e8b040', 'hairL'); s.rect(15, 8, 16, 11, 'e8b040', 'hairR')
    s.line([(7, 6), (10, 2), (14, 2), (17, 6)], '2e8a2e', 'cap', False); s.rect(9, 2, 15, 6, '2e8a2e', 'cap')
    s.line([(16, 4), (19, 8), (20, 12)], '2e8a2e', 'tip', False)
    s.rect(10, 10, 10, 11, '20406a', 'eL', True); s.rect(13, 10, 13, 11, '20406a', 'eR', True)
    s.put(6, 10, 'f0c8a0', 'ear'); s.put(17, 10, 'f0c8a0', 'ear')
    shadow(s); return s.render(outline='1a1a24')

def C():  # mroczna sylwetka z rim light
    s = Spr()
    s.line([(6, 14), (4, 22), (3, 29)], '1c1c26', 'capeL', False)
    s.ell(12, 21, 8, 8, '1c1c26', 'cloak'); s.rect(5, 21, 19, 29, '1c1c26', 'cloak')
    for x in (7, 11, 15): s.line([(x, 23), (x, 29)], '12121a', 'fold')
    s.ell(12, 10, 6, 6, '22222e', 'hood'); s.line([(12, 3), (12, 1)], '22222e', 'hood', False)
    s.ell(12, 11, 4, 3.5, '06060a', 'void', True)
    s.put(10, 11, 'ffd65a', 'eye', True); s.put(14, 11, 'ffd65a', 'eye', True)
    s.put(10, 12, 'a07a20', 'eye2', True); s.put(14, 12, 'a07a20', 'eye2', True)
    s.line([(19, 10), (21, 16), (21, 24), (19, 30)], '3a2a40', 'bow'); s.line([(19, 10), (19, 30)], '8a7aa0', 'str')
    s.ell(12, 18, 1.5, 1.5, '9a3a3a', 'gem')
    shadow(s); return s.render(outline='050507', rim='8a8aa8', hi=1.4)

def D():  # chibi
    s = Spr()
    s.rect(8, 26, 10, 29, '4a5a8a', 'legL'); s.rect(13, 26, 15, 29, '4a5a8a', 'legR')
    s.rect(8, 28, 10, 29, '8a4a3a', 'sL'); s.rect(13, 28, 15, 29, '8a4a3a', 'sR')
    s.ell(12, 22, 6, 5, '7ab8e8', 'body'); s.rect(9, 18, 14, 19, 'ffffff', 'collar')
    s.ell(5, 22, 2, 2, 'ffd8c0', 'hL'); s.ell(18, 22, 2, 2, 'ffd8c0', 'hR')
    s.line([(20, 15), (21, 19), (21, 24), (20, 28)], 'c08040', 'bow'); s.line([(20, 15), (20, 28)], 'ffffff', 'str')
    s.ell(12, 10, 10, 9, 'ffd8c0', 'face')
    s.ell(12, 6, 10.5, 6, 'a06040', 'hair'); s.rect(2, 6, 4, 14, 'a06040', 'hL2'); s.rect(19, 6, 21, 13, 'a06040', 'hR2')
    s.line([(7, 3), (9, 9)], 'a06040', 'fringe', False); s.line([(14, 2), (15, 9)], 'a06040', 'fringe', False)
    for ex in (7, 15):
        s.rect(ex, 10, ex + 2, 13, '2a2030', 'eye', True); s.put(ex, 10, 'ffffff', 'gl', True); s.put(ex + 1, 13, '4a6aa0', 'ir', True)
    s.rect(4, 14, 5, 14, 'ff9aa8', 'ch', True); s.rect(18, 14, 19, 14, 'ff9aa8', 'ch', True)
    s.rect(11, 15, 12, 15, 'a04050', 'm', True)
    s.ell(17, 2, 2, 1.5, 'ff7a90', 'bowtie')
    shadow(s); return s.render(outline='2a2030')

def E():  # rycerz w zbroi
    s = Spr()
    s.rect(7, 24, 10, 29, '8a929e', 'legL'); s.rect(13, 24, 16, 29, '8a929e', 'legR')
    s.rect(7, 26, 10, 26, '5a6270', 'knee', True); s.rect(13, 26, 16, 26, '5a6270', 'knee', True)
    s.rect(5, 15, 18, 24, 'a8b0bc', 'chest'); s.line([(11, 16), (11, 23)], '7a8290', 'seam', True)
    s.rect(6, 23, 17, 24, '5a3a2a', 'belt'); s.put(11, 23, 'd8b040', 'b', True)
    s.ell(4, 16, 3, 2.5, '9aa2ae', 'pauL'); s.ell(19, 16, 3, 2.5, '9aa2ae', 'pauR')
    s.rect(2, 18, 4, 23, '8a929e', 'armL'); s.rect(19, 18, 21, 23, '8a929e', 'armR')
    s.rect(8, 17, 15, 21, 'b03a3a', 'tabard'); s.line([(11, 17), (11, 21)], 'e0c060', 'cross', True); s.line([(9, 19), (14, 19)], 'e0c060', 'cross', True)
    s.line([(22, 10), (23, 16), (23, 24), (22, 30)], '6a4a2a', 'bow'); s.line([(22, 10), (22, 30)], 'c8c8c8', 'str')
    s.ell(12, 9, 6, 6.5, 'a8b0bc', 'helm'); s.rect(6, 9, 17, 14, 'a8b0bc', 'helm')
    s.rect(7, 10, 16, 11, '1a1c24', 'visor', True); s.rect(11, 12, 12, 14, '6a7280', 'nose', True)
    for x in (8, 10, 13, 15): s.put(x, 13, '3a3e48', 'holes', True)
    s.line([(12, 2), (11, 0), (14, 0), (16, 3)], 'c83a3a', 'plume', False); s.rect(10, 1, 14, 3, 'c83a3a', 'plume')
    shadow(s); return s.render()

def F():  # łucznik w kapturze
    s = Spr()
    s.line([(17, 6), (19, 4)], 'c8c0a0', 'fl', True); s.line([(19, 6), (21, 5)], 'c8c0a0', 'fl', True)
    s.rect(16, 6, 19, 16, '7a4a28', 'quiver')
    s.rect(8, 25, 10, 29, '3a2a1a', 'legL'); s.rect(13, 25, 15, 29, '3a2a1a', 'legR')
    s.rect(7, 28, 10, 29, '24180e', 'bL'); s.rect(13, 28, 16, 29, '24180e', 'bR')
    s.ell(12, 21, 7, 6, '4a5a3a', 'cloak'); s.rect(5, 21, 18, 26, '4a5a3a', 'cloak')
    for x in (8, 12, 16): s.line([(x, 22), (x - 1, 26)], '35422a', 'fold')
    s.rect(9, 16, 14, 24, '8a6a40', 'tunic'); s.rect(9, 21, 14, 21, '4a3018', 'belt', True)
    s.line([(9, 16), (15, 22)], '6a4a28', 'strap', True)
    s.ell(5, 21, 1.6, 2, 'd8a880', 'hL'); s.ell(19, 21, 1.6, 2, 'd8a880', 'hR')
    s.line([(3, 11), (2, 16), (2, 25), (3, 30)], '9a6a30', 'bow'); s.line([(3, 11), (4, 20), (3, 30)], 'e8e0c8', 'str')
    s.ell(12, 10, 7, 7.5, '4a5a3a', 'hood'); s.line([(12, 2), (12, 1)], '4a5a3a', 'hood', False)
    s.ell(12, 12, 4.5, 4, 'd8a880', 'face')
    s.rect(8, 9, 16, 10, '2e3a24', 'brim', True)
    s.rect(10, 12, 10, 12, '1a1a14', 'e', True); s.rect(14, 12, 14, 12, '1a1a14', 'e', True)
    s.put(9, 14, 'c08a6a', 'c', True); s.put(15, 14, 'c08a6a', 'c', True)
    shadow(s); return s.render(outline='121610')

STYLES = [("a_titan_chunky", "A: Krępy 16-bit (Titan Souls)", A), ("b_zelda_thin", "B: Smukły jak Zelda LttP", B),
          ("c_dark_silhouette", "C: Mroczna sylwetka + poświata", C), ("d_chibi", "D: Słodki chibi", D),
          ("e_armored_knight", "E: Rycerz w zbroi", E), ("f_hooded_archer", "F: Łucznik w kapturze", F)]
SC = 6; ARENA = (47, 45, 41); DARK = (20, 19, 24)
tiles = []
for key, name, fn in STYLES:
    im = fn(); im.save(f'{key}.png')
    up = im.resize((W * SC, H * SC), Image.NEAREST)
    big = Image.new('RGB', up.size, ARENA); big.paste(up, (0, 0), up); big.save(f'{key}_x{SC}.png')
    tiles.append((name, im, up))
cw, chh = W * SC + 90, H * SC + 70
sheet = Image.new('RGB', (cw * 3, chh * 2), (27, 26, 32)); d = ImageDraw.Draw(sheet)
for i, (name, im, up) in enumerate(tiles):
    x, y = (i % 3) * cw + 14, (i // 3) * chh + 10
    bg = Image.new('RGB', up.size, ARENA); bg.paste(up, (0, 0), up); sheet.paste(bg, (x, y))
    for j, col in enumerate((ARENA, DARK, (140, 130, 110))):  # test czytelności 1:1 i ×2 na 3 tłach
        sm = Image.new('RGB', (W * 2 + 4, H * 2 + 4), col); s2 = im.resize((W * 2, H * 2), Image.NEAREST); sm.paste(s2, (2, 2), s2)
        sheet.paste(sm, (x + up.width + 2, y + j * (H * 2 + 6)))
    d.text((x, y + up.height + 6), name, fill=(232, 217, 160), font=FONT)
    d.text((x, y + up.height + 24), "24×32 · obok ×2 na 3 tłach", fill=(125, 117, 99), font=FONT)
sheet.save('compare.png')
