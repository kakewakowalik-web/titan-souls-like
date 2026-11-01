# 5 różnych postaci (p1–p5). python3 make_five.py
src = open('make.py').read(); exec(src[:src.index('STYLES =')])
dk = open('make_dark.py').read(); exec(dk[dk.index('D0, D1'):dk.index('def c2')])

def legs(s, c, boot):
    s.rect(8, 25, 10, 29, c, 'legL'); s.rect(13, 25, 15, 29, c, 'legR')
    s.rect(7, 28, 10, 29, boot, 'bL'); s.rect(13, 28, 16, 29, boot, 'bR')
def bow(s, x, wood, string, side=1):
    s.line([(x, 10), (x + side * 2, 16), (x + side * 2, 24), (x, 30)], wood, 'bow'); s.line([(x, 10), (x, 30)], string, 'str')

def p1():  # Leśna tropicielka — jasna zieleń, ruda warkocz
    s = Spr(); legs(s, '6a4a2a', '3a2414')
    s.rect(16, 7, 19, 16, '8a5a30', 'quiver'); s.line([(17, 6), (18, 4)], 'f0e0b0', 'fl', True); s.line([(19, 6), (20, 5)], 'e85a4a', 'fl', True)
    s.rect(8, 15, 15, 25, '5ab84a', 'tunic'); s.rect(7, 22, 16, 25, '5ab84a', 'skirt'); s.rect(8, 20, 15, 20, '6a4020', 'belt', True)
    s.rect(6, 16, 7, 21, '8ad87a', 'armL'); s.rect(16, 16, 17, 21, '8ad87a', 'armR')
    s.ell(6.5, 22.5, 1.3, 1.3, 'f0c8a0', 'hL'); s.ell(16.5, 22.5, 1.3, 1.3, 'f0c8a0', 'hR')
    bow(s, 4, 'a06a30', 'f0f0e0', -1)
    s.ell(12, 10, 5, 5, 'f0c8a0', 'face'); s.ell(12, 7, 5.5, 3.5, 'd8602a', 'hair'); s.rect(6, 7, 7, 13, 'd8602a', 'hL2')
    s.line([(17, 9), (18, 13), (18, 17)], 'd8602a', 'braid', False)
    s.line([(8, 5), (11, 4)], '8ad87a', 'leaf', True)
    s.put(10, 10, '2a5a2a', 'e', True); s.put(14, 10, '2a5a2a', 'e', True); s.put(9, 12, 'e8a090', 'c', True); s.put(15, 12, 'e8a090', 'c', True)
    shadow(s); return s.render(outline='1a2014')

def p2():  # Zwiadowca pustyni — piasek, turban, chusta
    s = Spr(); legs(s, 'c8a878', '6a4a2a')
    s.ell(12, 21, 7, 6, 'e0c890', 'robe'); s.rect(6, 21, 17, 26, 'e0c890', 'robe')
    s.line([(6, 17), (17, 25)], 'c04a2a', 'sash', True); s.rect(6, 24, 17, 24, '8a3a1a', 'belt', True)
    s.ell(4.5, 21, 1.5, 2, 'b07a50', 'hL'); s.ell(19.5, 21, 1.5, 2, 'b07a50', 'hR')
    bow(s, 21, '7a4a22', 'e8e0c8')
    s.ell(12, 10, 5.5, 5.5, 'b07a50', 'face'); s.ell(12, 7, 6.5, 4.5, 'f0e0c0', 'turban'); s.line([(6, 8), (18, 6)], 'd8c098', 'wrap', True)
    s.rect(7, 11, 17, 14, '3a8aa0', 'scarf'); s.line([(17, 12), (20, 15)], '3a8aa0', 'tail', False)
    s.rect(9, 9, 10, 9, '1a1410', 'e', True); s.rect(14, 9, 15, 9, '1a1410', 'e', True)
    s.put(12, 5, 'e0b030', 'gem', True)
    shadow(s); return s.render(outline='2a1e14')

