extends SceneTree
func _init():
	var m = load("res://main.tscn").instantiate(); root.add_child(m); await process_frame
	m.debug_set(1,"stunned"); m.has_arrow=false; m.aflying=true; m.apos=Vector2(160,140); m.avel=Vector2(0,-250)
	for i in 30: await process_frame
	print("WIN_TEST ", m.state == 3, " ", m.state, m.apos, m.bstate, m.aflying)
	m.debug_set(1,"idle"); m.ppos = m.bpos + Vector2(10,0)
	for i in 5: await process_frame
	print("DIE_TEST ", m.state == 2)
	m.debug_set(1,"idle"); m.bpos=Vector2(60,60); m.roll_t=m.ROLL_TIME-0.08; m.roll_dir=Vector2.RIGHT
	m._die(); print("IFRAME_TEST ", m.state == 1)
	m.roll_t=0.0; m._die(); print("NOIFRAME_TEST ", m.state == 2)
	m.debug_set(1,"idle"); m.bpos=Vector2(60,60); m.ppos=Vector2(295,150); m.roll_t=0.2; m.roll_dir=Vector2.RIGHT
	var b := false
	for i in 200:
		await process_frame
		if m.bonk > 0.0: b = true; break
	print("BONK_TEST ", b)
	quit()
