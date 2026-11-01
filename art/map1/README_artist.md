# Titan Souls overworld – map kit (v1)
Top-down, 16×16 tiles. Map 240×80 tiles = 3840×1280 px (2× the 1920×640 Map 1 on both axes).
Layout L→R: garden (hedge ring, fountain, 7-tile gate east) → open meadow + lake/river with bridge (empty arena centre, 4-tile sand path) → darkening cliffs + black cave mouth (x≈220,y≈40). Ruins pillars north (side path).

Files
- tileset_16.png (+ _x4 preview), tileset.json – tile IDs, pixel coords, collision type. fountain_i_j = 8×8 multi-tile block.
- ground_layer.png – painted full map (draw under player). Rocks, pillars, tree trunks are baked in.
- canopy_layer.png – RGBA tree crowns, draw ABOVE player.
- collision.json – 240×80 grid, row-major `data`: 0 walkable, 1 solid, 2 water (blocks player, not arrows). spawn [20,46]. collision.png = debug overlay (red solid, blue water).
- anim/grass_tuft_4f.png (4×16px, transparent overlay to sprinkle on grass), anim/water_6f.png (6×16px, tileable water loop). _x6 = zoomed previews.
- preview.png (half size), preview_full.png, preview_garden_crop.png, preview_cave_crop_2x.png.
- build.py – regenerates everything (Pillow + numpy, seeded).
Note: ground is painted per-pixel with organic edges (not tile-stamped); tileset is the matching kit for extensions/Godot TileSet. Edge tiles are sampled, not a full 47-blob autotile set.

## v2 tiles (build_tiles_v2.py) – current
- 109 clean hand-shaped 16×16 tiles. Corner (wang) autotiles: `<kind>_<TL><TR><BL><BR>` for path, paving, water (with sand shore + light rim), cliff (rim highlight + dark lip), hedge (top highlight). 15 configs each.
- Base: grass, grass_alt, flowers, grass_mid, grass_dark, grass_dark_alt (3-step darkening toward cave). Props: bridge, rock, pillar, tree_trunk, fountain_i_j (3×3), cave_i_j (5×3).
- ground_layer.png is now ASSEMBLED from these tiles; map.json = per-layer tile IDs (-1 empty), layer order base,path,paving,water,hedge,cliff,deco.
- collision.json rebuilt from tiles (bridge walkable, cave_trigger_tiles). canopy + anim unchanged.
- v1 kept as tileset_v1.json / preview_v1.png; build.py still provides masks.
