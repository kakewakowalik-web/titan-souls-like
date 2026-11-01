# Strzała Strażnika — arena treningowa (Godot 4.7)
Uruchom: `godot --path .`. Boss jest odłożony (legacy/boss_mvp.gd).

## Sterowanie
| akcja | klawiatura + mysz | pad (Xbox / PlayStation) |
|---|---|---|
| ruch | WASD / strzałki | lewa gałka (analogowo, martwa strefa 0,22) |
| celowanie | mysz | prawa gałka (martwa strefa 0,35; puszczona = ostatni kierunek) |
| napnij (trzymaj) / strzał (puść) | LPM / Spacja | RT / A (×) |
| przywołanie (trzymaj) | PPM / R (też LPM/Spacja, gdy strzała leży) | LT / X (□) (też RT/A) |
| unik (wciśnij) / bieg (trzymaj) | Shift / ŚPM | B (○) / LB / RB / L3 |
| start | Enter | Start / A |

Zasady: **napinanie łuku = stoisz w miejscu**. **Przywołując strzałę możesz chodzić, biegać i strzelać w bok**. Unik jest zablokowany tylko przy napinaniu; unik w trakcie przywołania je przerywa (trzymaj dalej przycisk, by wznowić po przewrocie). Ruch myszą przełącza celowanie z powrotem na mysz. Propozycje postaci: docs/sprite-styles.md.

## Ruch (finalne wartości)
chód 62 px/s · bieg 96 px/s · przyspieszenie 900 px/s² (~67 ms do pełnej) · hamowanie 950 px/s² (~67 ms, 1,5 px) · zawrotka ×2 przyspieszenia (~100 ms) · przewrót 200 px/s × 0,22 s ≈ 47 px · odnowienie 0,45 s (≈3 przewroty / 2 s) · nietykalność 0,04–0,14 s przewrotu · bufor uniku 0,12 s · odbicie od ściany/filaru 0,25 s bezbronności · napinanie zatrzymuje w ~33 ms · brak uniku podczas napinania · pełny ruch podczas przywołania.
## Kamera
wygładzanie wykładnicze 8/s · martwa strefa 6 px · wyprzedzenie: 14 px w stronę celu + ruch·0,18 s · napinanie: przybliżenie do 1,25× i przesunięcie do 30 px w stronę celu · strzała poza kołczanem: kadr między graczem a strzałą, oddalenie do 0,75× · powrót do 1,0× po złapaniu · wstrząsy przy strzale/wbiciu/trafieniu/odbiciu · ograniczenie do areny.
## Strzała
260 px/s × (0,4–1,0 zależnie od napięcia), opór 0,3/s, wbija się w ściany/filary; przywołanie przyspiesza 60→420 px/s i trafia tarcze po drodze.

Testy: `godot --headless --path . -s playtest.gd`. Notatki: docs/feel-notes.md.
