extends SceneTree
const DT := 1.0 / 60.0
var m
func snap(name):
	m.queue_redraw(); m.hud.queue_redraw()
	for i in 3: await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://" + name)
func _init():
	m = load("res://main.tscn").instantiate(); root.add_child(m); await process_frame
	m.set_process(false)
	m.phase = 1; m.apply_char(3); await snap("shot-select.png")
	var names := ["rycerz", "cien", "lotrzyk", "barbarzynca", "mag"]
	for i in 5:
		m.apply_char(i); m.reset(); m.started = true; m.phase = 2
		for k in 20: m.sim = {"move": Vector2(1, -1)}; m.step(DT)
		for k in 40: m.sim = {"aim": m.ppos + Vector2(80, -60), "shoot": true}; m.step(DT)
		m.sim = {"shoot": false}
		for k in 12: m.step(DT)
		var thrown = not m.has_arrow
		await snap("shot-char-%d-%s.png" % [i + 1, names[i]])
		var f := 0
		while not m.has_arrow and f < 600:
			m.sim = {"recall": true, "move": Vector2(0, 0)}; m.step(DT); f += 1
		print("CHAR ", names[i], " thrown=", thrown, " recalled=", m.has_arrow, " in ", f, " fr")
	quit()
