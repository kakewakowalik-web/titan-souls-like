extends Node2D
# Strzała Strażnika — arena treningowa (bez bossa). Ruch + unik + łuk + kamera.
# Boss MVP odłożony w legacy/boss_mvp.gd.
const VIEW := Vector2(320, 240)
const ARENA := Rect2(0, 0, 640, 480)
const WALL := 16.0
const PR := 4.0 # promień gracza

# --- ruch (wartości po 3 iteracjach, patrz docs/feel-notes.md) ---
var WALK := 62.0
var RUN := 96.0
var ACCEL := 900.0
var FRICTION := 950.0
var TURN_BOOST := 2.0
var ROLL_SPEED := 200.0
var ROLL_TIME := 0.22
var ROLL_CD := 0.45
var ROLL_IFRAMES := Vector2(0.04, 0.14)
var BONK_TIME := 0.25
var DODGE_BUFFER := 0.12  # wciśnięcie uniku tuż przed końcem odnowienia się liczy
var dodge_buf := 0.0
var trail := []
var ASPEED := 260.0
var ARROW_DRAG := 0.3   # mnożnik prędkości na sekundę
var RECALL_MIN := 60.0
var RECALL_MAX := 420.0
var RECALL_ACC := 500.0
var recall_speed := 0.0
# --- kamera ---
var CAM_DAMP := 8.0        # wykładnicze wygładzanie (1/s)
var CAM_LOOK := 14.0       # look-ahead w stronę celu (px)
var CAM_LOOK_DRAW := 30.0  # przy napinaniu
var CAM_DEADZONE := 6.0
var CAM_MOVE_LEAD := 0.18  # s: wyprzedzenie w kierunku ruchu
var ZOOM_BASE := 1.0
var ZOOM_DRAW := 1.25      # przybliżenie przy napinaniu (jak w Titan Souls)
var ZOOM_ARROW := 0.75     # oddalenie gdy strzała w locie / przywoływanie
var ZOOM_DAMP := 4.0

# --- postacie (art/player/*.png) ---
const CHARS := [
	{"id": "rycerz", "name": "Rycerz", "desc": "Lśniąca zbroja · wolniejszy, pewny strzał", "tex": "res://art/player/r1_rycerz_lsniacy.png", "proj": "arrow",
		"walk": 56.0, "run": 88.0, "roll_speed": 185.0, "roll_time": 0.22, "charge": 1.5, "speed": 280.0, "drag": 0.3, "recall": 400.0},
	{"id": "cien", "name": "Cień", "desc": "Kaptur · długi, szybki przewrót", "tex": "res://art/player/r2_cien_w_kapturze.png", "proj": "arrow",
		"walk": 62.0, "run": 96.0, "roll_speed": 220.0, "roll_time": 0.25, "charge": 1.5, "speed": 260.0, "drag": 0.3, "recall": 420.0},
	{"id": "lotrzyk", "name": "Łotrzyk", "desc": "Mały i zwinny · szybkie napięcie, krótszy zasięg", "tex": "res://art/player/r3_maly_lotrzyk.png", "proj": "arrow",
		"walk": 70.0, "run": 106.0, "roll_speed": 210.0, "roll_time": 0.2, "charge": 2.4, "speed": 230.0, "drag": 0.22, "recall": 440.0},
	{"id": "barbarzynca", "name": "Barbarzyńca", "desc": "Rzut toporem · ciężki, krótki lot, szybki powrót", "tex": "res://art/player/r4_barbarzynca.png", "proj": "axe",
		"walk": 58.0, "run": 92.0, "roll_speed": 180.0, "roll_time": 0.22, "charge": 1.8, "speed": 230.0, "drag": 0.12, "recall": 520.0},
	{"id": "mag", "name": "Mag", "desc": "Kula zaklęcia · mało oporu, wolniejsze przywołanie", "tex": "res://art/player/r5_mag.png", "proj": "orb",
		"walk": 60.0, "run": 92.0, "roll_speed": 195.0, "roll_time": 0.22, "charge": 1.2, "speed": 200.0, "drag": 0.55, "recall": 340.0},
]
var char_i := 0
var phase := 0   # 0 = tytuł, 1 = wybór postaci, 2 = gra
var texs := []
var prev_keys := {}

