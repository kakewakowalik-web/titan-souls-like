# Mapa 1: ogród -> ścieżka nad jeziorem -> wejście do ciemnej jaskini. python3 make_map1.py
import random, math
from PIL import Image, ImageDraw, ImageFont
T = 16
def hx(c): return tuple(int(c[i:i+2], 16) for i in (0, 2, 4)) + (255,)
def noise_tile(base, specks, seed, density=0.18):
    r = random.Random(seed); im = Image.new('RGBA', (T, T), hx(base))
    for y in range(T):
        for x in range(T):
            if r.random() < density: im.putpixel((x, y), hx(r.choice(specks)))
    return im
def grass(seed=1): 
    im = noise_tile('4a8a3a', ['3e7a32', '5a9a44', '3a6e2e'], seed)
    r = random.Random(seed + 9)
    for _ in range(5):
        x, y = r.randrange(1, 15), r.randrange(2, 15); im.putpixel((x, y), hx('6ab04e')); im.putpixel((x, y - 1), hx('6ab04e'))
    return im
def flowers(col, seed):
    im = grass(seed); r = random.Random(seed)
    for _ in range(5):
        x, y = r.randrange(2, 14), r.randrange(2, 14)
        for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)): im.putpixel((x + dx, y + dy), hx(col))
        im.putpixel((x, y), hx('f8e070'))
    return im
def path(seed=3): return noise_tile('b89a6a', ['a88a5a', 'c8aa7a', '9a7a4a'], seed, 0.25)
def stones(seed=4):
    im = Image.new('RGBA', (T, T), hx('6a8a4a')); d = ImageDraw.Draw(im)
    for (x, y, w, h) in ((1, 1, 6, 5), (8, 1, 7, 6), (1, 8, 7, 7), (9, 9, 6, 6)):
        d.rectangle((x, y, x + w - 1, y + h - 1), fill=hx('a8a49a')); d.line((x, y, x + w - 1, y), fill=hx('c8c4ba')); d.line((x, y + h - 1, x + w - 1, y + h - 1), fill=hx('7a766e'))
    return im
def water(seed=5, deep=False):
    base = '2a5a8a' if not deep else '1e4470'
    im = noise_tile(base, ['3a6a9a', '24507e'], seed, 0.1); r = random.Random(seed)
    for _ in range(3):
        x, y = r.randrange(1, 12), r.randrange(1, 15)
        for i in range(3): im.putpixel((x + i, y), hx('7ab0d8'))
    return im
def shore(side):  # trawa + woda, side = strona wody
    g = grass(7); w = water(8); im = g.copy()
    for y in range(T):
        for x in range(T):
            k = {'S': y, 'N': T - 1 - y, 'E': x, 'W': T - 1 - x}[side]
            edge = 7 + int(1.5 * math.sin((x + y) * 0.9))
            if k > edge: im.putpixel((x, y), w.getpixel((x, y)))
            elif k > edge - 2: im.putpixel((x, y), hx('d8c890'))  # piaszczysty brzeg
    return im
def hedge():
    im = noise_tile('2e6a2a', ['245a22', '3a7a32', '1e4e1c'], 11, 0.35); d = ImageDraw.Draw(im)
    d.line((0, 15, 15, 15), fill=hx('1a3a18')); d.line((0, 0, 15, 0), fill=hx('4a8a3e')); return im
def rock_tile():
    im = grass(12); d = ImageDraw.Draw(im)
    d.ellipse((2, 4, 13, 14), fill=hx('7a7670')); d.ellipse((3, 4, 10, 10), fill=hx('9a968e')); d.point((5, 6), fill=hx('bab6ae')); d.arc((2, 4, 13, 14), 20, 160, fill=hx('4a4642'))
    return im
def lily():
    im = water(13); d = ImageDraw.Draw(im); d.ellipse((3, 5, 11, 11), fill=hx('4a9a3a')); d.line((7, 8, 11, 6), fill=hx('2a5a8a')); d.ellipse((9, 3, 12, 6), fill=hx('f0a0c0')); return im
