# Ciemna linia: 5 postaci w stylu C. python3 make_dark.py
src = open('make.py').read(); exec(src[:src.index('STYLES =')])
D0, D1, D2 = '1c1c26', '12121a', '22222e'

def eyes(s, y, c, c2, xs=(10, 14)):
    for x in xs: s.put(x, y, c, 'eye', True); s.put(x, y + 1, c2, 'eye2', True)

def c1():  # Łowczyni w kapturze — klasyczny łuk, długi płaszcz
    s = Spr()
    s.ell(12, 21, 7, 7, D0, 'cloak'); s.rect(5, 21, 18, 29, D0, 'cloak')
    for x in (8, 12, 16): s.line([(x, 23), (x - 1, 29)], D1, 'fold')
    s.ell(12, 10, 6, 6, D2, 'hood'); s.line([(12, 3), (13, 1)], D2, 'hood', False)
    s.ell(12, 11, 4, 3.5, '06060a', 'void', True); eyes(s, 11, '7ae8ff', '2a7a90')
    s.line([(20, 9), (22, 15), (22, 24), (20, 30)], '2a3440', 'bow'); s.line([(20, 9), (20, 30)], '7ab8c8', 'str')
    s.ell(12, 18, 1.2, 1.2, '3ab8d8', 'clasp')
    shadow(s); return s.render(outline='050507', rim='7ad0e8', hi=1.4)

def c2():  # Wysoki łowca z włócznią i łukiem na plecach
    s = Spr()
    s.line([(4, 1), (4, 30)], '3a3440', 'spear'); s.line([(3, 0), (4, -1), (5, 0)], 'b8c0d0', 'tip'); s.rect(3, 0, 5, 2, 'b8c0d0', 'tip', True)
    s.line([(17, 4), (20, 10), (20, 20), (17, 24)], '2a2230', 'bow'); s.line([(17, 4), (17, 24)], '9a8ab0', 'str')
    s.rect(8, 14, 16, 27, D0, 'body'); s.rect(7, 16, 17, 19, D2, 'shoulder')
    s.rect(9, 27, 10, 30, D1, 'legL'); s.rect(14, 27, 15, 30, D1, 'legR')
    s.rect(5, 17, 6, 22, D0, 'arm'); s.ell(12, 8, 4, 5, D2, 'head'); s.rect(8, 9, 16, 10, D1, 'mask', True)
    s.line([(9, 3), (8, 0)], D2, 'horn', False); s.line([(15, 3), (16, 0)], D2, 'horn', False)
    eyes(s, 9, 'c8a0ff', '6a4a9a', (10, 14))
    s.line([(8, 21), (16, 21)], '2e2a3a', 'belt', True)
    shadow(s); return s.render(outline='050507', rim='a890e8', hi=1.4)

def c3():  # Niski łotrzyk ze sztyletem i krótkim łukiem
    s = Spr()
    s.ell(12, 23, 6, 5, D0, 'body'); s.rect(8, 26, 10, 29, D1, 'legL'); s.rect(13, 26, 15, 29, D1, 'legR')
    s.line([(6, 22), (14, 27)], '2e2a24', 'strap', True)
    s.line([(4, 20), (3, 24), (4, 28)], '3a2a20', 'bow'); s.line([(4, 20), (4, 28)], 'b89a6a', 'str')
    s.line([(18, 22), (21, 17)], 'd8d8e0', 'dagger', True); s.put(18, 23, '5a4a3a', 'hilt', True); s.put(17, 22, '5a4a3a', 'hilt', True)
    s.ell(12, 14, 6, 5.5, D2, 'hood'); s.line([(16, 10), (19, 8), (21, 9)], D2, 'tail', False)
    s.rect(7, 15, 17, 16, D1, 'scarf', True)
    s.ell(12, 14, 3.5, 2.5, '06060a', 'void', True); eyes(s, 13, 'ffb04a', '8a5a1a', (10, 14))
    shadow(s); return s.render(outline='050507', rim='e8b070', hi=1.4)