func apply_char(i: int) -> void:
	char_i = i; var c: Dictionary = CHARS[i]
	WALK = c.walk; RUN = c.run; ROLL_SPEED = c.roll_speed; ROLL_TIME = c.roll_time
	ASPEED = c.speed; ARROW_DRAG = c.drag; RECALL_MAX = c.recall

func _pressed(name: String, down: bool) -> bool:
	var was: bool = prev_keys.get(name, false); prev_keys[name] = down
	return down and not was

var pillars := [Rect2(140, 120, 24, 24), Rect2(476, 120, 24, 24), Rect2(140, 336, 24, 24), Rect2(476, 336, 24, 24), Rect2(300, 220, 40, 40)]
var dummies := [] # {p, hit}

var sim := {}  # nadpisanie wejścia dla testów: {"move":Vector2,"aim":Vector2(world),"shoot":bool,"recall":bool,"dodge":bool}
var t := 0.0
var hitstop := 0.0
var shake := 0.0
var started := false

var ppos := Vector2(320, 400)
var pvel := Vector2.ZERO
var aim := Vector2.UP
var charge := 0.0
var charging := false
var recalling := false
var has_arrow := true
var apos := Vector2.ZERO
var avel := Vector2.ZERO
var aflying := false
var roll_t := 0.0
var roll_cd := 0.0
var roll_dir := Vector2.DOWN
var bonk := 0.0
var shift_was := false
var last_dir := Vector2.DOWN
var dust := []

var cam: Camera2D
var hud: Node2D
var cam_pos := Vector2.ZERO

func _ready() -> void:
	for c in CHARS: texs.append(load(c.tex))
	apply_char(0)
	cam = Camera2D.new(); add_child(cam); cam.make_current()
	var layer := CanvasLayer.new(); add_child(layer)
	hud = Node2D.new(); layer.add_child(hud); hud.draw.connect(_draw_hud)
	reset()

func reset() -> void:
	ppos = Vector2(320, 400); pvel = Vector2.ZERO; roll_t = 0.0; roll_cd = 0.0; bonk = 0.0
	has_arrow = true; aflying = false; charging = false; recalling = false; charge = 0.0
	dummies = [{"p": Vector2(320, 90), "hit": 0.0}, {"p": Vector2(90, 240), "hit": 0.0}, {"p": Vector2(550, 240), "hit": 0.0}]
	dodge_buf = 0.0; shift_was = false; trail.clear(); cam_pos = ppos; cam.position = cam_pos; cam.zoom = Vector2.ONE * ZOOM_BASE

# --- wejście (klawiatura + mysz + pad) ---
const STICK_DZ := 0.22     # martwa strefa lewej gałki (radialna, z przeskalowaniem)
const AIM_DZ := 0.35       # martwa strefa prawej gałki
const TRIG_ON := 0.45      # próg spustu
var pad_aim := false       # true = celujemy gałką, dopóki mysz się nie ruszy
var pad_used := false

func _input(e: InputEvent) -> void:
	if e is InputEventMouseMotion: pad_aim = false
	if e is InputEventJoypadButton or (e is InputEventJoypadMotion and abs(e.axis_value) > 0.5): pad_used = true
	

func _stick(ax: JoyAxis, ay: JoyAxis, dz: float) -> Vector2:
	var v := Vector2(Input.get_joy_axis(0, ax), Input.get_joy_axis(0, ay))
	var l := v.length()
	if l < dz: return Vector2.ZERO
	return v / l * min(1.0, (l - dz) / (1.0 - dz))
func _btn(b: JoyButton) -> bool:
	return Input.is_joy_button_pressed(0, b)
func _trig(ax: JoyAxis) -> bool:
	return Input.get_joy_axis(0, ax) > TRIG_ON

func in_move() -> Vector2:
	if sim.has("move"): return sim.move.normalized()
	var k := Vector2(
		float(Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT)) - float(Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT)),
		float(Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN)) - float(Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP))).normalized()
	if k != Vector2.ZERO: return k
	return _stick(JOY_AXIS_LEFT_X, JOY_AXIS_LEFT_Y, STICK_DZ)  # analog: długość = prędkość
