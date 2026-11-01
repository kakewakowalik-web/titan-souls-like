# Mapa 1 v2 (grywalna): ogród -> brzeg jeziora -> jaskinia. python3 make_map1.py
# Wynik: tileset.png, map1_ground.png, map1_canopy.png (nad graczem), map1.json (kolizje, spawn), podglądy.
import random, math, json
from PIL import Image, ImageDraw, ImageFont
T = 16; MW, MH = 120, 40
R = random.Random(7)
def hx(c, a=255): return tuple(int(c[i:i+2], 16) for i in (0, 2, 4)) + (a,)
# Paleta: stonowana, lekko szara zieleń, ciepły kamień, turkusowa woda (inspiracja Titan Souls)
P = {
 'grass': ['5e7a4a', '56724a', '668252', '4e6a42'], 'grass_hi': '7a945e',
 'path': ['a8956e', '9c8964', 'b4a078', '8e7b58'], 'stone': ['9a968a', '8a867a', 'aaa69a'], 'stone_gap': '6a675e',
 'water': ['3e6e78', '386470', '44767e'], 'deep': ['2c5460', '284c58', '30586a'], 'foam': 'a8c8c0', 'sand': 'b8a880', 'bank': '2a3e3a',
 'hedge': ['3a5a36', '34522f', '42643c'], 'hedge_hi': '56744a', 'hedge_lo': '243a22',
 'rock': ['7e7a6e', '726e62', '8a867a'], 'cliff_top': ['8a8474', '7e786a'], 'cliff': ['5a554c', '504b44', '625d54'], 'cliff_lo': '3a3632',
 'cave': ['1a1820', '16141c', '1e1c24'], 'cave_wall': ['2c2832', '24202a', '343040'],
 'flower': ['c8604e', 'd8b04e', '7e8ac8', 'e0d8c8'],
}
def noise(im, x0, y0, cols, dens=0.35, seed=0):
    r = random.Random(seed)
    for y in range(T):
        for x in range(T):
            im.putpixel((x0 + x, y0 + y), hx(cols[0] if r.random() > dens else r.choice(cols[1:])))
# --- typy kafli ---
TYPES = ['trawa', 'sciezka', 'aleja', 'woda', 'gleboka_woda', 'zywoplot', 'kwiaty', 'skala', 'klif_gora', 'klif', 'jaskinia', 'sciana_jaskini', 'skalista_trawa']
SOLID = {'woda', 'gleboka_woda', 'zywoplot', 'skala', 'klif_gora', 'klif', 'sciana_jaskini'}
g = [['trawa'] * MW for _ in range(MH)]
def rect(x0, y0, x1, y1, t):
    for y in range(max(0, y0), min(MH, y1)):
        for x in range(max(0, x0), min(MW, x1)): g[y][x] = t
# granice
rect(0, 0, MW, 2, 'zywoplot'); rect(0, MH - 2, MW, MH, 'zywoplot'); rect(0, 0, 2, MH, 'zywoplot')
# OGRÓD (2–36): kamienna aleja 3 kafle, plac z fontanną, rabaty z przejściami
rect(2, 20, 40, 23, 'aleja'); rect(14, 15, 27, 28, 'aleja')
for (x, y) in ((4, 6), (4, 30), (30, 6), (30, 30)): rect(x, y, x + 6, y + 4, 'kwiaty')
for (x, y) in ((14, 6), (20, 6), (14, 32), (20, 32)): rect(x, y, x + 4, y + 3, 'kwiaty')
rect(2, 12, 12, 13, 'zywoplot'); rect(29, 12, 37, 13, 'zywoplot'); rect(2, 28, 12, 29, 'zywoplot'); rect(29, 28, 37, 29, 'zywoplot')
rect(36, 2, 38, 18, 'zywoplot'); rect(36, 25, 38, MH - 2, 'zywoplot')  # brama ogrodu: przerwa 7 kafli na aleję
# JEZIORO (40–92): elipsa, ścieżka 4 kafle po południowym brzegu
for y in range(2, 28):
    for x in range(40, 94):
        e = ((x - 66) / 26) ** 2 + ((y - 13) / (11 + 1.5 * math.sin(x * 0.3))) ** 2
        if e < 1: g[y][x] = 'gleboka_woda' if e < 0.45 else 'woda'
for x in range(38, 104):
    yc = 30 + int(round(1.5 * math.sin(x * 0.12)))
    for y in range(yc - 2, yc + 2):
        if g[y][x] not in ('woda', 'gleboka_woda'): g[y][x] = 'sciezka'
