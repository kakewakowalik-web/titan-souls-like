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
	await snap("shot-title.png")
	await snap("shot-pad-hint.png")
	m.sim = {"move": Vector2.ZERO}; m.step(DT)
	# ruch: bieg po skosie z celowaniem w bok
	for i in 50:
		m.sim = {"move": Vector2(1, -1), "aim": m.ppos + Vector2(60, 20), "dodge": false}; m.step(DT)
	await snap("shot-move.png")
	# przewrót w lewo
	m.sim = {"move": Vector2.LEFT, "dodge": true}; m.step(DT)
	for i in 6:
		m.sim = {"move": Vector2.LEFT, "dodge": false}; m.step(DT)
	await snap("shot-roll.png")
	# kamera: napinanie, strzał, kadr ze strzałą
	for i in 30: m.sim = {"move": Vector2.ZERO}; m.step(DT)
	for i in 50: m.sim = {"aim": m.ppos + Vector2(0, -100), "shoot": true}; m.step(DT)
	await snap("shot-draw.png")
	m.sim = {"shoot": false}
	for i in 40: m.step(DT)
	await snap("shot-cam-follow.png")
	# przywołanie w ruchu
	m.sim = {"recall": true, "move": Vector2(-1, 0)}
	for i in 14: m.step(DT)
	await snap("shot-recall-move.png")
	quit()
