extends Node2D
# Strzała Strażnika — Titan Souls-like MVP. 1 HP, jedna strzała, jeden boss.
const W := 320.0
const H := 240.0
const ARENA := Rect2(16, 24, 288, 200)
const WALK := 62.0      # chód
const RUN := 96.0       # bieg (trzymaj Shift po przewrocie)
const ACCEL := 900.0    # px/s^2 — ~0.07 s do pełnej prędkości
const FRICTION := 1200.0 # hamowanie ~0.05 s, bez ślizgania
const ROLL_SPEED := 200.0
const ROLL_TIME := 0.22  # ~44 px
const ROLL_CD := 0.45
const ROLL_IFRAMES := Vector2(0.04, 0.14) # krótkie okno nietykalności w środku przewrotu
const BONK_TIME := 0.25  # odbicie od ściany = chwila bezbronności
var pvel := Vector2.ZERO
var roll_t := 0.0
var roll_cd := 0.0
var roll_dir := Vector2.DOWN
var bonk := 0.0
var shift_was := false
var last_dir := Vector2.DOWN
const ASPEED := 260.0

enum S { TITLE, PLAY, DEAD, WIN }
var state := S.TITLE
var t := 0.0
var hitstop := 0.0
var shake := 0.0

var ppos := Vector2(160, 200)
var aim := Vector2.UP
var charge := 0.0
var charging := false
var recalling := false
var has_arrow := true
var apos := Vector2.ZERO
var avel := Vector2.ZERO
var aflying := false
var dust := []

# Boss: Golem Strażnik
var bpos := Vector2(160, 80)
const BR := 22.0
var bstate := "idle" # idle, tele_slam, slam, stunned, tele_charge, charge
var btimer := 1.5
var bdir := Vector2.ZERO
var wave_r := -1.0
var eye_open := false
var nexta := 0

func _ready() -> void:
	reset()

func reset() -> void:
	ppos = Vector2(160, 200); pvel = Vector2.ZERO; roll_t = 0.0; roll_cd = 0.0; bonk = 0.0; has_arrow = true; aflying = false; charging = false; recalling = false
	bpos = Vector2(160, 80); bstate = "idle"; btimer = 1.5; wave_r = -1.0; eye_open = false; dust.clear()

func _mouse() -> Vector2:
	return get_global_mouse_position()

func _process(dt: float) -> void:
	t += dt
	shake = max(0.0, shake - dt * 8.0)
	if hitstop > 0.0:
		hitstop -= dt; queue_redraw(); return
	match state:
		S.TITLE, S.DEAD, S.WIN:
			if Input.is_key_pressed(KEY_ENTER) or Input.is_key_pressed(KEY_SPACE) and state == S.TITLE:
				reset(); state = S.PLAY
		S.PLAY:
			_player(dt); _arrow(dt); _boss(dt)
	for d in dust:
		d.life -= dt
	dust = dust.filter(func(d): return d.life > 0)
	queue_redraw()