# las na południe od ścieżki = ściana (drzewa)
TREES = []
for x in range(40, 100, 3):
    TREES.append(('dab' if x % 2 else 'swierk', x + R.randint(0, 1), 36 + R.randint(-1, 0)))
for x in range(42, 92, 7): TREES.append(('swierk', x, 3 + R.randint(0, 1)))
# SKAŁY + KLIF + JASKINIA (96–120)
for y in range(2, MH - 2):
    for x in range(92, 104):
        if g[y][x] == 'trawa' and R.random() < (x - 92) / 14: g[y][x] = 'skalista_trawa'
rect(104, 2, MW, 26, 'klif'); rect(104, 2, MW, 4, 'klif_gora'); rect(103, 2, 104, 26, 'klif_gora')
rect(108, 20, 113, 26, 'jaskinia')  # wejście 5 kafli szerokie
rect(106, 6, 118, 20, 'jaskinia'); rect(106, 6, 118, 7, 'sciana_jaskini')
for (x, y) in ((106, 9), (107, 9), (116, 12), (117, 12), (110, 14), (111, 14)): g[y][x] = 'sciana_jaskini'
rect(104, 26, 120, 34, 'skalista_trawa'); rect(100, 28, 113, 32, 'sciezka')
rect(118, 2, MW, MH, 'klif'); rect(104, 34, MW, MH - 2, 'skala')
for (x, y) in ((95, 24), (98, 20), (100, 35), (96, 33), (101, 25)): g[y][x] = 'skala'
ROCKS = [(95, 24), (98, 20), (100, 35), (96, 33), (101, 25)]
# drzewa w ogrodzie (wiśnie) — z przerwami
for (x, y) in ((6, 16), (32, 16), (6, 25), (32, 25), (10, 36), (28, 36), (10, 4), (28, 4)): TREES.append(('wisnia', x, y))
FOUNTAIN = (20, 21)
# --- render podłoża (piksele) ---
W, H = MW * T, MH * T
ground = Image.new('RGBA', (W, H)); canopy = Image.new('RGBA', (W, H), (0, 0, 0, 0))
def t_at(x, y): return g[y][x] if 0 <= x < MW and 0 <= y < MH else 'zywoplot'
colmap = {'trawa': P['grass'], 'sciezka': P['path'], 'woda': P['water'], 'gleboka_woda': P['deep'], 'zywoplot': P['hedge'],
          'skala': P['rock'], 'klif_gora': P['cliff_top'], 'klif': P['cliff'], 'jaskinia': P['cave'], 'sciana_jaskini': P['cave_wall'],
          'skalista_trawa': ['6a7254', '5e664a', '7a7a62', '565e44'], 'kwiaty': P['grass'], 'aleja': P['stone']}
