# Generator propozycji sprite'ów (idle, przód). python3 make.py
from PIL import Image, ImageDraw, ImageFont
FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
S = {
"a_titan_chunky": ("Krępy 16-bit (Titan Souls)", {'k':'1a1620','s':'e8b48a','h':'6a3a2a','t':'8a2f3a','T':'5e1f2a','p':'3a3040','b':'2a2228','w':'c8b070'}, [
"......kkkk......",
".....khhhhk.....",
"....khhhhhhk....",
"....khsssshk....",
"....kskssksk....",
"....ksssssk.....",
"...kTtttttTk....",
"..ksTtwttttTsk..",
"..ksTttwtttTsk..",
"...kTtttwttTk...",
"....kpppppk.....",
"....kppkppk.....",
"....kbbkbbk.....",
"....kkk.kkk....."]),
"b_zelda_thin": ("Smukły jak Zelda LttP", {'k':'20202a','s':'f0c8a0','h':'d8a040','g':'3a8a3a','G':'25602a','p':'c8a878','b':'6a4020','w':'e0e0e0'}, [
".......kk.......",
"......kggk......",
".....kgggGk.....",
"....khhhhhk.....",
"....kskssk......",
"....kssssk......",
".....kGgGk......",
"....kgGgGgk.....",
"....ksgGgsk.....",
".....kbbbk......",
".....kppk.......",
".....kp.kp......",
".....kb.kb......",
".....kk.kk......"]),
"c_dark_silhouette": ("Mroczna sylwetka", {'k':'0a0a0e','d':'1c1c26','e':'ffd65a','r':'7a2a2a'}, [
".......kk.......",
"......kddk......",
".....kddddk.....",
".....kdeedk.....",
".....kddddk.....",
"....kddddddk....",
"...kddddddddk...",
"...kddrddddk....",
"...kdddddddk....",
"....kddddddk....",
"....kdddddk.....",
"....kdk.kdk.....",
"....kdk.kdk.....",
"....kk..kk......"]),
"d_chibi": ("Słodki chibi", {'k':'2a2030','s':'ffd8c0','h':'a06040','c':'ff9aa8','t':'7ab8e8','p':'4a5a8a','w':'ffffff'}, [
"....kkkkkkk.....",
"...khhhhhhhk....",
"..khhhhhhhhhk...",
"..khsssssssh k..".replace(' ','.'),
"..ksswksswssk...",
"..kssksskssk....",
"..kcsssssscsk...",
"...ksssssssk....",
"....kttttttk....",
"...ksttttttsk...",
"....kppppk......",
"....kk..kk......"]),
"e_armored_knight": ("Rycerz w zbroi", {'k':'14161c','m':'a8b0bc','M':'6a7280','v':'2a2e38','r':'b03a3a','b':'4a3a2a','g':'d8b040'}, [
"......krrk......",
".....kmmmmk.....",
"....kmmmmmmk....",
"....kMvvvvMk....",
"....kmmmmmmk....",
"...kMmmmmmmMk...",
"..kmMmmgmmmMmk..",
"..kmMmmmmmmMmk..",
"...kMmmmmmmMk...",
"....kbbgbbbk....",
"....kMMkMMk.....",
"....kmmkmmk.....",
"....kMMkMMk.....",
"....kkk.kkk....."]),
"f_hooded_archer": ("Łucznik w kapturze", {'k':'161a14','c':'4a5a3a','C':'2e3a24','s':'d8a880','e':'f0f0d0','q':'8a5a30','w':'c8a060','b':'3a2a1a'}, [
".......kk.......",
"......kcck......",
".....kccCck.....",
"....kcCssCck....",
"....kcseseck....",
"....kCsssCk.....",
"...kcccccccqk...",
"..kcCcccccCcqk..",
"..ksCccwccCsqk..",
"...kCcccccCkq...",
"....kbbbbbk.....",
"....kbbkbbk.....",
"....kbbkbbk.....",
"....kkk.kkk....."]),
}
SC = 8
tiles = []
for key, (name, pal, rows) in S.items():
    w = 16; h = len(rows)
    im = Image.new('RGBA', (w, 20), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r[:16]):
            if ch in pal: im.putpixel((x, y + (20 - h)), tuple(int(pal[ch][i:i+2], 16) for i in (0, 2, 4)) + (255,))
    im.save(f'{key}.png')
    big = Image.new('RGB', (w * SC, 20 * SC), (47, 45, 41)); big.paste(im.resize((w * SC, 20 * SC), Image.NEAREST), (0, 0), im.resize((w * SC, 20 * SC), Image.NEAREST))
    big.save(f'{key}_x8.png'); tiles.append((key, name, big, im))
cw, ch = 16 * SC + 40, 20 * SC + 60
sheet = Image.new('RGB', (cw * 3, ch * 2), (27, 26, 32)); d = ImageDraw.Draw(sheet)
for i, (key, name, big, im) in enumerate(tiles):
    x, y = (i % 3) * cw + 20, (i // 3) * ch + 14
    sheet.paste(big, (x, y))
    sheet.paste(im, (x + big.width - 16, y + big.height + 6), im)  # rozmiar 1:1
    d.text((x, y + big.height + 6), f"{key[0].upper()}: {name}", fill=(232, 217, 160), font=FONT)
    d.text((x, y + big.height + 22), "(obok 1:1)", fill=(125, 117, 99), font=FONT)
sheet.save('compare.png')
