import numpy as np, json, math, random
from PIL import Image, ImageDraw, ImageFilter
rng=np.random.default_rng(7); random.seed(7)
T=16; TW,TH=240,80; W,H=TW*T,TH*T
def noise(w,h,scale,seed):
    r=np.random.default_rng(seed).random((max(2,h//scale+2),max(2,w//scale+2)))
    im=Image.fromarray((r*255).astype(np.uint8)).resize((w+scale*2,h+scale*2),Image.BICUBIC)
    return np.asarray(im,dtype=np.float32)[:h,:w]/255
def fbm(w,h,s,seed): return (noise(w,h,s,seed)*.6+noise(w,h,s//2 or 1,seed+1)*.3+noise(w,h,max(1,s//4),seed+2)*.1)
X,Y=np.meshgrid(np.arange(W),np.arange(H))
tx,ty=X/T,Y/T
n1=fbm(W,H,96,1); n2=fbm(W,H,32,2)
# palettes (muted)
def C(h):return np.array([int(h[i:i+2],16) for i in (1,3,5)],np.float32)
GR=C('#8fa27c');GR2=C('#7d9070');GRD=C('#6b7766');PATH=C('#c9b28a');PATHD=C('#a99a80')
WAT=C('#6f93a3');WATD=C('#557a8c');SHORE=C('#b9ad8c');ROCK=C('#8a8a88');ROCKD=C('#5d5f62')
CL=C('#77787a');CLD=C('#4a4c50');HED=C('#5e7656');PAV=C('#b8b2a2');CAVE=C('#0b0b0e')
# --- terrain masks (pixel) ---
dark=np.clip((tx-150)/70,0,1)  # mood progression toward cave
# cliffs top/bottom + right
top=4+3*n1[:, :]*1.0; 
cliff=(ty<3+4*noise(W,H,160,3))|(ty>TH-3-4*noise(W,H,160,4))|(tx>222+6*(noise(W,H,120,5)-.5)+ (np.abs(ty-40)<14)*0)
cliff|=(tx>205+8*noise(W,H,80,6))&((ty<26+4*n2)|(ty>54-4*n2))
cliff|=(tx<2.5+2*noise(W,H,100,9))
# cave pocket: corridor from x205 to 222, y 30..50 open floor; cave mouth
cave=((tx-224)**2/9+(ty-40)**2/7.5<1)&(tx>220)
cliff&=~cave
# lake + river
lake=((tx-128)/30)**2+((ty-58)/12)**2 < 1-0.35*(n1-.5)*2
rx=96+5*np.sin(ty/7)
river=(np.abs(tx-rx)<1.8+0.4*n2)&(ty<58)
water=(lake|river)&~cliff
# path: gate(44,40) -> cave(220,40), arcs above lake
def pathy(x):
    return 40+ -6*np.sin(np.clip((x-60)/140,0,1)*math.pi)*1.0 - 3*np.sin(x/23)
py=pathy(tx)
path=(np.abs(ty-py)<1.9+0.4*n2)&(tx>44)&(tx<221)
# branch up to ruins (north) ~ x150
path|=(np.abs(tx-(152+3*np.sin(ty/6)))<1.7)&(ty<py)&(ty>8)
bridge=path&river
path&=~water|bridge
# garden
garden=(tx>=5)&(tx<44)&(ty>=17)&(ty<63)
hedge_ring=garden&~((tx>=6.5)&(tx<42.5)&(ty>=18.5)&(ty<61.5))
gate=(tx>=40)&(np.abs(ty-40)<3.6)
hedge=hedge_ring&~gate
# inner hedge beds
for (a,b,c,d) in [(10,22,20,28),(28,22,38,28),(10,52,20,58),(28,52,38,58)]:
    hedge|=(tx>=a)&(tx<c)&(ty>=b)&(ty<b+1.2)
    hedge|=(tx>=a)&(tx<c)&(ty>=d-1.2)&(ty<d)
fd=np.hypot(tx-24,ty-40)
pav=garden&(((np.abs(ty-40)<2)&(tx>14))|((np.abs(tx-24)<2)&(np.abs(ty-40)<14))|(fd<7))
fountain=fd<4
# ruins (north, few pillars) + rocks
solid_extra=np.zeros((TH,TW),bool)
rocks=[(70,20),(84,62),(118,24),(170,62),(186,22),(196,58),(60,30),(140,36),(176,30)]
pillars=[(146,10),(150,8),(156,9),(160,12),(144,15),(161,16)]
trees=[]
for _ in range(400):
    x,y=random.uniform(6,215),random.uniform(6,74)
    if 44<x<205 and 26<y<54 and not(118<x<140): continue  # keep arena empty
    if 5<x<44 and 17<y<63: 
        if not ((7<x<10 or 38<x<41) and (20<y<34 or 46<y<60)): continue
    ix,iy=int(x),int(y)
    if cliff[iy*T,ix*T] or water[iy*T,ix*T] or path[iy*T,ix*T] or hedge[iy*T,ix*T]: continue
    if any(math.hypot(x-a,y-b)<7 for a,b in trees): continue
    if any(math.hypot(x-a,y-b)<4 for a,b in rocks+pillars): continue
    trees.append((x,y))
    if len(trees)>=38: break
# --- paint ground ---
img=np.zeros((H,W,3),np.float32)
g=GR*(1-n2[...,None]*.5)+GR2*(n2[...,None]*.5)
g=g*(1-dark[...,None]*.6)+GRD*dark[...,None]*.6
img[:]=g
img[pav]=PAV*(0.95+0.1*n2[pav,None])
p=path&~bridge
img[p]=(PATH*(1-dark[p,None]*.5)+PATHD*dark[p,None]*.5)*(0.93+0.12*n2[p,None])
# shore ring
shore=np.asarray(Image.fromarray((water*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9)))>0
sh=shore&~water&~cliff
img[sh]=SHORE*(0.95+0.1*n2[sh,None])
wd=np.asarray(Image.fromarray((~water*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10)),np.float32)/255
wc=WATD*(1-wd[...,None])+WAT*wd[...,None]
img[water]=wc[water]
# bridge planks
bi=bridge
img[bi]=C('#9a7a58')*(0.85+0.2*((X[bi]//4)%2))[:,None]
img[hedge]=HED*(0.85+0.3*n2[hedge,None])
# cliff with face shading
cl=cliff
cv=CL*(1-n1[...,None]*.4)+CLD*n1[...,None]*.4
cv=cv*(1-dark[...,None]*.35)
img[cl]=cv[cl]
img[cave]=CAVE
img=np.clip(img,0,255).astype(np.uint8)
im=Image.fromarray(img)
d=ImageDraw.Draw(im)
# cliff rim highlight / shadow edges
cm=Image.fromarray((cliff*255).astype(np.uint8))
edge=np.asarray(cm.filter(ImageFilter.FIND_EDGES))>0
a=np.asarray(im).copy(); a[edge&cliff]=(a[edge&cliff]*0.6).astype(np.uint8)
sh2=np.roll(cliff,6,0)&~cliff&~water; a[sh2]=(a[sh2]*0.78).astype(np.uint8)
im=Image.fromarray(a); d=ImageDraw.Draw(im)
# fountain
cx,cy=24*T,40*T
d.ellipse([cx-60,cy-60,cx+60,cy+60],fill='#9b958a',outline='#6f6a62',width=4)
d.ellipse([cx-50,cy-50,cx+50,cy+50],fill='#6f93a3')
d.ellipse([cx-14,cy-14,cx+14,cy+14],fill='#b8b2a2',outline='#6f6a62',width=3)
d.ellipse([cx-6,cy-6,cx+6,cy+6],fill='#d8e6ea')
# sparse flowers
for _ in range(500):
    x,y=random.randrange(W),random.randrange(H)
    if a[y,x].tolist()==img[y,x].tolist() and not(cliff[y,x] or water[y,x] or path[y,x] or pav[y,x] or hedge[y,x] or sh[y,x]) and (x<44*T or random.random()<.35):
        col=random.choice(['#e8e2cf','#d9b8c4','#e4d48a'])
        d.rectangle([x,y,x+1,y+1],fill=col)
# rocks / pillars / trunks (ground layer) -> solids
def blob(x,y,r,f,o):
    d.ellipse([x-r,y-r*.8,x+r,y+r*.8],fill=f,outline=o,width=2); d.ellipse([x-r*.5,y-r*.6,x+r*.1,y-r*.2],fill='#a4a4a0')
for x,y in rocks: blob(x*T,y*T,14,'#8a8a88','#55575b'); solid_extra[int(y),int(x)]=True
for x,y in pillars:
    X0,Y0=x*T,y*T; d.rectangle([X0-6,Y0-14,X0+6,Y0+6],fill='#a7a39a',outline='#5d5f62',width=2); d.rectangle([X0-8,Y0-18,X0+8,Y0-12],fill='#bdb8ad',outline='#5d5f62')
    solid_extra[int(y),int(x)]=True
for x,y in trees:
    X0,Y0=x*T,y*T; d.ellipse([X0-12,Y0+4,X0+16,Y0+14],fill=(60,70,58)); d.rectangle([X0-4,Y0-6,X0+4,Y0+10],fill='#5b4636',outline='#3c2f26')
    solid_extra[int(y),int(x)]=True
im.save('ground_layer.png')
# canopy
can=Image.new('RGBA',(W,H),(0,0,0,0)); cd=ImageDraw.Draw(can)
for x,y in trees:
    X0,Y0=x*T,y*T-14; dk=max(0,min(1,(x-150)/70))
    base=tuple(int(v*(1-.35*dk)) for v in (78,104,72)); hi=tuple(int(v*(1-.35*dk)) for v in (112,140,98))
    for ox,oy,r in [(-10,4,16),(10,4,16),(0,-8,18)]: cd.ellipse([X0+ox-r,Y0+oy-r,X0+ox+r,Y0+oy+r],fill=base+(255,),outline=(46,58,44,255),width=2)
    cd.ellipse([X0-12,Y0-18,X0+4,Y0-4],fill=hi+(255,))
can.save('canopy_layer.png')
# collision per tile: 0 walk,1 solid,2 water
def tilemaj(m): return m.reshape(TH,T,TW,T).mean((1,3))>0.5
col=np.zeros((TH,TW),np.uint8)
col[tilemaj(water)&~tilemaj(bridge)]=2
col[tilemaj(cliff)|tilemaj(hedge)|tilemaj(fountain)|solid_extra]=1
cavet=tilemaj(cave); col[cavet]=0
json.dump({'tile':16,'width':TW,'height':TH,'legend':{'0':'walkable','1':'solid','2':'water (blocks player, not arrows)'},'cave_mouth_tiles':np.argwhere(cavet).tolist()[:1],'spawn':[20,46],'data':col.flatten().tolist()},open('collision.json','w'))
pal=np.array([[0,0,0,0],[220,60,60,170],[60,120,230,170]],np.uint8)
Image.fromarray(pal[col]).resize((W,H),Image.NEAREST).save('collision.png')
# tileset: sample/paint tiles
tiles=[]
def tile_from(x,y): return im.crop((x*T,y*T,x*T+T,y*T+T)).convert('RGBA')
def find(mask,lo=0.99):
    m=mask.reshape(TH,T,TW,T).mean((1,3))
    while True:
        ys,xs=np.where(m>=lo)
        if len(ys): i=len(ys)//2; return tile_from(xs[i],ys[i])
        lo-=0.1
def edge_find(m_in,cond):
    m=m_in.reshape(TH,T,TW,T).mean((1,3))
    for y in range(1,TH-1):
        for x in range(1,TW-1):
            if 0.35<m[y,x]<0.65 and cond(m,y,x): return tile_from(x,y)
    return find(m_in,0.5)
named=[('grass',find(~cliff&~water&~path&~pav&~sh&(dark<.1))),('grass_alt',tile_from(70,45)),('grass_dark',find(~cliff&~water&~path&~cave&~sh&(dark>.6))),
('flowers',None),('path',find(path&~bridge&(dark<.2))),('path_dark',find(path&(dark>.7))),('paving',find(pav&~fountain)),('shore_sand',find(sh,0.9)),
('water',find(lake,1)),('water_edge_n',edge_find(water,lambda m,y,x:m[y+1,x]>.9 and m[y-1,x]<.1)),('water_edge_s',edge_find(water,lambda m,y,x:m[y-1,x]>.9 and m[y+1,x]<.1)),
('water_edge_w',edge_find(water,lambda m,y,x:m[y,x+1]>.9 and m[y,x-1]<.1)),('water_edge_e',edge_find(water,lambda m,y,x:m[y,x-1]>.9 and m[y,x+1]<.1)),
('bridge',find(bridge,0.9)),('hedge',find(hedge,1)),('cliff',find(cliff&(dark<.3),1)),('cliff_dark',find(cliff&(dark>.8),1)),
('cliff_edge_s',edge_find(cliff,lambda m,y,x:m[y-1,x]>.9 and m[y+1,x]<.1)),('cave_mouth',find(cave,1)),('rock',tile_from(*rocks[0])),('pillar',tile_from(*pillars[0])),('tree_trunk',tile_from(int(trees[0][0]),int(trees[0][1])))]
fl=named[0][1].copy(); fd2=ImageDraw.Draw(fl)
for p_,c_ in [((3,4),'#e8e2cf'),((11,9),'#d9b8c4'),((6,12),'#e4d48a')]: fd2.rectangle([p_[0],p_[1],p_[0]+1,p_[1]+1],fill=c_)
named[3]=('flowers',fl)
# fountain 8x8 tiles block, cave 
fblock=[(f'fountain_{i}_{j}',tile_from(20+i,36+j)) for j in range(8) for i in range(8)]
allt=named+fblock
cols=16; rows=math.ceil(len(allt)/cols)
ts=Image.new('RGBA',(cols*T,rows*T),(0,0,0,0)); meta={}
for i,(n,t) in enumerate(allt):
    ts.paste(t,((i%cols)*T,(i//cols)*T)); meta[n]={'id':i,'x':(i%cols)*T,'y':(i//cols)*T,'collision':'water' if n.startswith('water') and n!='water_edge' else ('solid' if n.split('_')[0] in('hedge','cliff','cave','rock','pillar','tree','fountain') and n!='cave_mouth' else 'walkable')}
meta['cave_mouth']['collision']='walkable (trigger: enter cave)'
ts.save('tileset_16.png'); ts.resize((ts.width*4,ts.height*4),Image.NEAREST).save('tileset_16_x4.png')
json.dump({'tile_size':16,'columns':cols,'tiles':meta,'note':'water_edge_* = shore transitions; fountain_i_j = 8x8 multi-tile landmark'},open('tileset.json','w'),indent=1)
# anim: grass (4) and water (6) 16x16 frames
gs=Image.new('RGBA',(T*4,T),(0,0,0,0))
for f in range(4):
    t=Image.new('RGBA',(T,T),(0,0,0,0)); td=ImageDraw.Draw(t); sw=[0,1,0,-1][f]
    for bx in (3,8,12): td.line([bx,14,bx+sw,8],fill=(96,122,84,255),width=1); td.line([bx+1,14,bx+1+sw,10],fill=(122,146,104,255))
    gs.paste(t,(f*T,0))
gs.save('anim/grass_tuft_4f.png'); gs.resize((gs.width*6,gs.height*6),Image.NEAREST).save('anim/grass_tuft_4f_x6.png')
ws=Image.new('RGBA',(T*6,T))
for f in range(6):
    t=Image.new('RGBA',(T,T),tuple(WAT.astype(int))+(255,)); td=ImageDraw.Draw(t)
    for k,(yy) in enumerate((3,9,14)):
        x0=(f*3+k*6)%T; td.line([x0,yy,x0+4,yy],fill=(150,182,192,255)); td.line([x0-T,yy,x0-T+4,yy],fill=(150,182,192,255))
    ws.paste(t,(f*T,0))
ws.save('anim/water_6f.png'); ws.resize((ws.width*6,ws.height*6),Image.NEAREST).save('anim/water_6f_x6.png')
# preview
pv=im.convert('RGBA'); pv.alpha_composite(can)
pv.save('preview_full.png')
pv.resize((W//2,H//2),Image.LANCZOS).save('preview.png')
pv.crop((0,24*T,72*T,58*T)).resize((72*T*2//2*1,34*T),Image.NEAREST).save('preview_garden_crop.png')
pv.crop((168*T,22*T,TW*T,58*T)).resize(((TW-168)*T*2,36*T*2),Image.NEAREST).save('preview_cave_crop_2x.png')
print(W,H,len(trees),len(allt))