for ty in range(MH):
    for tx in range(MW):
        t = g[ty][tx]; noise(ground, tx * T, ty * T, colmap[t], 0.3, ty * 1000 + tx)
        d = ImageDraw.Draw(ground); X, Y = tx * T, ty * T
        if t == 'aleja':
            d.line((X, Y + 7, X + 15, Y + 7), fill=hx(P['stone_gap'])); d.line((X, Y + 15, X + 15, Y + 15), fill=hx(P['stone_gap']))
            d.line((X + (0 if ty % 2 else 8), Y, X + (0 if ty % 2 else 8), Y + 7), fill=hx(P['stone_gap'])); d.line((X + (8 if ty % 2 else 0), Y + 8, X + (8 if ty % 2 else 0), Y + 15), fill=hx(P['stone_gap']))
        if t == 'kwiaty':
            r = random.Random(tx * 7 + ty)
            for _ in range(4):
                x, y = X + r.randrange(2, 14), Y + r.randrange(2, 14); c = P['flower'][(tx + ty) % 4]
                for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)): ground.putpixel((x + dx, y + dy), hx(c))
                ground.putpixel((x, y), hx('f0e0a0'))
        if t == 'trawa' and R.random() < 0.25:
            x, y = X + R.randrange(2, 14), Y + R.randrange(3, 14); ground.putpixel((x, y), hx(P['grass_hi'])); ground.putpixel((x, y - 1), hx(P['grass_hi']))
        if t == 'zywoplot':  # wypukły: jasna góra, ciemny dół
            if t_at(tx, ty - 1) != 'zywoplot': d.rectangle((X, Y, X + 15, Y + 2), fill=hx(P['hedge_hi']))
            if t_at(tx, ty + 1) != 'zywoplot': d.rectangle((X, Y + 12, X + 15, Y + 15), fill=hx(P['hedge_lo']))
        if t == 'klif':
            for x in (3, 9, 14): d.line((X + x, Y, X + x - 1, Y + 15), fill=hx(P['cliff_lo']))
            if t_at(tx, ty + 1) not in ('klif', 'klif_gora', 'sciana_jaskini'): d.rectangle((X, Y + 13, X + 15, Y + 15), fill=hx('2a2622'))
        if t == 'klif_gora': d.line((X, Y, X + 15, Y), fill=hx('a8a290'))
        if t == 'sciana_jaskini': d.rectangle((X, Y + 12, X + 15, Y + 15), fill=hx('0e0c12'))
        # brzeg: piasek na lądzie, ciemna krawędź w wodzie
        if t in ('woda', 'gleboka_woda'):
            for (dx, dy, box) in ((0, -1, (0, 0, 15, 3)), (0, 1, (0, 13, 15, 15)), (-1, 0, (0, 0, 2, 15)), (1, 0, (13, 0, 15, 15))):
                if t_at(tx + dx, ty + dy) not in ('woda', 'gleboka_woda'):
                    b = box; d.rectangle((X + b[0], Y + b[1], X + b[2], Y + b[3]), fill=hx(P['bank']))
                    if dy == -1: d.line((X, Y + 4, X + 15, Y + 4), fill=hx(P['foam']))
        elif t not in SOLID:
            for (dx, dy, box) in ((0, -1, (0, 0, 15, 1)), (0, 1, (0, 14, 15, 15)), (-1, 0, (0, 0, 1, 15)), (1, 0, (14, 0, 15, 15))):
                if t_at(tx + dx, ty + dy) in ('woda', 'gleboka_woda'): d.rectangle((X + box[0], Y + box[1], X + box[2], Y + box[3]), fill=hx(P['sand']))
            if t_at(tx, ty - 1) in ('zywoplot', 'klif', 'skala', 'sciana_jaskini', 'klif_gora'):  # cień ściany na podłodze
                ground.alpha_composite(Image.new('RGBA', (T, 4), (0, 0, 0, 70)), (X, Y))
# lilie
for _ in range(18):
    x, y = R.randrange(44, 90), R.randrange(4, 24)
    if g[y][x] == 'woda':
        d = ImageDraw.Draw(ground); d.ellipse((x * T + 3, y * T + 5, x * T + 11, y * T + 11), fill=hx('5a8a4a')); d.point((x * T + 9, y * T + 6), fill=hx('e8b8c8'))
# kamienie (obiekty)
d = ImageDraw.Draw(ground)
for (x, y) in ROCKS:
    X, Y = x * T, y * T; d.ellipse((X, Y + 10, X + 16, Y + 16), fill=(0, 0, 0, 90)); d.ellipse((X + 1, Y + 1, X + 15, Y + 14), fill=hx('7e7a6e'))
    d.ellipse((X + 3, Y + 2, X + 11, Y + 8), fill=hx('9a968a')); d.arc((X + 1, Y + 1, X + 15, Y + 14), 10, 170, fill=hx('3e3a34'))
# fontanna (solid 3×3)
fx, fy = FOUNTAIN; X, Y = fx * T - 24, fy * T - 24
d.ellipse((X + 2, Y + 6, X + 70, Y + 70), fill=(0, 0, 0, 80)); d.ellipse((X, Y, X + 66, Y + 62), fill=hx('8a867a')); d.ellipse((X + 5, Y + 5, X + 61, Y + 57), fill=hx('3e6e78'))
d.ellipse((X + 12, Y + 10, X + 36, Y + 26), fill=hx('4e7e88')); d.rectangle((X + 29, Y + 16, X + 37, Y + 40), fill=hx('aaa69a')); d.ellipse((X + 23, Y + 12, X + 43, Y + 20), fill=hx('bab6aa'))
for i in range(5): d.line((X + 33, Y + 13, X + 22 + i * 6, Y + 30), fill=hx('b8d8d0'))
for y in range(fy - 1, fy + 2):
    for x in range(fx - 1, fx + 3): g[y][x] = 'fontanna'