func in_aim() -> Vector2:
	if sim.has("aim"): return sim.aim
	if sim.has("stick_aim"): pad_aim = true; return ppos + sim.stick_aim.normalized() * 40.0
	var r := _stick(JOY_AXIS_RIGHT_X, JOY_AXIS_RIGHT_Y, AIM_DZ)
	if r != Vector2.ZERO: pad_aim = true; return ppos + r.normalized() * 40.0
	if pad_aim: return ppos + aim * 40.0  # gałka puszczona: trzymaj ostatni kierunek
	return get_global_mouse_position()
func in_shoot() -> bool:
	return sim.get("shoot", Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) or Input.is_key_pressed(KEY_SPACE) or _trig(JOY_AXIS_TRIGGER_RIGHT) or _btn(JOY_BUTTON_A))
func in_recall() -> bool:
	return sim.get("recall", Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT) or Input.is_key_pressed(KEY_R) or _trig(JOY_AXIS_TRIGGER_LEFT) or _btn(JOY_BUTTON_X))
func in_dodge() -> bool:
	return sim.get("dodge", Input.is_key_pressed(KEY_SHIFT) or Input.is_mouse_button_pressed(MOUSE_BUTTON_MIDDLE) or _btn(JOY_BUTTON_B) or _btn(JOY_BUTTON_LEFT_SHOULDER) or _btn(JOY_BUTTON_RIGHT_SHOULDER) or _btn(JOY_BUTTON_LEFT_STICK))

func _process(dt: float) -> void:
	step(dt)

func step(dt: float) -> void:
	t += dt
	shake = max(0.0, shake - dt * 6.0)
	if not started:
		if sim.size() > 0: started = true; phase = 2
		var ok := _pressed("ok", Input.is_key_pressed(KEY_ENTER) or Input.is_key_pressed(KEY_SPACE) or _btn(JOY_BUTTON_A) or _btn(JOY_BUTTON_START))
		var lx := Input.get_joy_axis(0, JOY_AXIS_LEFT_X)
		var l := _pressed("l", Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT) or _btn(JOY_BUTTON_DPAD_LEFT) or lx < -0.6)
		var r := _pressed("r", Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT) or _btn(JOY_BUTTON_DPAD_RIGHT) or lx > 0.6)
		if phase == 0 and ok: phase = 1
		elif phase == 1:
			if l: apply_char((char_i + CHARS.size() - 1) % CHARS.size())
			if r: apply_char((char_i + 1) % CHARS.size())
			if ok: reset(); started = true; phase = 2; prev_keys["ok"] = true
		_camera(dt); queue_redraw(); hud.queue_redraw(); return
	if _pressed("esc", Input.is_key_pressed(KEY_ESCAPE) or _btn(JOY_BUTTON_BACK)) and sim.size() == 0:
		started = false; phase = 1; return
	if hitstop > 0.0:
		hitstop -= dt
	else:
		_player(dt); _arrow(dt)
	for d in dummies: d.hit = max(0.0, d.hit - dt)
	for d in dust: d.life -= dt
	dust = dust.filter(func(d): return d.life > 0)
	_camera(dt)
	queue_redraw(); hud.queue_redraw()