def c4():  # Mag-łucznik w szerokim kapeluszu, łuk z runą
    s = Spr()
    s.ell(12, 22, 8, 7, D0, 'robe'); s.rect(4, 22, 20, 29, D0, 'robe')
    for x in (7, 12, 17): s.line([(x, 22), (x, 29)], D1, 'fold')
    s.ell(12, 11, 5, 5, D2, 'head'); s.ell(12, 9, 10, 2.2, D2, 'brim'); s.line([(12, 7), (13, 2), (16, 0)], D2, 'cone', False); s.ell(12, 5, 3, 3, D2, 'cone')
    s.rect(9, 11, 15, 13, '06060a', 'void', True); eyes(s, 12, 'b8ff9a', '4a8a3a', (10, 14))
    s.line([(20, 13), (22, 18), (22, 25), (20, 30)], '22302a', 'bow'); s.line([(20, 13), (20, 30)], '8ad87a', 'str')
    s.put(22, 21, 'b8ff9a', 'rune', True); s.put(21, 21, '6ad85a', 'rune', True)
    s.ell(12, 19, 1.3, 1.3, '6ad85a', 'amulet')
    for p in ((5, 15), (3, 19)): s.put(*p, '6ad85a', 'spark', True)
    shadow(s); return s.render(outline='050507', rim='90d8a0', hi=1.4)

def c5():  # Mroczny rycerz z ciężkim łukiem
    s = Spr()
    s.rect(7, 24, 10, 29, D1, 'legL'); s.rect(13, 24, 16, 29, D1, 'legR')
    s.rect(5, 14, 18, 24, D0, 'chest'); s.ell(4, 15, 3, 2.5, D2, 'pauL'); s.ell(19, 15, 3, 2.5, D2, 'pauR')
    s.line([(4, 13), (3, 11)], D2, 'spikeL', False); s.line([(19, 13), (20, 11)], D2, 'spikeR', False)
    s.rect(2, 17, 4, 23, D0, 'armL'); s.rect(19, 17, 21, 23, D0, 'armR')
    s.line([(11, 15), (11, 23)], D1, 'seam', True); s.rect(6, 23, 17, 23, '2a1818', 'belt', True)
    s.ell(12, 8, 6, 6.5, D2, 'helm'); s.rect(6, 8, 17, 13, D2, 'helm')
    s.rect(7, 9, 16, 10, '06060a', 'visor', True); eyes(s, 9, 'ff5a4a', '8a2a2a', (9, 14))
    s.line([(9, 2), (12, -1), (15, 2)], D2, 'crest', False)
    s.line([(22, 8), (23, 15), (23, 24), (22, 30)], '30202a', 'bow'); s.line([(22, 8), (22, 30)], 'c87a7a', 'str')
    s.ell(11, 19, 1.3, 1.3, 'c83a3a', 'gem')
    shadow(s); return s.render(outline='050507', rim='9aa0c8', hi=1.4)

CH = [("c1_lowczyni", "C1: Łowczyni w kapturze", c1), ("c2_wysoki_lowca", "C2: Wysoki łowca z włócznią", c2),
      ("c3_lotrzyk", "C3: Łotrzyk ze sztyletem", c3), ("c4_mag_lucznik", "C4: Mag-łucznik", c4),
      ("c5_mroczny_rycerz", "C5: Mroczny rycerz", c5)]
SC = 6; DARK = (20, 19, 24); ARENA = (47, 45, 41)
cw, chh = W * SC + 90, H * SC + 50
sheet = Image.new('RGB', (cw * 5, chh), (12, 12, 16)); d = ImageDraw.Draw(sheet)
for i, (key, name, fn) in enumerate(CH):
    im = fn(); im.save(f'{key}.png')
    up = im.resize((W * SC, H * SC), Image.NEAREST)
    big = Image.new('RGB', up.size, DARK); big.paste(up, (0, 0), up); big.save(f'{key}_x6.png')
    x = i * cw + 10; sheet.paste(big, (x, 10))
    for j, col in enumerate((DARK, ARENA, (90, 88, 96))):
        sm = Image.new('RGB', (W * 2 + 4, H * 2 + 4), col); s2 = im.resize((W * 2, H * 2), Image.NEAREST); sm.paste(s2, (2, 2), s2)
        sheet.paste(sm, (x + up.width + 4, 10 + j * (H * 2 + 6)))
    d.text((x, H * SC + 18), name, fill=(200, 210, 230), font=FONT)
sheet.save('compare_dark.png')