SOLID.add('fontanna')
# wejście do jaskini: łuk w klifie
d = ImageDraw.Draw(ground); X, Y = 108 * T, 19 * T
d.ellipse((X - 6, Y - 10, X + 5 * T + 6, Y + 40), fill=hx('2a2622')); d.ellipse((X, Y - 4, X + 5 * T, Y + 44), fill=hx('0c0a10'))
d.rectangle((X, Y + 16, X + 5 * T - 1, Y + 7 * T), fill=hx('0c0a10'))
for (x, y) in ((X - 4, Y), (X + 5 * T, Y + 4)): d.line((x + 2, y - 8, x + 4, y + 20), fill=hx('5a7a46'), width=2)  # pnącza
# drzewa: pień (solid, na ziemi) + korona (nad graczem)
def tree(kind, tx, ty):
    cx, by = tx * T + 8, ty * T + 14
    d = ImageDraw.Draw(ground); d.ellipse((cx - 11, by - 4, cx + 11, by + 3), fill=(0, 0, 0, 90)); d.rectangle((cx - 3, by - 14, cx + 3, by), fill=hx('5a4230')); d.line((cx - 3, by - 14, cx - 3, by), fill=hx('76583e'))
    c = ImageDraw.Draw(canopy)
    if kind == 'swierk':
        for i, col in enumerate(('2e4a36', '36553c', '406044')): y = by - 46 + i * 9; c.polygon([(cx, y), (cx - 13 + i, y + 20), (cx + 13 - i, y + 20)], fill=hx(col))
    else:
        cols = ('4a6a3e', '587a48', '668a52', '7a9a5e') if kind == 'dab' else ('a8707e', 'b8848e', 'c898a0', 'd8b0b4')
        for (x0, y0, x1, y1), col in zip(((-15, -40, 15, -14), (-13, -44, 11, -20), (-9, -46, 7, -28), (-7, -42, -1, -36)), cols):
            c.ellipse((cx + x0, by + y0, cx + x1, by + y1), fill=hx(col))
    if 0 <= ty < MH and 0 <= tx < MW: g[ty][tx] = 'pien'
SOLID.add('pien')
for k, x, y in TREES: tree(k, x, y)
ground.save('map1_ground.png'); canopy.save('map1_canopy.png')
# --- dane gry ---
solid = [''.join('1' if g[y][x] in SOLID else '0' for x in range(MW)) for y in range(MH)]
zones = {"ogrod": [0, 38], "jezioro": [38, 96], "jaskinia": [96, 120]}
water = [''.join('1' if g[y][x] in ('woda', 'gleboka_woda') else '0' for x in range(MW)) for y in range(MH)]
json.dump({"water": water, "tile": T, "w": MW, "h": MH, "spawn": [8 * T, 21 * T + 8], "solid": solid, "zones": zones,
           "cave_rect": [106 * T, 6 * T, 12 * T, 20 * T], "targets": [[24 * T, 10 * T], [66 * T, 33 * T], [112 * T, 12 * T]]},
          open('map1.json', 'w'))
# --- tileset (wzorce do edytora) ---
ts = Image.new('RGBA', (8 * T, 2 * T))
for i, t in enumerate(TYPES):
    for ty in range(MH):
        for tx in range(MW):
            if g[ty][tx] == t and 2 < tx < MW - 3 and all(g[ty + dy][tx + dx] == t for dx in (-1, 0, 1) for dy in (-1, 0, 1) if 0 <= ty + dy < MH):
                ts.paste(ground.crop((tx * T, ty * T, tx * T + T, ty * T + T)), ((i % 8) * T, (i // 8) * T)); break
        else: continue
        break
ts.save('tileset.png')
with open('tiles.txt', 'w') as fh:
    for i, t in enumerate(TYPES): fh.write(f"{i}\t{t}\t{'KOLIZJA' if t in SOLID else 'chodzenie'}\n")
# --- podglądy ---
ov = ground.copy(); ov.alpha_composite(canopy)
dk = Image.new('RGBA', ov.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(dk)
for x in range(0, W, 4):
    a = int(max(0.0, (x - 90 * T) / (30 * T)) ** 1.4 * 140); dd.rectangle((x, 0, x + 3, H), fill=(8, 6, 16, a))
cx, cy, cw_, ch_ = 106 * T, 6 * T, 12 * T, 20 * T; dd.rectangle((cx, cy, cx + cw_, cy + ch_), fill=(4, 3, 8, 200))
ov.alpha_composite(dk); ov.save('overview_map1.png')
lab = ov.copy(); d = ImageDraw.Draw(lab); f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
for (x, y, t) in ((4, 37, "1. OGRÓD (start)"), (50, 33.5, "2. ŚCIEŻKA NAD JEZIOREM"), (96, 37, "3. JASKINIA")):
    d.text((x * T + 2, y * T + 2), t, fill=(0, 0, 0), font=f); d.text((x * T, y * T), t, fill=(255, 240, 200), font=f)
d.ellipse((8 * T - 6, 21 * T + 2, 8 * T + 6, 21 * T + 14), outline=(255, 230, 120), width=3)
lab.save('overview_map1_opis.png'); lab.resize((W // 2, H // 2), Image.LANCZOS).save('overview_map1_maly.png')