func _player(dt: float) -> void:
	var m := in_aim() - ppos
	if m.length() > 1.0: aim = m.normalized()
	var shoot_held := in_shoot()
	var recall_held := in_recall()
	var shift := in_dodge()
	var v := in_move()
	if v != Vector2.ZERO: last_dir = v
	roll_cd = max(0.0, roll_cd - dt)
	dodge_buf = max(0.0, dodge_buf - dt)
	if shift and not shift_was: dodge_buf = DODGE_BUFFER
	for g in trail: g.life -= dt
	trail = trail.filter(func(g): return g.life > 0)
	if bonk > 0.0:
		bonk -= dt; pvel = pvel.move_toward(Vector2.ZERO, FRICTION * dt); _move(dt); shift_was = shift; return
	if roll_t > 0.0:
		roll_t -= dt
		pvel = roll_dir * ROLL_SPEED
		_dust(ppos + Vector2(randf_range(-2, 2), 0), 0.35)
		if int(roll_t * 60) % 3 == 0: trail.append({"p": ppos.round(), "life": 0.15})
		_move(dt)
		_pickup()
		if roll_t <= 0.0: pvel = roll_dir * (RUN if shift and v != Vector2.ZERO else WALK)
		shift_was = shift; return
	if dodge_buf > 0.0 and roll_cd <= 0.0 and not charging:
		recalling = false
		dodge_buf = 0.0
		roll_dir = v if v != Vector2.ZERO else last_dir
		roll_t = ROLL_TIME; roll_cd = ROLL_TIME + ROLL_CD
		for i in 4: _dust(ppos + Vector2(randf_range(-3, 3), 0), 0.4)
		shift_was = shift; return
	shift_was = shift
	charging = has_arrow and shoot_held
	if charging:
		charge = min(1.0, charge + dt * float(CHARS[char_i].charge))
	elif has_arrow and charge > 0.0:
		apos = ppos + aim * 6; avel = aim * ASPEED * (0.4 + 0.6 * charge)
		has_arrow = false; aflying = true; charge = 0.0; shake = 0.25
	else:
		charge = 0.0
	var was_rec := recalling
	recalling = (not has_arrow) and (not aflying) and (recall_held or shoot_held)
	if recalling and not was_rec: recall_speed = 0.0
	if charging:
		pvel = pvel.move_toward(Vector2.ZERO, FRICTION * 2.0 * dt); _move(dt); return
	var target := v * (RUN if shift else WALK)
	if v != Vector2.ZERO:
		if pvel.length() < 10.0: _dust(ppos, 0.3)
		var a := ACCEL * (TURN_BOOST if pvel.dot(v) < 0.0 else 1.0)
		pvel = pvel.move_toward(target, a * dt)
	else:
		pvel = pvel.move_toward(Vector2.ZERO, FRICTION * dt)
	_move(dt)
	_pickup()

func _dust(p: Vector2, life: float) -> void:
	dust.append({"p": p + Vector2(0, 4), "life": life})

func _solid(p: Vector2, r: float) -> bool:
	if not ARENA.grow(-WALL - r).has_point(p): return true
	for q in pillars:
		if q.grow(r).has_point(p): return true
	return false

func _move(dt: float) -> void:
	var hit := false
	var nx := ppos + Vector2(pvel.x * dt, 0)
	if _solid(nx, PR): hit = true; pvel.x = 0.0 if roll_t <= 0.0 else pvel.x
	else: ppos = nx
	var ny := ppos + Vector2(0, pvel.y * dt)
	if _solid(ny, PR): hit = true; pvel.y = 0.0 if roll_t <= 0.0 else pvel.y
	else: ppos = ny
	if hit and roll_t > 0.0:
		roll_t = 0.0; bonk = BONK_TIME; pvel = -roll_dir * 60.0; shake = 0.3

func _pickup() -> void:
	if not has_arrow and not aflying and ppos.distance_to(apos) < 8.0: has_arrow = true

func _arrow(dt: float) -> void:
	if has_arrow: return
	if recalling:
		var d := ppos - apos
		recall_speed = min(RECALL_MAX, max(recall_speed, RECALL_MIN) + RECALL_ACC * dt)
		avel = d.normalized() * recall_speed
		apos += avel * dt
		_hit_dummies()
		if d.length() < 6.0: has_arrow = true; recalling = false
		return
	if aflying:
		var np := apos + avel * dt
		if _solid(np, 1.0):
			aflying = false; shake = 0.15  # wbija się w ścianę/filar
		else:
			apos = np
			avel *= pow(ARROW_DRAG, dt)
			_hit_dummies()
			if avel.length() < 25.0: aflying = false

func _hit_dummies() -> void:
	for d in dummies:
		if d.hit <= 0.0 and apos.distance_to(d.p) < 7.0:
			d.hit = 0.6; hitstop = 0.05; shake = 0.4