def reeds():
    im = shore('N'); d = ImageDraw.Draw(im)
    for x in (3, 6, 9, 12): d.line((x, 15, x, 6), fill=hx('6a8a3a')); d.rectangle((x, 4, x, 6), fill=hx('6a4a2a'))
    return im
def rough(seed=14): return noise_tile('5a6a42', ['4a5a36', '6a6a4a', '7a7a5a'], seed, 0.3)
def cave_floor(seed=15): return noise_tile('16141a', ['1e1c24', '0e0c12', '222028'], seed, 0.2)
def cave_wall(seed=16):
    im = noise_tile('2a2630', ['221e28', '342e3a', '1a1620'], seed, 0.3); d = ImageDraw.Draw(im)
    for y in (4, 10): d.line((0, y, 15, y), fill=hx('1a1620'))
    d.line((5, 0, 5, 4), fill=hx('1a1620')); d.line((11, 4, 11, 10), fill=hx('1a1620')); d.line((3, 10, 3, 15), fill=hx('1a1620')); return im
def cliff_top(seed=17):
    im = noise_tile('5a5650', ['4a4640', '6a665e'], seed, 0.3); d = ImageDraw.Draw(im); d.line((0, 0, 15, 0), fill=hx('8a867e')); d.line((0, 1, 15, 1), fill=hx('7a766e')); return im
def cliff_face(seed=18):
    im = noise_tile('3e3a38', ['34302e', '4a4644', '2a2624'], seed, 0.3); d = ImageDraw.Draw(im)
    for x in (2, 7, 12): d.line((x, 0, x + 1, 15), fill=hx('2a2624'))
    return im

TILES = [("trawa", grass(1)), ("trawa_2", grass(21)), ("kwiaty_czerwone", flowers('e04a4a', 31)), ("kwiaty_zolte", flowers('f0d040', 32)),
         ("kwiaty_niebieskie", flowers('6a8af0', 33)), ("sciezka", path()), ("kamienna_sciezka", stones()), ("woda", water()),
         ("woda_gleboka", water(6, True)), ("brzeg_woda_pd", shore('S')), ("brzeg_woda_pn", shore('N')), ("brzeg_woda_zach", shore('W')),
         ("brzeg_woda_wsch", shore('E')), ("zywoplot", hedge()), ("kamien", rock_tile()), ("lilia_wodna", lily()), ("trzciny", reeds()),
         ("skalista_trawa", rough()), ("klif_gora", cliff_top()), ("klif_sciana", cliff_face()), ("jaskinia_podloga", cave_floor()), ("jaskinia_sciana", cave_wall())]
