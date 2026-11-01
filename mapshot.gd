extends SceneTree
# Mapa 1: przejście trasy ogród → jaskinia (test grywalności) + zrzuty.
const DT := 1.0 / 60.0
var m
func snap(name):
	m.queue_redraw(); m.hud.queue_redraw()
	for i in 3: await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://" + name)
func go(target: Vector2, max_steps := 1500) -> bool:
	for i in max_steps:
		var d: Vector2 = target - m.ppos
		if d.length() < 6: return true
		m.sim = {"move": d.normalized(), "aim": m.ppos + d}; m.step(DT)
	return false
func _init():
	m = load("res://main.tscn").instantiate(); root.add_child(m); await process_frame
	m.set_process(false); m.map_mode = true; m.reset()
	m.sim = {"move": Vector2.ZERO}; m.step(DT)
	for i in 30: m.step(DT)
	await snap("shot-map-garden.png")
	var route := [Vector2(160, 400), Vector2(420, 400), Vector2(470, 350), Vector2(640, 350), Vector2(700, 470), Vector2(1100, 480), Vector2(1500, 470), Vector2(1784, 440), Vector2(1784, 380), Vector2(1784, 250)]
	var ok := true
	for i in route.size():
		var r := go(route[i])
		print("PT waypoint_%d %s reached=%s at %s" % [i, route[i], r, m.ppos.round()])
		ok = ok and r
		if i == 5: await snap("shot-map-lake.png")
		if i == 7: await snap("shot-map-cave-entry.png")
	for i in 120: m.sim = {"move": Vector2.ZERO}; m.step(DT)
	await snap("shot-map-cave.png")
	print("PT route_ok = ", ok)
	# woda blokuje gracza
	m.ppos = Vector2(1000, 560); m.pvel = Vector2.ZERO
	go(Vector2(1000, 100), 300)
	print("PT water_blocks = ", m.ppos.y > 300, " y=", m.ppos.y)
	# strzała przelatuje nad wodą
	m.ppos = Vector2(1000, 450); m.pvel = Vector2.ZERO; m.has_arrow = true
	for i in 60: m.sim = {"aim": m.ppos + Vector2(0, -100), "shoot": true}; m.step(DT)
	m.sim = {"shoot": false}
	for i in 40: m.step(DT)
	await snap("shot-map-arrow-water.png")
	print("PT arrow_over_water = ", m.apos.y < 380, " y=", m.apos.y)
	quit()