# --- kamera w stylu Titan Souls ---
func _camera(dt: float) -> void:
	var target := ppos
	var z := ZOOM_BASE
	if charging:
		target += aim * CAM_LOOK_DRAW * (0.5 + 0.5 * charge); z = lerp(ZOOM_BASE, ZOOM_DRAW, charge)
	elif not has_arrow:
		# trzymaj w kadrze gracza i strzałę
		var mid := (ppos + apos) * 0.5
		target = ppos.lerp(mid, 0.6)
		var span := ppos.distance_to(apos)
		z = clamp(lerp(ZOOM_BASE, ZOOM_ARROW, span / 160.0), ZOOM_ARROW, ZOOM_BASE)
	else:
		target += aim * CAM_LOOK + pvel * CAM_MOVE_LEAD
	var diff := target - cam_pos
	if diff.length() > CAM_DEADZONE or charging or not has_arrow:
		cam_pos += diff * (1.0 - exp(-CAM_DAMP * dt))
	var cz: float = cam.zoom.x + (z - cam.zoom.x) * (1.0 - exp(-ZOOM_DAMP * dt))
	cam.zoom = Vector2(cz, cz)
	var half := VIEW * 0.5 / cz
	var c := cam_pos
	c.x = clamp(c.x, ARENA.position.x + half.x, ARENA.end.x - half.x) if ARENA.size.x > half.x * 2 else ARENA.get_center().x
	c.y = clamp(c.y, ARENA.position.y + half.y, ARENA.end.y - half.y) if ARENA.size.y > half.y * 2 else ARENA.get_center().y
	var sh := Vector2(randf_range(-1, 1), randf_range(-1, 1)) * shake * 3.0
	cam.position = (c + sh).round()