IDX = {n: i for i, (n, _) in enumerate(TILES)}
COLS = 8
sheet = Image.new('RGBA', (COLS * T, math.ceil(len(TILES) / COLS) * T), (0, 0, 0, 0))
for i, (n, im) in enumerate(TILES): sheet.paste(im, ((i % COLS) * T, (i // COLS) * T))
sheet.save('tileset.png')

# --- obiekty (większe sprite'y) ---
def tree(kind):
    im = Image.new('RGBA', (32, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((6, 40, 26, 46), fill=(0, 0, 0, 90)); d.rectangle((13, 28, 18, 43), fill=hx('5a3a22')); d.line((13, 28, 13, 43), fill=hx('7a5232'))
    if kind == 'dab':
        for (x0, y0, x1, y1, c) in ((2, 8, 30, 34, '2e6a2a'), (4, 4, 26, 28, '3a7a32'), (8, 2, 22, 18, '4a8a3e'), (8, 6, 14, 12, '5aa04a')): d.ellipse((x0, y0, x1, y1), fill=hx(c))
    elif kind == 'wisnia':
        for (x0, y0, x1, y1, c) in ((2, 8, 30, 34, 'c86a8a'), (4, 4, 26, 28, 'e08aa8'), (8, 3, 22, 18, 'f0aac0'), (9, 6, 14, 11, 'ffd0e0')): d.ellipse((x0, y0, x1, y1), fill=hx(c))
    else:  # świerk
        for i, c in enumerate(('1e4a2a', '2a5a32', '346a3a')):
            y = 4 + i * 9; d.polygon([(16, y), (3 + i, y + 18), (29 - i, y + 18)], fill=hx(c))
    return im
def bush():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((1, 11, 15, 15), fill=(0, 0, 0, 80)); d.ellipse((1, 3, 15, 14), fill=hx('2e6a2a')); d.ellipse((3, 3, 11, 10), fill=hx('4a8a3e'))
    for p in ((5, 6), (10, 8), (7, 11)): d.point(p, fill=hx('e04a4a'))
    return im
def fountain():
    im = Image.new('RGBA', (48, 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((2, 12, 46, 38), fill=hx('9a968e')); d.ellipse((5, 14, 43, 34), fill=hx('2a5a8a')); d.ellipse((8, 16, 30, 26), fill=hx('3a6a9a'))
    d.rectangle((21, 4, 27, 24), fill=hx('bab6ae')); d.ellipse((17, 2, 31, 8), fill=hx('cac6be'))
    for x in (18, 24, 30): d.line((24, 3, x, 14), fill=hx('a8d8f8'))
    return im
def cave_mouth():
    im = Image.new('RGBA', (64, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 63, 47), fill=hx('3e3a38'))
    for x in range(0, 64, 5): d.line((x, 0, x + 2, 47), fill=hx('34302e'))
    d.ellipse((10, 8, 54, 70), fill=hx('1a1620')); d.ellipse((14, 12, 50, 70), fill=hx('0a0810')); d.ellipse((20, 18, 44, 70), fill=hx('030206'))
    for (x, y) in ((12, 12), (50, 14), (8, 30), (56, 34)): d.ellipse((x - 4, y - 3, x + 4, y + 3), fill=hx('5a5650'))
    d.line((14, 10, 16, 18), fill=hx('6a8a3a')); d.line((48, 10, 47, 20), fill=hx('6a8a3a'))  # pnącza
    return im
OBJS = [("drzewo_dab", tree('dab')), ("drzewo_wisnia", tree('wisnia')), ("drzewo_swierk", tree('swierk')), ("krzew", bush()), ("fontanna", fountain()), ("wejscie_jaskini", cave_mouth())]
ow = sum(o.width for _, o in OBJS) + 4 * len(OBJS); objs = Image.new('RGBA', (ow, 48), (0, 0, 0, 0)); x = 0; OPOS = {}
for n, o in OBJS: objs.paste(o, (x, 48 - o.height)); OPOS[n] = (x, 48 - o.height, o.width, o.height); x += o.width + 4
objs.save('objects.png')

# --- podgląd całej mapy 120×26 kafli ---
MW, MH = 120, 26; R = random.Random(42); g = [[IDX['trawa'] if R.random() < 0.7 else IDX['trawa_2'] for _ in range(MW)] for _ in range(MH)]
def setr(x0, y0, x1, y1, n):
    for y in range(max(0, y0), min(MH, y1)):
        for x in range(max(0, x0), min(MW, x1)): g[y][x] = IDX[n]
# ogród (0–38): żywopłoty, rabaty, kamienna aleja do fontanny
setr(0, 0, 40, 1, 'zywoplot'); setr(0, MH - 1, 40, MH, 'zywoplot'); setr(0, 0, 1, MH, 'zywoplot')
setr(1, 12, 40, 14, 'kamienna_sciezka')
for i, (x, y) in enumerate(((4, 4), (12, 4), (24, 4), (32, 4), (4, 17), (12, 17), (24, 17), (32, 17))):
    setr(x, y, x + 5, y + 4, ['kwiaty_czerwone', 'kwiaty_zolte', 'kwiaty_niebieskie'][i % 3])
# jezioro (38–86) z brzegami, ścieżka wzdłuż południowego brzegu
LX0, LX1 = 40, 86
for x in range(LX0, LX1):
    top = 1 + int(2 * math.sin(x * 0.2)); bot = 16 + int(2 * math.sin(x * 0.15 + 1))
    for y in range(top, bot):
        g[y][x] = IDX['woda_gleboka'] if ((x - 63) / 19) ** 2 + ((y - 8.5) / 5.5) ** 2 < 1 else IDX['woda']
    g[bot][x] = IDX['brzeg_woda_pn'] if R.random() > 0.15 else IDX['trzciny']
    if top > 0: g[top - 1][x] = IDX['brzeg_woda_pd']
for y in range(2, 16): 
    if g[y][LX0] != IDX['woda'] or True: g[y][LX0 - 1] = IDX['brzeg_woda_wsch']; g[y][LX1] = IDX['brzeg_woda_zach']
for _ in range(14):
    x, y = R.randrange(LX0 + 2, LX1 - 2), R.randrange(4, 14)
    if g[y][x] in (IDX['woda'], IDX['woda_gleboka']): g[y][x] = IDX['lilia_wodna']
for x in range(38, 92):
    y = 19 + int(1.5 * math.sin(x * 0.18)); g[y][x] = IDX['sciezka']; g[y + 1][x] = IDX['sciezka']
# skały i klif z jaskinią (86–120)
for y in range(MH):
    for x in range(86, MW):
        if R.random() < (x - 86) / 40: g[y][x] = IDX['skalista_trawa']
setr(100, 0, MW, 1, 'klif_gora'); setr(100, 1, MW, 22, 'klif_sciana'); setr(99, 0, 100, 22, 'klif_gora')
for x in range(90, 104):
    y = 19 + int(1.5 * math.sin(x * 0.18)); g[y][x] = IDX['sciezka']; g[y + 1][x] = IDX['sciezka']
setr(104, 17, 112, 22, 'jaskinia_podloga')
img = Image.new('RGBA', (MW * T, MH * T))
for y in range(MH):
    for x in range(MW): img.paste(TILES[g[y][x]][1], (x * T, y * T))
def put(n, px, py):
    o = dict(OBJS)[n]; img.alpha_composite(o, (int(px - o.width / 2), int(py - o.height)))
put('fontanna', 20 * T, 15 * T)
for x in (3, 9, 30, 36): put('drzewo_wisnia', x * T, 11 * T); put('drzewo_dab', x * T + 8, 25 * T)
for x in range(2, 38, 5): put('krzew', x * T, 22 * T + 4)
for x in (44, 56, 70, 82): put('drzewo_dab', x * T, 25 * T)
for x in (88, 93, 97): put('drzewo_swierk', x * T, (8 + x % 5) * T)
for (x, y) in ((90, 23), (95, 15), (98, 24), (113, 24), (117, 23)): img.alpha_composite(TILES[IDX['kamien']][1], (x * T, y * T))
put('wejscie_jaskini', 108 * T, 22 * T)
# ciemność narasta w stronę jaskini + zaproszenie światłem
dark = Image.new('RGBA', img.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(dark)
for x in range(0, img.width, 4):
    a = int(max(0, (x - 84 * T) / (36 * T)) ** 1.5 * 150); dd.rectangle((x, 0, x + 3, img.height), fill=(10, 8, 20, a))
img.alpha_composite(dark)
img.save('overview_map1.png')
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
lab = img.copy(); d = ImageDraw.Draw(lab)
for (x, t) in ((6, "1. OGRÓD"), (52, "2. ŚCIEŻKA NAD JEZIOREM"), (100, "3. WEJŚCIE DO JASKINI")):
    d.text((x * T + 2, MH * T - 30 + 2), t, fill=(0, 0, 0), font=f); d.text((x * T, MH * T - 30), t, fill=(255, 240, 200), font=f)
lab.save('overview_map1_opis.png')
lab.resize((lab.width // 2, lab.height // 2), Image.NEAREST).save('overview_map1_maly.png')
with open('tiles.txt', 'w') as fh:
    for i, (n, _) in enumerate(TILES): fh.write(f"{i}\t{n}\t({(i % COLS) * T},{(i // COLS) * T})\n")
    for n, p in OPOS.items(): fh.write(f"obj\t{n}\t{p}\n")