func _player(dt: float) -> void:
	var m := _mouse() - ppos
	if m.length() > 1.0: aim = m.normalized()
	var shoot_held := Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) or Input.is_key_pressed(KEY_SPACE)
	var recall_held := Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT) or Input.is_key_pressed(KEY_R)
	var shift := Input.is_key_pressed(KEY_SHIFT) or Input.is_mouse_button_pressed(MOUSE_BUTTON_MIDDLE)
	var v := Vector2(
		float(Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT)) - float(Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT)),
		float(Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN)) - float(Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP))).normalized()
	if v != Vector2.ZERO: last_dir = v
	roll_cd = max(0.0, roll_cd - dt)
	# przewrót / odbicie mają pierwszeństwo — nie da się z nich strzelić
	if bonk > 0.0:
		bonk -= dt; pvel = pvel.move_toward(Vector2.ZERO, FRICTION * dt); _move(dt); shift_was = shift; return
	if roll_t > 0.0:
		roll_t -= dt
		pvel = roll_dir * ROLL_SPEED
		if randf() < 0.5: dust.append({"p": ppos + Vector2(0, 4), "life": 0.35})
		_move(dt)
		if roll_t <= 0.0: pvel = roll_dir * RUN
		shift_was = shift; return
	if shift and not shift_was and roll_cd <= 0.0 and not charging and not recalling:
		roll_dir = v if v != Vector2.ZERO else last_dir
		roll_t = ROLL_TIME; roll_cd = ROLL_TIME + ROLL_CD; charge = 0.0
		for i in 4: dust.append({"p": ppos + Vector2(randf_range(-3, 3), 4), "life": 0.4})
		shift_was = shift; return
	shift_was = shift
	charging = has_arrow and shoot_held
	if charging:
		charge = min(1.0, charge + dt * 1.5)
	elif has_arrow and charge > 0.0:
		apos = ppos + aim * 8; avel = aim * ASPEED * (0.4 + 0.6 * charge)
		has_arrow = false; aflying = true; charge = 0.0; shake = 0.3
	else:
		charge = 0.0
	recalling = (not has_arrow) and (not aflying) and (recall_held or shoot_held)
	if charging or recalling:
		pvel = pvel.move_toward(Vector2.ZERO, FRICTION * 2 * dt); _move(dt); return  # stoisz = bezbronny
	var target := v * (RUN if shift else WALK)
	if v != Vector2.ZERO:
		if pvel.length() < 10 and randf() < 0.6: dust.append({"p": ppos + Vector2(0, 4), "life": 0.3})
		# szybki zwrot: przy zmianie kierunku > 90° hamuj mocniej
		var a := ACCEL * (2.0 if pvel.dot(v) < 0 else 1.0)
		pvel = pvel.move_toward(target, a * dt)
	else:
		pvel = pvel.move_toward(Vector2.ZERO, FRICTION * dt)
	_move(dt)

func _move(dt: float) -> void:
	ppos += pvel * dt
	var c := ppos.clamp(ARENA.position + Vector2(4, 4), ARENA.end - Vector2(4, 4))
	if c != ppos and roll_t > 0.0:
		roll_t = 0.0; bonk = BONK_TIME; pvel = -roll_dir * 60; shake = 0.3
	ppos = c

func _invuln() -> bool:
	var e := ROLL_TIME - roll_t
	return roll_t > 0.0 and e >= ROLL_IFRAMES.x and e <= ROLL_IFRAMES.y

func _arrow(dt: float) -> void:
	if has_arrow: return
	if recalling:
		var d := ppos - apos
		avel = d.normalized() * 200.0
		apos += avel * dt
		_check_eye()
		if d.length() < 6: has_arrow = true
		return
	if aflying:
		apos += avel * dt
		avel *= pow(0.6, dt)
		if not ARENA.grow(-1).has_point(apos):
			apos = apos.clamp(ARENA.position, ARENA.end); aflying = false
		elif _check_eye(): pass
		elif apos.distance_to(bpos) < BR:
			# odbicie od kamiennego ciała
			avel = (apos - bpos).normalized() * avel.length() * 0.3
			apos = bpos + (apos - bpos).normalized() * (BR + 1)
			shake = 0.2; hitstop = 0.03
		if avel.length() < 25: aflying = false
	elif ppos.distance_to(apos) < 8:
		has_arrow = true

func _eye_pos() -> Vector2:
	return bpos + Vector2(0, -4)

func _check_eye() -> bool:
	if eye_open and abs(apos.x - bpos.x) < 8 and apos.distance_to(bpos) < BR + 2:
		hitstop = 0.07; shake = 1.0; state = S.WIN; return true
	return false