func _draw() -> void:
	draw_rect(Rect2(-200, -200, 1040, 880), Color("141318"))
	draw_rect(ARENA, Color("2f2d29"))
	for x in range(0, int(ARENA.size.x), 16):
		for y in range(0, int(ARENA.size.y), 16):
			if (x / 16 + y / 16) % 2 == 0: draw_rect(Rect2(x, y, 16, 16), Color("363430"))
	draw_rect(Rect2(0, 0, ARENA.size.x, WALL), Color("4d483e")); draw_rect(Rect2(0, ARENA.size.y - WALL, ARENA.size.x, WALL), Color("4d483e"))
	draw_rect(Rect2(0, 0, WALL, ARENA.size.y), Color("4d483e")); draw_rect(Rect2(ARENA.size.x - WALL, 0, WALL, ARENA.size.y), Color("4d483e"))
	for q in pillars:
		draw_rect(Rect2(q.position + Vector2(0, 4), q.size), Color(0, 0, 0, 0.35))
		draw_rect(q, Color("6b6455")); draw_rect(Rect2(q.position, Vector2(q.size.x, 4)), Color("857d6a"))
	for d in dummies:
		var c := Color("d9c27a") if d.hit > 0.0 else Color("8a6a4a")
		draw_rect(Rect2(d.p - Vector2(1, -2), Vector2(2, 6)), Color("4a3a2a"))
		draw_circle(d.p, 6, c); draw_circle(d.p, 3, Color("2a2420")); draw_circle(d.p, 1.5, c)
	for d in dust: draw_rect(Rect2((d.p - Vector2(1, 1)).round(), Vector2(2, 2)), Color(0.7, 0.65, 0.55, d.life * 2.5))
	if not has_arrow:
		var dir := avel.normalized() if avel.length() > 1.0 else Vector2.RIGHT
		match CHARS[char_i].proj:
			"axe":
				var spin := t * 25.0 if (aflying or recalling) else 0.6
				var ax := Vector2.from_angle(spin)
				draw_line(apos - ax * 5, apos + ax * 5, Color("6a4a2a"), 2)
				draw_circle(apos + ax * 5, 3, Color("b8c0c8")); draw_circle(apos + ax * 5 + ax.orthogonal(), 1, Color("f0f4f8"))
			"orb":
				var pulse := 1.0 + 0.3 * sin(t * 12.0)
				draw_circle(apos, 5 * pulse, Color(0.3, 0.8, 1.0, 0.25)); draw_circle(apos, 3, Color("4ac8ff")); draw_circle(apos - Vector2(1, 1), 1, Color.WHITE)
				if aflying or recalling: dust.append({"p": apos + Vector2(randf_range(-2, 2), -4 + randf_range(-2, 2)), "life": 0.25})
			_:
				draw_line(apos - dir * 6, apos + dir * 3, Color("e8e0c8"), 1)
				draw_rect(Rect2(apos + dir * 2 - Vector2(1, 1), Vector2(2, 2)), Color("b07ad8"))
	for g in trail: draw_rect(Rect2(g.p - Vector2(4, 1), Vector2(8, 5)), Color(0.56, 0.71, 0.85, g.life * 3.0))
	var p := ppos.round()
	draw_rect(Rect2(p + Vector2(-3, 2), Vector2(6, 3)), Color(0, 0, 0, 0.35))
	var tex: Texture2D = texs[char_i]
	var mod := Color.WHITE
	if charging: mod = Color(1.15, 1.1, 0.9)
	if bonk > 0.0: mod = Color(1.0, 0.6, 0.55)
	var flip := aim.x < -0.2
	if roll_t > 0.0:
		var e := ROLL_TIME - roll_t
		if e >= ROLL_IFRAMES.x and e <= ROLL_IFRAMES.y: mod = Color(1.4, 1.5, 1.7)
		var ang := (1.0 - roll_t / ROLL_TIME) * TAU * (1.0 if roll_dir.x >= 0.0 else -1.0)
		draw_set_transform(p + Vector2(0, -8), ang, Vector2(0.8, 0.8))
		draw_texture(tex, Vector2(-12, -16), mod)
		draw_set_transform(Vector2.ZERO, 0, Vector2.ONE)
	else:
		var bob := 1.0 if pvel.length() > 20.0 and int(t * 10) % 2 == 0 else 0.0
		draw_set_transform(p + Vector2(0, -bob), 0, Vector2(-1 if flip else 1, 1))
		draw_texture(tex, Vector2(-12, -29), mod)
		draw_set_transform(Vector2.ZERO, 0, Vector2.ONE)
	if has_arrow and charging:
		var wc: Color = {"arrow": Color("e8e0c8"), "axe": Color("b8c0c8"), "orb": Color("4ac8ff")}[CHARS[char_i].proj]
		draw_line(p + Vector2(0, -10), p + Vector2(0, -10) + aim * (8 + charge * 8), wc, 1)
	elif has_arrow:
		draw_rect(Rect2(p + Vector2(0, -10) + aim * 10 - Vector2(1, 1), Vector2(2, 2)), Color(1, 1, 1, 0.5))
	if recalling: draw_line(p + Vector2(0, -10), apos, Color(1, 0.9, 0.5, 0.25), 1)
	if roll_cd > 0.0 and roll_t <= 0.0:
		draw_rect(Rect2(p + Vector2(-4, 3), Vector2(8.0 * roll_cd / (ROLL_TIME + ROLL_CD), 1)), Color("7d7563"))