def p3():  # Królewski łucznik — granat, złoto, peleryna
    s = Spr(); legs(s, 'f0f0f0', '2a2440')
    s.ell(12, 21, 8, 7, 'b02a3a', 'cape'); s.rect(4, 21, 20, 28, 'b02a3a', 'cape')
    s.rect(8, 15, 15, 25, '2a3a8a', 'doublet'); s.line([(11, 15), (11, 25)], 'e0b040', 'trim', True); s.line([(12, 15), (12, 25)], 'e0b040', 'trim', True)
    s.rect(8, 21, 15, 21, 'e0b040', 'belt', True)
    s.rect(6, 16, 7, 22, '3a4aa8', 'armL'); s.rect(16, 16, 17, 22, '3a4aa8', 'armR')
    bow(s, 20, 'e0b040', 'ffffff')
    s.ell(12, 10, 5, 5, 'f0d0b0', 'face'); s.ell(12, 7, 5.5, 3, 'f0e090', 'hair')
    s.rect(8, 3, 16, 5, 'e0b040', 'crown'); [s.put(x, 2, 'e0b040', 'cr', True) for x in (8, 12, 16)]; s.put(12, 4, 'c83a3a', 'ruby', True)
    s.put(10, 10, '2a3a6a', 'e', True); s.put(14, 10, '2a3a6a', 'e', True)
    s.rect(8, 14, 15, 15, 'ffffff', 'collar')
    shadow(s); return s.render(outline='14142a')

def p4():  # Łowca mrozu — futro, biel i lodowy błękit
    s = Spr(); legs(s, '5a6a80', 'e8f0f8')
    s.ell(12, 21, 8, 7, '6aa0d0', 'coat'); s.rect(5, 21, 19, 27, '6aa0d0', 'coat')
    s.rect(4, 26, 20, 27, 'f0f4f8', 'fur'); s.rect(11, 15, 13, 26, 'f0f4f8', 'furline')
    s.ell(4, 21, 2, 2.5, 'e8f0f8', 'mitL'); s.ell(20, 21, 2, 2.5, 'e8f0f8', 'mitR')
    bow(s, 2, '9ad8f0', 'ffffff', 1); s.put(4, 20, 'c8f4ff', 'ice', True)
    s.ell(12, 10, 7.5, 7, 'f0f4f8', 'hood'); s.ell(12, 11, 4.5, 4, 'f0c8b0', 'face')
    s.put(10, 11, '2a4a8a', 'e', True); s.put(14, 11, '2a4a8a', 'e', True); s.rect(9, 13, 15, 14, '4a7ab0', 'scarf')
    s.put(9, 12, 'f08a8a', 'c', True); s.put(15, 12, 'f08a8a', 'c', True)
    shadow(s); return s.render(outline='1a2a3a')

CH = [("p1_lesna_tropicielka", "P1: Leśna tropicielka", p1), ("p2_zwiadowca_pustyni", "P2: Zwiadowca pustyni", p2),
      ("p3_krolewski_lucznik", "P3: Królewski łucznik", p3), ("p4_lowca_mrozu", "P4: Łowca mrozu", p4),
      ("p5_cien_w_kapturze", "P5: Cień w kapturze", c1)]
SC = 6; DARK = (20, 19, 24); ARENA = (47, 45, 41)
cw, chh = W * SC + 90, H * SC + 50
sheet = Image.new('RGB', (cw * 5, chh), (16, 15, 20)); d = ImageDraw.Draw(sheet)
for i, (key, name, fn) in enumerate(CH):
    im = fn(); im.save(f'{key}.png')
    up = im.resize((W * SC, H * SC), Image.NEAREST)
    big = Image.new('RGB', up.size, ARENA); big.paste(up, (0, 0), up); big.save(f'{key}_x6.png')
    x = i * cw + 10; sheet.paste(big, (x, 10))
    for j, col in enumerate((DARK, ARENA, (140, 130, 110))):
        sm = Image.new('RGB', (W * 2 + 4, H * 2 + 4), col); s2 = im.resize((W * 2, H * 2), Image.NEAREST); sm.paste(s2, (2, 2), s2)
        sheet.paste(sm, (x + up.width + 4, 10 + j * (H * 2 + 6)))
    d.text((x, H * SC + 18), name, fill=(232, 217, 160), font=FONT)
sheet.save('compare_five.png')
