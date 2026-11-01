# Mapa 1 — Ogród → ścieżka nad jeziorem → ciemna jaskinia (grafika, bez TileMapy)
Generator: `python3 make_map1.py`. Kafel ma 16×16 px, ten sam piksel co postacie.

## Pliki
- `tileset.png` — 22 kafle, siatka 8 kolumn × 16 px. Lista z indeksami i współrzędnymi: `tiles.txt`.
- `objects.png` — większe obiekty (współrzędne w `tiles.txt`): dąb, wiśnia, świerk (32×48), krzew (16×16), fontanna (48×40), wejście do jaskini (64×48).
- `overview_map1.png` — podgląd całej mapy 120×26 kafli (1920×416 px). `overview_map1_opis.png` to ten sam podgląd z podpisami stref, a `overview_map1_maly.png` jest pomniejszony.

## Kafle (indeks → znaczenie)
0–1 trawa (2 warianty) · 2–4 rabaty kwiatów (czerwone/żółte/niebieskie) · 5 ścieżka ziemna · 6 kamienna aleja · 7 woda · 8 głęboka woda · 9–12 brzeg (woda po stronie: pd / pn / zach / wsch) · 13 żywopłot (kolizja) · 14 kamień (kolizja) · 15 lilia wodna · 16 trzciny na brzegu · 17 skalista trawa · 18 krawędź klifu · 19 ściana klifu (kolizja) · 20 podłoga jaskini (bardzo ciemna) · 21 ściana jaskini (kolizja).

## Przebieg mapy
1. **Ogród** (kafle 0–38): żywopłoty, rabaty, kwitnące wiśnie, kamienna aleja z fontanną. Jasno i spokojnie.
2. **Ścieżka nad jeziorem** (38–90): duże jezioro z liliami i trzcinami. Ścieżka wije się wzdłuż południowego brzegu, przy niej dęby.
3. **Wejście do jaskini** (90–120): trawa przechodzi w skały, pojawiają się świerki. Pod klifem jest czarne wejście do jaskini, a ekran stopniowo ciemnieje (w grze: CanvasModulate / światło gracza).

W Godot: TileSet z `tileset.png` (16×16, filtr Nearest), kolizja na kaflach 13, 14, 19 i 21, a woda (7–8) jako przeszkoda dla gracza, ale nie dla strzały. Obiekty jako Sprite2D z Y-sort.