func _boss(dt: float) -> void:
	btimer -= dt
	eye_open = bstate == "stunned"
	match bstate:
		"idle":
			bpos = bpos.move_toward(ppos, 15 * dt)
			if btimer <= 0:
				nexta = (nexta + 1) % 2
				bstate = "tele_slam" if nexta == 0 else "tele_charge"; btimer = 0.8
				bdir = (ppos - bpos).normalized()
		"tele_slam":
			if btimer <= 0: bstate = "slam"; btimer = 0.6; wave_r = BR; shake = 1.0; hitstop = 0.05
		"slam":
			wave_r += 160 * dt
			var d := ppos.distance_to(bpos)
			if abs(d - wave_r) < 5: _die()
			if btimer <= 0: wave_r = -1; bstate = "stunned"; btimer = 1.8
		"stunned":
			if btimer <= 0: bstate = "idle"; btimer = 1.2
		"tele_charge":
			bdir = bdir.lerp((ppos - bpos).normalized(), dt * 2).normalized()
			if btimer <= 0: bstate = "charge"; btimer = 1.2
		"charge":
			bpos += bdir * 180 * dt
			if not ARENA.grow(-BR).has_point(bpos):
				bpos = bpos.clamp(ARENA.position + Vector2(BR, BR), ARENA.end - Vector2(BR, BR))
				shake = 1.0; hitstop = 0.05; bstate = "stunned"; btimer = 1.2
	if state == S.PLAY and ppos.distance_to(bpos) < BR + 3 and bstate != "stunned": _die()

func _die() -> void:
	if state != S.PLAY or _invuln(): return
	state = S.DEAD; hitstop = 0.07; shake = 1.0

