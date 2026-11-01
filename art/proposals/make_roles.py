# Role: rycerz, cień, łotrzyk, barbarzyńca, mag. python3 make_roles.py
src = open('make.py').read(); exec(src[:src.index('STYLES =')])
dk = open('make_dark.py').read(); exec(dk[dk.index('D0, D1'):dk.index('def c2')])

def r1():  # Rycerz w lśniącej zbroi
    s = Spr()
    s.rect(7, 24, 10, 29, 'c8d0dc', 'legL'); s.rect(13, 24, 16, 29, 'c8d0dc', 'legR')
    s.rect(5, 15, 18, 24, 'd8e0ea', 'chest'); s.ell(4, 16, 3, 2.5, 'e0e8f0', 'pauL'); s.ell(19, 16, 3, 2.5, 'e0e8f0', 'pauR')
    s.rect(2, 18, 4, 23, 'c8d0dc', 'armL'); s.rect(19, 18, 21, 23, 'c8d0dc', 'armR')
    s.rect(6, 23, 17, 23, 'e0b040', 'belt', True)
    s.line([(22, 9), (23, 16), (23, 24), (22, 30)], 'e0b040', 'bow'); s.line([(22, 9), (22, 30)], 'ffffff', 'str')
    s.ell(12, 9, 6, 6.5, 'd8e0ea', 'helm'); s.rect(6, 9, 17, 14, 'd8e0ea', 'helm')
    s.rect(7, 10, 16, 11, '1a2030', 'visor', True); s.rect(11, 12, 12, 14, 'a8b4c4', 'nose', True)
    s.rect(9, 0, 14, 3, '3a6ae0', 'plume'); s.line([(14, 1), (17, 4)], '3a6ae0', 'plume', False)
    s.rect(8, 17, 15, 21, '3a6ae0', 'tabard'); s.line([(11, 17), (11, 21)], 'ffe070', 'x', True); s.line([(9, 19), (14, 19)], 'ffe070', 'x', True)
    for p in ((7, 6), (5, 15), (3, 18), (8, 24), (7, 26), (14, 25), (18, 15)): s.put(*p, 'ffffff', 'glint', True)  # błyski
    for p in ((8, 7), (6, 16)): s.put(*p, 'f0f8ff', 'glint', True)
    shadow(s); return s.render(outline='141a26', hi=1.35)

def r3():  # Mały łotrzyk
    s = Spr()
    s.rect(9, 26, 10, 29, '4a3a5a', 'legL'); s.rect(13, 26, 14, 29, '4a3a5a', 'legR'); s.rect(8, 28, 10, 29, '2a1e1a', 'b'); s.rect(13, 28, 15, 29, '2a1e1a', 'b2')
    s.ell(12, 23, 5, 4.5, '7a3a8a', 'vest'); s.line([(8, 21), (15, 26)], '3a2418', 'strap', True)
    s.rect(7, 25, 16, 25, '3a2418', 'belt', True); s.put(15, 25, 'e0c060', 'pouch', True)
    s.ell(6, 23, 1.3, 1.3, 'e8b890', 'hL'); s.ell(18, 23, 1.3, 1.3, 'e8b890', 'hR')
    s.line([(19, 23), (21, 19)], 'e8e8f0', 'dagger', True); s.put(19, 24, '6a4a2a', 'h', True)
    s.line([(4, 18), (3, 22), (4, 27)], '8a5a2a', 'bow'); s.line([(4, 18), (4, 27)], 'e0d8c0', 'str')
    s.ell(12, 15, 5.5, 5, '5a2a6a', 'hood'); s.ell(12, 16, 3.5, 3, 'e8b890', 'face')
    s.rect(8, 17, 16, 18, 'c03a4a', 'mask'); s.line([(16, 13), (19, 12), (20, 14)], '5a2a6a', 'tail', False)
    s.put(10, 15, '1a1420', 'e', True); s.put(14, 15, '1a1420', 'e', True)
    shadow(s); return s.render(outline='1a1020')

