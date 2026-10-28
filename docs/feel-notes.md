# Feel notes — 3 iteracje (arena treningowa, bez bossa)
Testy: `godot --headless --path . -s playtest.gd` (symulowane wejście, krok 1/60 s). Surowe wyniki: docs/iter1..3.txt. Zrzuty: `xvfb-run godot --rendering-driver opengl3 --path . -s shot.gd`.

Research (recenzje/poradniki): w Titan Souls naciśnięcie przycisku uniku daje przewrót, a przytrzymanie daje bieg. Przewrót jest szybszy od biegu, ma odnowienie i odbija od przeszkód. Napinanie łuku zatrzymuje postać i **przybliża kamerę**, a strzał/przywołanie ją **oddala**. Kamera trzyma w kadrze ważne obiekty, areny są większe od ekranu. Nie ma celownika.

## Iteracja 1 — kamera + arena 640×480, filary, tarcze
Znalezione: kamera 20 px za graczem przy chodzie (zbyt ociężała). Strzała odlatywała na 335 px i wychodziła z kadru. Przywołanie trwało 2,35 s (nużące).
## Iteracja 2
Poprawki: CAM_DAMP 6→8, wyprzedzenie w kierunku ruchu (pvel·0,18 s), ARROW_DRAG 0,6→0,3/s, ZOOM_ARROW 0,85→0,75, przywołanie przyspiesza 60→420 px/s.
Wynik: kamera 4 px przed graczem, strzała ≤209 px i zawsze w kadrze, przywołanie 0,8 s.
## Iteracja 3
Znalezione: zatrzymanie 1 px — zbyt „cyfrowe”. Ślad przewrotu słabo widoczny. Szybkie ponowne wciśnięcie uniku przepadało. Reset nie czyścił stanu Shift (wykryte przez test odbicia).
Poprawki: FRICTION 1200→950 (hamowanie 1,5 px / 67 ms), pył co klatkę i duszki przewrotu, bufor uniku 0,12 s, poprawiony reset. Wszystkie metryki OK.