func _draw_hud() -> void:
	var f := ThemeDB.fallback_font
	if not started and phase == 1:
		hud.draw_rect(Rect2(0, 0, VIEW.x, VIEW.y), Color(0.04, 0.04, 0.06, 0.92))
		hud.draw_string(f, Vector2(0, 30), "WYBIERZ POSTAĆ", HORIZONTAL_ALIGNMENT_CENTER, VIEW.x, 16, Color("e8d9a0"))
		for i in CHARS.size():
			var x := 32 + i * 64; var sel := i == char_i
			hud.draw_rect(Rect2(x - 26, 52, 52, 96), Color("2f2d29") if sel else Color("1b1a20"))
			if sel: hud.draw_rect(Rect2(x - 26, 52, 52, 96), Color("e8d9a0"), false, 1)
			hud.draw_set_transform(Vector2(x, 100), 0, Vector2(2, 2) if sel else Vector2(1.5, 1.5))
			hud.draw_texture(texs[i], Vector2(-12, -16), Color.WHITE if sel else Color(0.6, 0.6, 0.65))
			hud.draw_set_transform(Vector2.ZERO, 0, Vector2.ONE)
			hud.draw_string(f, Vector2(x - 30, 162), CHARS[i].name, HORIZONTAL_ALIGNMENT_CENTER, 60, 8, Color("e8d9a0") if sel else Color("7d7563"))
		var c: Dictionary = CHARS[char_i]
		var wname: String = {"arrow": "łuk i jedna strzała", "axe": "jeden topór do rzucania", "orb": "jedna kula zaklęcia"}[c.proj]
		hud.draw_string(f, Vector2(0, 186), c.desc, HORIZONTAL_ALIGNMENT_CENTER, VIEW.x, 9, Color("cfc6ad"))
		hud.draw_string(f, Vector2(0, 200), "Broń: " + wname + " (strzał + przywołanie)", HORIZONTAL_ALIGNMENT_CENTER, VIEW.x, 8, Color("a89f86"))
		hud.draw_string(f, Vector2(0, 224), "◄ ► / A D / krzyżak – wybór · ENTER / A – graj", HORIZONTAL_ALIGNMENT_CENTER, VIEW.x, 8, Color("e8d9a0"))
		return
	if not started:
		hud.draw_rect(Rect2(0, 0, VIEW.x, VIEW.y), Color(0, 0, 0, 0.7))
		hud.draw_string(f, Vector2(0, 50), "STRZAŁA STRAŻNIKA", HORIZONTAL_ALIGNMENT_CENTER, VIEW.x, 20, Color("e8d9a0"))
		hud.draw_string(f, Vector2(0, 68), "ARENA TRENINGOWA · JEDNA STRZAŁA", HORIZONTAL_ALIGNMENT_CENTER, VIEW.x, 9, Color("a89f86"))
		var rows := [["", "KLAWIATURA + MYSZ", "PAD"], ["ruch", "WASD / strzałki", "lewa gałka"], ["celowanie", "mysz", "prawa gałka"], ["napnij/strzał", "LPM / Spacja", "RT / A"], ["przywołanie", "PPM / R", "LT / X"], ["unik / bieg", "Shift / ŚPM", "B / LB / RB / L3"]]
		for i in rows.size():
			var c := Color("e8d9a0") if i == 0 else Color("cfc6ad")
			hud.draw_string(f, Vector2(14, 92 + i * 13), rows[i][0], HORIZONTAL_ALIGNMENT_LEFT, -1, 8, Color("a89f86"))
			hud.draw_string(f, Vector2(88, 92 + i * 13), rows[i][1], HORIZONTAL_ALIGNMENT_LEFT, -1, 8, c)
			hud.draw_string(f, Vector2(208, 92 + i * 13), rows[i][2], HORIZONTAL_ALIGNMENT_LEFT, -1, 8, c)
		hud.draw_string(f, Vector2(0, 184), "Napinanie łuku = stoisz. Przywołując strzałę możesz chodzić.", HORIZONTAL_ALIGNMENT_CENTER, VIEW.x, 8, Color("cfc6ad"))
		hud.draw_string(f, Vector2(0, 198), "Unik przerywa przywołanie (trzymaj dalej, by wznowić).", HORIZONTAL_ALIGNMENT_CENTER, VIEW.x, 8, Color("cfc6ad"))
		hud.draw_string(f, Vector2(0, 220), "ENTER / START / A – dalej (wybór postaci)", HORIZONTAL_ALIGNMENT_CENTER, VIEW.x, 9, Color("e8d9a0"))
		return
	hud.draw_string(f, Vector2(4, 12), "ARENA TRENINGOWA · " + String(CHARS[char_i].name).to_upper() + " · Esc: zmiana postaci", HORIZONTAL_ALIGNMENT_LEFT, -1, 8, Color("7d7563"))
	hud.draw_string(f, Vector2(0, 236), ("B/LB: unik" if pad_used else "Shift: unik") + " · 1 " + String({"arrow": "STRZAŁA", "axe": "TOPÓR", "orb": "KULA"}[CHARS[char_i].proj]) + " · " + ("strzała: jest" if has_arrow else ("LT/X: przywołaj" if pad_used else "R/PPM: przywołaj")), HORIZONTAL_ALIGNMENT_RIGHT, VIEW.x - 4, 8, Color("7d7563"))