func _draw() -> void:
	var o := Vector2(randf_range(-1, 1), randf_range(-1, 1)) * shake * 3
	o = o.round()
	draw_rect(Rect2(0, 0, W, H), Color("1b1a20"))
	draw_rect(Rect2(ARENA.position + o, ARENA.size), Color("3a3833"))
	for x in range(int(ARENA.position.x), int(ARENA.end.x), 16):
		for y in range(int(ARENA.position.y), int(ARENA.end.y), 16):
			if (x + y) / 16 % 2 == 0: draw_rect(Rect2(Vector2(x, y) + o, Vector2(16, 16)), Color("413e38"))
	draw_rect(Rect2(ARENA.position + o, ARENA.size), Color("6b6455"), false, 2)
	var f := ThemeDB.fallback_font
	if state == S.TITLE:
		draw_string(f, Vector2(0, 60), "STRZAŁA STRAŻNIKA", HORIZONTAL_ALIGNMENT_CENTER, W, 20, Color("e8d9a0"))
		draw_string(f, Vector2(0, 80), "JEDNA STRZAŁA · JEDNO ŻYCIE", HORIZONTAL_ALIGNMENT_CENTER, W, 10, Color("a89f86"))
		var lines := ["WASD / strzałki – ruch", "Mysz – celowanie", "LPM / Spacja (trzymaj) – napnij i strzel", "PPM / R (trzymaj) – przywołaj strzałę", "Shift / ŚPM – unik (przewrót), trzymaj = bieg", "Strzelanie i przywołanie = stoisz w miejscu!", "Trafić Golema w oko, gdy się otworzy", "", "ENTER – start"]
		for i in lines.size():
			draw_string(f, Vector2(0, 110 + i * 13), lines[i], HORIZONTAL_ALIGNMENT_CENTER, W, 9, Color("cfc6ad"))
		return
	for d in dust: draw_rect(Rect2(d.p + o - Vector2(1, 1), Vector2(2, 2)), Color(0.7, 0.65, 0.55, d.life * 3))
	# boss
	var bc := Color("6e6a60")
	if bstate == "tele_slam" or bstate == "tele_charge":
		bc = Color("b04a3a") if int(t * 12) % 2 == 0 else Color("6e6a60")
	var bp := bpos + o
	if bstate == "tele_slam": bp.y -= 4
	draw_circle(bp + Vector2(0, 6), BR, Color(0, 0, 0, 0.35))
	draw_rect(Rect2(bp - Vector2(BR, BR), Vector2(BR * 2, BR * 2)), bc)
	draw_rect(Rect2(bp - Vector2(BR, BR), Vector2(BR * 2, BR * 2)), Color("2c2a26"), false, 2)
	draw_rect(Rect2(bp + Vector2(-BR - 8, -6), Vector2(8, 16)), bc.darkened(0.2))
	draw_rect(Rect2(bp + Vector2(BR, -6), Vector2(8, 16)), bc.darkened(0.2))
	var ep := _eye_pos() + o
	if eye_open:
		draw_circle(ep, 6, Color("ffd65a")); draw_circle(ep, 3, Color("fff6c0"))
	else:
		draw_rect(Rect2(ep - Vector2(6, 1), Vector2(12, 2)), Color("2c2a26"))
	if bstate == "tele_charge":
		draw_line(bp, bp + bdir * 60, Color(0.9, 0.3, 0.2, 0.6), 1)
	if wave_r > 0: draw_arc(bpos + o, wave_r, 0, TAU, 48, Color("d9c27a"), 2)
	# arrow
	if not has_arrow:
		var dir := avel.normalized() if avel.length() > 1 else Vector2.RIGHT
		draw_line(apos + o - dir * 6, apos + o + dir * 3, Color("e8e0c8"), 1)
	# player
	if state != S.DEAD:
		var pc := Color("8fb6d8") if not (charging or recalling) else Color("d8d08f")
		if roll_t > 0.0:
			draw_rect(Rect2(ppos + o - Vector2(4, 1), Vector2(8, 5)), Color("cfe6ff") if _invuln() else pc)
		else:
			if bonk > 0.0: pc = Color("a07060")
			draw_rect(Rect2(ppos + o - Vector2(3, 4), Vector2(6, 8)), pc)
			draw_rect(Rect2(ppos + o - Vector2(2, 6), Vector2(4, 3)), Color("e8c9a0"))
		if roll_cd > 0.0 and roll_t <= 0.0:
			draw_rect(Rect2(ppos + o + Vector2(-4, 7), Vector2(8.0 * roll_cd / (ROLL_TIME + ROLL_CD), 1)), Color("7d7563"))
		if has_arrow: draw_line(ppos + o, ppos + o + aim * (8 + charge * 6), Color("e8e0c8"), 1)
		if recalling: draw_line(ppos + o, apos + o, Color(1, 0.9, 0.5, 0.25), 1)
	draw_string(f, Vector2(4, 16), "GOLEM STRAŻNIK", HORIZONTAL_ALIGNMENT_LEFT, -1, 9, Color("a89f86"))
	draw_string(f, Vector2(0, 236), "Shift: unik · 1 STRZAŁA · 1 ŻYCIE   " + ("strzała: jest" if has_arrow else "strzała: R/PPM"), HORIZONTAL_ALIGNMENT_RIGHT, W - 4, 8, Color("7d7563"))
	if state == S.DEAD:
		draw_string(f, Vector2(0, 120), "ZGINĄŁEŚ — ENTER, by spróbować ponownie", HORIZONTAL_ALIGNMENT_CENTER, W, 10, Color("d06050"))
	if state == S.WIN:
		draw_string(f, Vector2(0, 110), "GOLEM STRAŻNIK POKONANY", HORIZONTAL_ALIGNMENT_CENTER, W, 14, Color("ffd65a"))
		draw_string(f, Vector2(0, 130), "ENTER – jeszcze raz", HORIZONTAL_ALIGNMENT_CENTER, W, 9, Color("cfc6ad"))

# Do testów / zrzutów: wymuś stan
func debug_set(s: int, boss_state := "idle") -> void:
	reset(); state = s; bstate = boss_state; btimer = 99
	if boss_state == "roll":
		bstate = "tele_charge"; roll_t = 0.12; roll_dir = Vector2.RIGHT; ppos = Vector2(120, 180)
		for i in 8: dust.append({"p": ppos - Vector2(i * 4, -4), "life": 0.3})
