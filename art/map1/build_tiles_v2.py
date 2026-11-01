# v2: clean hand-shaped 16x16 wang-corner tiles; ground is assembled FROM tiles.
exec(open('build.py').read()); fountain_mask=fountain
import numpy as np, json, math
from PIL import Image, ImageDraw
T=16
def hx(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
P=dict(g1=hx('#8fa27c'),g2=hx('#85996f'),g3=hx('#9bad86'),gd1=hx('#6f7d68'),gd2=hx('#66735f'),
 pa1=hx('#cbb48c'),pa2=hx('#bba57f'),pa3=hx('#d8c49e'),pv1=hx('#b9b3a3'),pv2=hx('#a39d8e'),
 sh=hx('#c2b48f'),w1=hx('#6f93a3'),w2=hx('#5c8193'),wh=hx('#a9c6cf'),
 c1=hx('#85868a'),c2=hx('#77787c'),c3=hx('#9c9d9f'),cf=hx('#55575c'),co=hx('#3e4045'),
 h1=hx('#5e7656'),h2=hx('#4d6347'),h3=hx('#718a67'),ho=hx('#3c4d38'),out=hx('#4b5a45'))
R=np.random.default_rng(3)
def speck(a,cols,n):
    for _ in range(n):
        x,y=R.integers(1,15,2); a[y,x]=cols[R.integers(len(cols))]
def base(c1,c2,c3,seed,n=6):
    a=np.zeros((T,T,4),np.uint8); a[...,:3]=c1; a[...,3]=255
    r=np.random.default_rng(seed)
    for _ in range(n):  # tiny 2px clumps, low density
        x,y=r.integers(1,14,2); a[y,x,:3]=c2; a[y,x+1,:3]=c2; a[y-1,x,:3]=c3
    return a
u=(np.arange(T)+.5)/T; U,V=np.meshgrid(u,u)
def field(cfg):  # cfg=(TL,TR,BL,BR) -> smooth value 0..1
    tl,tr,bl,br=cfg
    v=tl*(1-U)*(1-V)+tr*U*(1-V)+bl*(1-U)*V+br*U*V
    return v
def wang(kind,cfg):
    v=field(cfg); a=np.zeros((T,T,4),np.uint8)
    def put(m,c):
        a[m,:3]=c; a[m,3]=255
    if kind=='path' or kind=='paving':
        k1,k2,k3=('pa1','pa2','pa3') if kind=='path' else ('pv1','pv2','pv1')
        m=v>.5; put(m,P[k1]); put((v>.42)&~m,P['out'] if kind=='path' else P['pv2'])
        tex=(((np.indices((T,T)).sum(0))%7==0)&(v>.7)); put(tex,P[k2])
        if kind=='paving': put(m&((np.indices((T,T))[0]%8==0)|(np.indices((T,T))[1]%8==0)),P['pv2'])
    elif kind=='water':
        put(v>.3,P['sh']); put((v>.3)&(v<.36),P['out'])
        m=v>.5; put(m,P['w1']); put(v>.85,P['w2']); put((v>.5)&(v<.56),P['wh'])
    elif kind=='cliff':
        put(v>.36,P['cf']); put(v>.5,P['c1']); put(v>.75,P['c2'])
        put((v>.5)&(v<.56),P['c3']); put((v>.36)&(v<.41),P['co'])
        I=np.indices((T,T)); put((v>.6)&((I[0]*3+I[1]*5)%13==0),P['c3'])
    elif kind=='hedge':
        put(v>.42,P['ho']); put(v>.5,P['h1']); put((v>.5)&(V<.4),P['h3'])
        I=np.indices((T,T)); put((v>.62)&((I[0]+I[1]*2)%6==0),P['h2'])
    return a
KINDS=['path','paving','water','cliff','hedge']
CFGS=[(a,b,c,d) for a in (0,1) for b in (0,1) for c in (0,1) for d in (0,1)][1:]
tiles={}; order=[]
def add(n,arr): tiles[n]=arr; order.append(n)
add('grass',base(P['g1'],P['g2'],P['g3'],1)); add('grass_alt',base(P['g1'],P['g2'],P['g3'],2,4))
fl=base(P['g1'],P['g2'],P['g3'],3,2)
for (x,y),c in [((4,5),'#e8e2cf'),((11,10),'#d9b8c4'),((7,12),'#e4d48a')]: fl[y,x,:3]=hx(c); fl[y+1,x,:3]=P['g2']
add('flowers',fl); cf=base(hx('#1a1a1f'),hx('#24252b'),hx('#2c2d33'),9,5); add('cave_floor',cf); add('grass_mid',base(hx('#7f9071'),P['gd1'],P['g1'],6)); add('grass_dark',base(P['gd1'],P['gd2'],P['g2'],4)); add('grass_dark_alt',base(P['gd1'],P['gd2'],P['g2'],5,3))
# bridge (horizontal planks, rails top/bottom), over water
b=np.zeros((T,T,4),np.uint8); b[...,3]=255; b[...,:3]=hx('#9a7a58')
for x in range(0,T,4): b[:,x,:3]=hx('#6e543d')
b[0:2,:,:3]=hx('#5b4636'); b[14:16,:,:3]=hx('#5b4636'); b[2,:,:3]=hx('#b89670')
add('bridge',b)
def sprite(w,h,fn):
    im=Image.new('RGBA',(w,h),(0,0,0,0)); fn(ImageDraw.Draw(im)); return im
def rock(d): d.ellipse([1,4,14,14],fill=(70,72,74,90)); d.ellipse([1,2,14,13],fill=P['c1'],outline=P['co']); d.ellipse([4,4,9,7],fill=P['c3'])
def pillar(d): d.rectangle([4,1,11,14],fill=hx('#a7a39a'),outline=P['co']); d.rectangle([3,0,12,3],fill=hx('#bdb8ad'),outline=P['co']); d.line([6,4,6,13],fill=hx('#c9c4b9'))
def trunk(d): d.ellipse([2,10,15,15],fill=(55,65,52,150)); d.rectangle([6,2,10,13],fill=hx('#5b4636'),outline=hx('#3c2f26'))
for n,f in [('rock',rock),('pillar',pillar),('tree_trunk',trunk)]: add(n,np.asarray(sprite(16,16,f)))
def fountain(d):
    d.ellipse([1,1,46,46],fill=hx('#9b958a'),outline=P['co'],width=2); d.ellipse([5,5,42,42],fill=P['w1'])
    d.arc([7,7,40,40],200,330,fill=P['wh']); d.ellipse([18,18,29,29],fill=hx('#b8b2a2'),outline=P['co']); d.ellipse([21,20,26,25],fill=hx('#d8e6ea'))
F=np.asarray(sprite(48,48,fountain))
for j in range(3):
    for i in range(3): add(f'fountain_{i}_{j}',F[j*16:j*16+16,i*16:i*16+16])
def cave(d):  # 5x3 tiles, south-facing arch, opening = exactly tiles i=1..3 (px 16..63)
    d.rectangle([0,0,79,47],fill=P['c2'])
    d.rectangle([0,0,79,3],fill=P['c3']); d.line([0,4,79,4],fill=P['co'])
    d.ellipse([10,6,69,60],fill=P['co']); d.rectangle([10,33,69,47],fill=P['co'])
    d.ellipse([16,10,63,58],fill=hx('#0b0b0e')); d.rectangle([16,34,63,47],fill=hx('#0b0b0e'))
    d.arc([10,6,69,60],185,355,fill=P['c3'],width=2)
    for x in (0,79): d.line([x,0,x,47],fill=P['co'])
Cv=np.asarray(sprite(80,48,cave))
for j in range(3):
    for i in range(5): add(f'cave_{i}_{j}',Cv[j*16:j*16+16,i*16:i*16+16])
for k in KINDS:
    for c in CFGS: add(f'{k}_{"".join(map(str,c))}',wang(k,c))
# --- corner grids ---
def corners(m):
    ys=np.clip(np.arange(TH+1)*T,0,H-1); xs=np.clip(np.arange(TW+1)*T,0,W-1)
    return m[np.ix_(ys,xs)].astype(int)
Cc=corners(cliff); Cw=corners(water&~bridge)|corners(bridge); Cp=corners(path&~bridge)&(1-Cw)&(1-Cc)
Cpv=corners(pav&~fountain_mask)&(1-Cc); Ch=corners(hedge)&(1-Cc)
# cave block area forced to cliff around, carve corners
cx0,cy0=214,34          # arch tiles x214-218, y34-36; opening x215-217
IX0,IX1,IY0,IY1=212,220,25,33   # interior tiles x212-219, y25-33 (8x9)
Cc[20:cy0+3,204:226]=1          # solid rock mass around cave
Cc[IY0+1:IY1+1,IX0+1:IX1]=0     # carve interior
Cc[IY1:cy0+3,cx0+1:cx0+4]=0     # tunnel through arch
Cc[cy0+3:cy0+10,203:223]=0      # approach clearing y37-43 in front of arch
layers={k:np.zeros((TH,TW),object) for k in ['base','path','paving','water','cliff','hedge','deco']}
grid={'path':Cp,'paving':Cpv,'water':Cw,'cliff':Cc,'hedge':Ch}
for y in range(TH):
    for x in range(TW):
        dk=x>196+2*math.sin(y/5); mid=x>178+2*math.sin(y/4); alt=(x*7+y*13)%11==0; flw=(x*31+y*17)%53==0 and x<60
        layers['base'][y,x]=('grass_dark_alt' if alt else 'grass_dark') if dk else ('grass_mid' if mid else ('flowers' if flw else ('grass_alt' if alt else 'grass')))
        for k,g in grid.items():
            c=(g[y,x],g[y,x+1],g[y+1,x],g[y+1,x+1])
            if any(c): layers[k][y,x]=f'{k}_{"".join(map(str,c))}'
            else: layers[k][y,x]=None
        layers['deco'][y,x]=None
        if IX0<=x<=IX1 and IY0<=y<=IY1+1: layers['base'][y,x]='cave_floor'
bm=bridge.reshape(TH,T,TW,T).mean((1,3))>.05
ys_,xs_=np.where(bm); yc=int(round(ys_.mean())); x0b,x1b=xs_.min(),xs_.max()
for y in range(yc-1,yc+2):
    for x in range(x0b,x1b+1): layers['deco'][y,x]='bridge'; Cw[y,x]=Cw[y,x]  # walkable set below
bridge_tiles=[(y,x) for y in range(yc-1,yc+2) for x in range(x0b,x1b+1)]
for j in range(3):
    for i in range(3): layers['deco'][39+j,23+i]=f'fountain_{i}_{j}'
for j in range(3):
    for i in range(5): layers['deco'][cy0+j,cx0+i]=f'cave_{i}_{j}'
for x,y in rocks: layers['deco'][int(y),int(x)]='rock'
for x,y in pillars: layers['deco'][int(y),int(x)]='pillar'
for x,y in trees: layers['deco'][int(y),int(x)]='tree_trunk'
LORDER=['base','path','paving','water','hedge','cliff','deco']
g=Image.new('RGBA',(W,H))
TI={n:Image.fromarray(tiles[n]) for n in order}
for L in LORDER:
    for y in range(TH):
        for x in range(TW):
            n=layers[L][y,x]
            if n: g.alpha_composite(TI[n],(x*T,y*T))
g.convert('RGB').save('ground_layer.png')
# collision from tiles
col=np.zeros((TH,TW),np.uint8)
def cnt(Cg,y,x): return Cg[y,x]+Cg[y,x+1]+Cg[y+1,x]+Cg[y+1,x+1]
for y in range(TH):
    for x in range(TW):
        if cnt(Cw,y,x)>=2: col[y,x]=2
        if cnt(Cc,y,x)>=2 or cnt(Ch,y,x)>=2: col[y,x]=1
        d=layers['deco'][y,x]
        if d and d!='bridge' and not d.startswith('cave'): col[y,x]=1
        if d=='bridge': col[y,x]=0
        if (y,x) in bridge_tiles and x in (x0b-1,): pass
for j in range(3):
    for i in range(5): col[cy0+j,cx0+i]=0 if 1<=i<=3 else 1   # arch: 3-wide walkable opening
cave_trig=[[cx0+i,cy0] for i in range(1,4)]   # threshold = top (inner) row of arch
json.dump({'tile':16,'width':TW,'height':TH,'legend':{'0':'walkable','1':'solid','2':'water (blocks player, not arrows)'},'cave_trigger_tiles':cave_trig,'spawn':[20,46],'data':col.flatten().tolist()},open('collision.json','w'))
pal=np.array([[0,0,0,0],[220,60,60,170],[60,120,230,170]],np.uint8)
Image.fromarray(pal[col]).resize((W,H),Image.NEAREST).save('collision.png')
# tileset sheet
cols=16; rows=math.ceil(len(order)/cols)
ts=Image.new('RGBA',(cols*T,rows*T)); meta={}
solidk=('cliff','hedge','rock','pillar','tree','fountain')
for i,n in enumerate(order):
    ts.alpha_composite(TI[n],((i%cols)*T,(i//cols)*T))
    k=n.split('_')[0]; ctype='solid' if k in solidk else 'water' if k=='water' else 'walkable'
    if k=='cave': ctype='solid (inner 3 bottom tiles walkable = cave trigger)'
    meta[n]={'id':i,'x':(i%cols)*T,'y':(i//cols)*T,'collision':ctype}
ts.save('tileset_16.png'); ts.resize((ts.width*4,ts.height*4),Image.NEAREST).save('tileset_16_x4.png')
json.dump({'tile_size':16,'columns':cols,'version':2,
 'wang':'<kind>_<TL><TR><BL><BR>: corner-based (wang) autotiles, 1 = corner belongs to that terrain. Overlays with alpha; draw over base grass.',
 'layer_order':LORDER,'tiles':meta},open('tileset.json','w'),indent=1)
idmap={n:i for i,n in enumerate(order)}
json.dump({'tile':16,'width':TW,'height':TH,'layer_order':LORDER,'layers':{L:[(idmap[n] if n else -1) for n in layers[L].flatten()] for L in LORDER}},open('map.json','w'))
pv=g.copy(); pv.alpha_composite(can); pv.save('preview_full.png')
pv.resize((W//2,H//2),Image.LANCZOS).save('preview.png')
pv.crop((0,24*T,72*T,58*T)).save('preview_garden_crop.png')
pv.crop((196*T,20*T,TW*T,48*T)).resize(((TW-196)*T*3,28*T*3),Image.NEAREST).save('preview_cave_crop_2x.png')
pv.crop((80*T,30*T,120*T,60*T)).resize((40*T*3,30*T*3),Image.NEAREST).save('preview_bridge_crop_3x.png')
print(len(order),'tiles')
