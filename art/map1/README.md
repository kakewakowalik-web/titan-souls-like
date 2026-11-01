# Mapa 1 — Ogród → Ścieżka nad jeziorem → Jaskinia (v2)

Generator: `make_map1.py` (Python + PIL, deterministyczny). Stara wersja: `v1/`.

Pliki:
- `map1_ground.png` – podłoże 1920×640 (120×40 kafli po 16 px), rysowane pod graczem.
- `map1_canopy.png` – korony drzew, rysowane NAD graczem (chowa się pod drzewem).
- `map1.json` – `solid` (kolizja gracza), `water` (woda: blokuje gracza, nie strzałę), `spawn`, `zones`, `cave_rect`, `targets`.
- `tileset.png`, `tiles.txt` – 13 typów kafli i flaga kolizji.
- `overview_map1*.png` – podgląd całej mapy (z opisami / zmniejszony).

## Inspiracja Titan Souls
- Cichy, rozległy świat jako „korytarz” między walkami: długie spacery, mało obiektów, wyraźne punkty orientacyjne (fontanna, jezioro, ciemny otwór skały).
- Stonowana paleta (szałwiowa zieleń, przygaszony błękit, piaskowa ścieżka, szary kamień), bez jaskrawych kolorów – kontrast zostaje dla gracza, strzały i celów.
- Progresja nastroju: jasny ogród → otwarte jezioro → coraz ciemniej przy klifie → prawie czarna jaskinia.

## Zasady grywalności (zastosowane)
1. **Szerokość przejść ≥ 3–4 kafle** (48–64 px) – szersze niż przewrót (~47 px), więc unik nie kończy się „bonkiem” na krawędzi ścieżki.
2. **Czytelne sylwetki**: wszystko, co blokuje, ma cień pod spodem, jaśniejszą górną krawędź i wyższy kontrast niż podłoże; podłoże po którym się chodzi jest płaskie i ciche.
3. **Kolizja = wygląd**: blokuje tylko to, co wygląda na twarde (żywopłot, pień, kamień, klif, fontanna, woda). Kwiaty i trawa są przechodnie. Pnie drzew są solidne, korony rysują się nad graczem.
4. **Woda blokuje gracza, ale nie strzałę** – można strzelać przez jezioro (test `arrow_over_water`).
5. **Bramy ~7 kafli, wejście do jaskini 5 kafli** – przejścia między strefami są szerokie i widoczne z daleka.
6. **Ścieżka prowadzi wzrok**: piaskowy pas wije się wzdłuż brzegu jeziora i kończy pod otworem jaskini.
7. **Kamera ograniczona do mapy** (ARENA = 1920×640), więc nigdy nie widać pustki poza światem.
8. **Ciemność rośnie przy klifie**, a w jaskini prawie czerń + światło wokół gracza (PointLight2D). Kula maga też świeci.
9. **Spawn w ogrodzie** (128, 344) – bezpieczny, jasny start z widokiem na aleję prowadzącą do bramy.
10. **Cele treningowe opcjonalne** (3 tarcze: ogród, ścieżka, jaskinia) – przełącznik T / pad X na ekranie wyboru postaci.

## Weryfikacja
`mapshot.gd` przechodzi trasę ogród → brama → ścieżka → jaskinia (10 punktów, wszystkie osiągnięte),
sprawdza że woda blokuje gracza i że strzała przelatuje nad wodą, i robi zrzuty `shot-map-*.png`.