def r4():  # Barbarzyńca — duży, wypełnia kadr
    s = Spr()
    s.rect(6, 24, 10, 30, '6a4a2a', 'legL'); s.rect(13, 24, 17, 30, '6a4a2a', 'legR'); s.rect(5, 29, 10, 30, '8a8a8a', 'fL'); s.rect(13, 29, 18, 30, '8a8a8a', 'fR')
    s.ell(12, 18, 10, 7, 'd8986a', 'torso')
    s.rect(4, 22, 19, 25, '7a5a3a', 'kilt'); s.rect(4, 22, 19, 22, '3a2a1a', 'belt', True); s.ell(12, 22, 1.5, 1, 'c8c8c8', 'skull', True)
    s.ell(3, 14, 3, 3, 'c8b898', 'furL'); s.ell(21, 14, 3, 3, 'c8b898', 'furR')
    s.rect(0, 15, 2, 22, 'd8986a', 'armL'); s.rect(21, 15, 23, 22, 'd8986a', 'armR')
    s.line([(9, 15), (12, 18), (15, 15)], 'b0705a', 'pec', True); s.line([(6, 13), (18, 21)], '5a3a22', 'strap', True)
    s.line([(1, 4), (0, 10), (0, 22), (1, 28)], '5a3a22', 'bow'); s.line([(1, 4), (1, 28)], 'e0d8c0', 'str')
    s.ell(12, 8, 5, 5, 'd8986a', 'face'); s.ell(12, 5, 6, 3.5, 'c84a1a', 'hair'); s.line([(6, 6), (5, 13)], 'c84a1a', 'mane', False); s.line([(18, 6), (19, 13)], 'c84a1a', 'mane', False)
    s.ell(12, 12, 3.5, 2.2, 'c84a1a', 'beard')
    s.line([(7, 3), (5, 0)], 'e8e0d0', 'horn', True); s.line([(17, 3), (19, 0)], 'e8e0d0', 'horn', True)
    s.put(10, 8, '1a1010', 'e', True); s.put(14, 8, '1a1010', 'e', True); s.line([(9, 7), (11, 7)], '8a3a1a', 'brow', True)
    shadow(s); return s.render(outline='1e140e')

def r5():  # Mag z kosturem
    s = Spr()
    s.ell(12, 22, 7, 7, '4a3ab0', 'robe'); s.rect(5, 22, 19, 29, '4a3ab0', 'robe')
    for x in (8, 12, 16): s.line([(x, 23), (x, 29)], '3a2a90', 'fold')
    s.line([(12, 16), (12, 29)], 'e0c050', 'trim', True); for_ = [s.put(x, 25, 'e0c050', 'st', True) for x in (7, 17)]
    s.ell(5, 21, 1.5, 1.5, 'f0d0b0', 'hL'); s.ell(19, 21, 1.5, 1.5, 'f0d0b0', 'hR')
    s.line([(20, 8), (20, 30)], '7a4a22', 'staff'); s.ell(20, 6, 2.2, 2.2, '7af0ff', 'orb', True); s.put(19, 5, 'ffffff', 'gl', True)
    for p in ((17, 3), (23, 4), (22, 9), (17, 8)): s.put(*p, 'b0f8ff', 'spark', True)
    s.line([(4, 14), (3, 18), (4, 22)], '6a4a2a', 'bow'); s.line([(4, 14), (4, 22)], 'c0d0ff', 'str')
    s.ell(12, 12, 4.5, 4.5, 'f0d0b0', 'face'); s.ell(12, 15, 4, 3, 'e8e8f0', 'beard'); s.line([(12, 17), (12, 19)], 'e8e8f0', 'beard', True)
    s.ell(12, 9, 9, 2, '3a2a90', 'brim'); s.ell(12, 6, 3.5, 3, '4a3ab0', 'cone'); s.line([(13, 4), (15, 1), (17, 0)], '4a3ab0', 'tip', False)
    s.put(11, 6, 'ffe070', 'star', True); s.put(10, 11, '2a2a6a', 'e', True); s.put(14, 11, '2a2a6a', 'e', True)
    shadow(s); return s.render(outline='120e2a')

CH = [("r1_rycerz_lsniacy", "1: Rycerz w lśniącej zbroi", r1), ("r2_cien_w_kapturze", "2: Cień w kapturze (P5)", c1),
      ("r3_maly_lotrzyk", "3: Mały łotrzyk", r3), ("r4_barbarzynca", "4: Barbarzyńca", r4), ("r5_mag", "5: Mag z kosturem", r5)]
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
sheet.save('compare_roles.png')
