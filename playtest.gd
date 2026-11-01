extends SceneTree
# Zautomatyzowany "playtest": symulowane wejście, stały krok 1/60 s, metryki odczucia.
const DT := 1.0 / 60.0
var m
func run(frames: int, inp: Dictionary) -> void:
	m.sim = inp
	for i in frames: m.step(DT)
func _init():
	m = load("res://main.tscn").instantiate(); root.add_child(m); await process_frame
	m.set_process(false); m.sim = {"move": Vector2.ZERO}; m.step(DT)
	var R := {}
	# 1. przyspieszenie
	m.reset(); var f := 0
	while m.pvel.length() < m.WALK * 0.95 and f < 120:
		m.sim = {"move": Vector2.RIGHT, "aim": m.ppos + Vector2(0, -50)}; m.step(DT); f += 1
	R.accel_ms = f * DT * 1000
	for i in 60:
		m.sim = {"move": Vector2.RIGHT, "aim": m.ppos + Vector2(0, -50)}; m.step(DT)
	R.cam_lag_walk = snapped(m.cam_pos.x - m.ppos.x, 0.1)
	R.aim_kept_while_strafe = m.aim.y < -0.9
	# 2. zatrzymanie
	var x0 = m.ppos.x; f = 0
	m.sim = {"move": Vector2.ZERO, "aim": m.ppos + Vector2(0, -50)}
	while m.pvel.length() > 0.1 and f < 120: m.step(DT); f += 1
	R.stop_ms = f * DT * 1000; R.stop_px = snapped(m.ppos.x - x0, 0.1)
	# 3. zawrotka
	run(30, {"move": Vector2.RIGHT}); f = 0
	m.sim = {"move": Vector2.LEFT}
	while m.pvel.x > -m.WALK * 0.95 and f < 120: m.step(DT); f += 1
	R.reverse_ms = f * DT * 1000
	# 4. przewrót
	m.reset(); x0 = m.ppos.x
	run(1, {"move": Vector2.RIGHT, "dodge": true}); run(30, {"move": Vector2.RIGHT, "dodge": false})
	R.roll_px = snapped(m.ppos.x - x0 - 30 * DT * 0, 0.1)
	m.reset(); x0 = m.ppos.x
	run(1, {"move": Vector2.RIGHT, "dodge": true}); var rt := 0
	while m.roll_t > 0.0: m.step(DT); rt += 1
	R.roll_only_px = snapped(m.ppos.x - x0, 0.1); R.roll_frames = rt
	# spam: ile przewrotów w 2 s
	m.reset(); var rolls := 0
	for i in 120:
		var d := i % 2 == 0
		m.sim = {"move": Vector2.RIGHT if (i / 40) % 2 == 0 else Vector2.LEFT, "dodge": d}
		var was = m.roll_t; m.step(DT)
		if m.roll_t > 0.0 and was <= 0.0: rolls += 1
	R.rolls_in_2s = rolls
	# bufor: wciśnij unik 5 klatek przed końcem odnowienia
	m.reset(); run(1, {"move": Vector2.RIGHT, "dodge": true})
	run(int((m.ROLL_TIME + m.ROLL_CD) * 60) - 5, {"move": Vector2.RIGHT, "dodge": false})
	run(1, {"move": Vector2.RIGHT, "dodge": true}); run(8, {"move": Vector2.RIGHT, "dodge": true})
	R.buffered_roll = m.roll_t > 0.0
	# 5. odbicie od ściany
	m.reset(); m.ppos = Vector2(600, 400)
	run(1, {"move": Vector2.RIGHT, "dodge": true}); var b := false
	for i in 30:
		m.sim = {"move": Vector2.RIGHT}; m.step(DT)
		if m.bonk > 0.0: b = true
	R.wall_bonk = b
	# odbicie od filaru
	m.reset(); m.ppos = Vector2(120, 132)
	run(1, {"move": Vector2.RIGHT, "dodge": true}); b = false
	for i in 30:
		m.sim = {"move": Vector2.RIGHT}; m.step(DT)
		if m.bonk > 0.0: b = true
	R.pillar_bonk = b; R.pillar_not_inside = not m.pillars[0].has_point(m.ppos)
	# 6. napinanie: stop + kamera
	m.reset(); run(40, {"move": Vector2.RIGHT, "aim": m.ppos + Vector2(0, -80)})
	var cam0 = m.cam_pos
	f = 0; m.sim = {"move": Vector2.RIGHT, "aim": m.ppos + Vector2(0, -80), "shoot": true}
	while m.pvel.length() > 0.1 and f < 60: m.step(DT); f += 1
	R.draw_stop_ms = f * DT * 1000
	run(60, m.sim)
	R.draw_zoom = snapped(m.cam.zoom.x, 0.01); R.draw_cam_lead_y = snapped(m.cam_pos.y - m.ppos.y, 0.1)
	# roll zablokowany przy napinaniu
	run(1, {"aim": m.ppos + Vector2(0, -80), "shoot": true, "dodge": true}); R.no_roll_while_draw = m.roll_t <= 0.0
	# 7. strzał + kadr ze strzałą
	run(1, {"aim": m.ppos + Vector2(0, -80), "shoot": false})
	var maxspan := 0.0; var inview := true
	for i in 120:
		m.step(DT)
		var half = Vector2(160, 120) / m.cam.zoom.x
		var rel = (m.apos - m.cam.position).abs()
		if rel.x > half.x or rel.y > half.y: inview = false
		maxspan = max(maxspan, m.ppos.distance_to(m.apos))
	R.arrow_span = snapped(maxspan, 1); R.arrow_always_in_view = inview; R.arrow_zoom = snapped(m.cam.zoom.x, 0.01)
	# 8. przywołanie
	f = 0; m.sim = {"recall": true}
	while not m.has_arrow and f < 300: m.step(DT); f += 1
	R.recall_ms = f * DT * 1000; R.recall_ok = m.has_arrow
	run(90, {})
	R.zoom_back = snapped(m.cam.zoom.x, 0.01)
	# 9. drgania kamery przy stałym biegu po skosie
	m.reset(); run(20, {"move": Vector2(1, -1)}); var jit := 0; var prev = m.cam.position; var pd = Vector2.ZERO
	for i in 60:
		m.step(DT); var d = m.cam.position - prev
		if pd != Vector2.ZERO and (d - pd).length() > 1.5: jit += 1
		pd = d; prev = m.cam.position
	R.cam_jitter_frames = jit
	# 10. ruch podczas przywołania
	m.reset(); m.has_arrow = false; m.aflying = false; m.apos = Vector2(320, 100)
	var x1 = m.ppos.x
	run(30, {"move": Vector2.RIGHT, "recall": true})
	R.recall_move_px = snapped(m.ppos.x - x1, 0.1); R.recall_active_while_move = m.recalling
	run(1, {"move": Vector2.RIGHT, "recall": true, "dodge": true})
	R.roll_during_recall = m.roll_t > 0.0 and not m.recalling
	while m.roll_t > 0.0: m.step(DT)
	run(2, {"move": Vector2.RIGHT, "recall": true, "dodge": false}); R.recall_resumes = m.recalling
	f = 0
	while not m.has_arrow and f < 300:
		m.sim = {"move": Vector2.LEFT, "recall": true}; m.step(DT); f += 1
	R.recall_move_caught = m.has_arrow
	# 11. napinanie dalej blokuje ruch
	m.reset(); run(20, {"move": Vector2.RIGHT, "shoot": true}); var x2 = m.ppos.x
	run(20, {"move": Vector2.RIGHT, "shoot": true}); R.draw_still = abs(m.ppos.x - x2) < 0.5
	# 12. pad: celowanie gałką
	m.reset(); run(3, {"stick_aim": Vector2(1, 1)}); R.pad_aim_ok = m.aim.dot(Vector2(1, 1).normalized()) > 0.99
	R.stick_deadzone = m._stick(JOY_AXIS_LEFT_X, JOY_AXIS_LEFT_Y, m.STICK_DZ) == Vector2.ZERO
	for k in R: print("PT ", k, " = ", R[k])
	quit()
