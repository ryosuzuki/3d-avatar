"""Validated semantic spatial geometry. No model-supplied vertices are rendered."""
import math
PALETTE={'O':'#ffb094','H':'#c0efff','C':'#c8c7ee'}
def compile_scene(v):
 if not isinstance(v.get('answer'),str) or len(v['answer'])>2000:raise ValueError('Invalid explanation')
 scene=v.get('scene',{});items=scene.get('primitives',[])
 if not 1<=len(items)<=4:raise ValueError('Use one to four semantic primitives')
 # Molecular comparisons occupy the whole board; explanatory concept boxes would obscure topology.
 if any(p.get('kind')=='molecule' for p in items):items=[p for p in items if p.get('kind')=='molecule'][:2]
 elif any(p.get('kind')=='attention' for p in items):items=[p for p in items if p.get('kind')=='attention'][:1]
 strokes=[];labels=[];evidence=[]
 def line(ps,c='#bce9e0',role='outline'):
  strokes.append({'points':ps,'color':c,'role':role})
 def label(s,x,y):labels.append({'text':str(s)[:30],'x':x,'y':y})
 def sphere(center,r,element):
  x,y,z=center;c=PALETTE[element]
  # Each meridian starts as the same circle and unfolds around its vertical axis.
  for angle in [0,math.pi/3,2*math.pi/3]:
   pts=[];flat=[]
   for i in range(49):
    t=i/48*math.tau;pts.append([x+r*math.cos(t)*math.cos(angle),y+r*math.sin(t),z+r*math.cos(t)*math.sin(angle)]);flat.append([x+r*math.cos(t),y+r*math.sin(t),0])
   strokes.append({'points':pts,'flatPoints':flat,'color':c,'role':'atom'})
  label(element,x-.035,y-.19)
 def arrow(a,b,c):
  line([a,b],c,'vector');d=[b[i]-a[i] for i in range(3)];n=math.sqrt(sum(t*t for t in d)) or 1;d=[t/n for t in d];xy=math.hypot(d[0],d[1]);normal=[-d[1]/xy,d[0]/xy,0] if xy>1e-9 else [1,0,0]
  line([[b[i]-.07*d[i]+.035*normal[i] for i in range(3)],b,[b[i]-.07*d[i]-.035*normal[i] for i in range(3)]],c,'arrowhead')
 for index,p in enumerate(items):
  kind=p.get('kind')
  if kind=='molecule':
   formula=p.get('formula');cx=(-.48 if index==0 else .48) if len(items)>1 else 0;cy=.08
   if formula=='H2O':
    angle=math.radians(52.25);length=.36;centers=[[cx,cy,.15],[cx-length*math.sin(angle),cy-length*math.cos(angle),.15],[cx+length*math.sin(angle),cy-length*math.cos(angle),.15]];elements=['O','H','H'];bonds=[(0,1,1),(0,2,1)];bondangle=104.5
   elif formula=='CO2':
    centers=[[cx,cy,.15],[cx-.34,cy,.15],[cx+.34,cy,.15]];elements=['C','O','O'];bonds=[(0,1,2),(0,2,2)];bondangle=180
   else:raise ValueError('Unsupported molecular topology; use a concept diagram instead')
   for a,b,order in bonds:
    for j in range(order):
     offset=(j-(order-1)/2)*.035;line([[centers[a][0],centers[a][1]+offset,.15],[centers[b][0],centers[b][1]+offset,.15]],'#f5dfac','bond')
   for c,e in zip(centers,elements):sphere(c,.10 if e!='H' else .075,e)
   label(formula+' · '+str(bondangle)+'°',cx-.27,.52)
   evidence.append({'kind':kind,'formula':formula,'atoms':elements,'centers':centers,'bonds':bonds,'angleDegrees':bondangle})
  elif kind=='attention':
   q=p.get('query');keys=p.get('keys')
   if not isinstance(q,list) or len(q)!=3 or not isinstance(keys,list) or not 1<=len(keys)<=3:raise ValueError('Attention requires 3D teaching query and up to three keys')
   if any(not isinstance(a,(int,float)) or not math.isfinite(a) or abs(a)>10 for vec in [q]+keys for a in vec) or any(len(k)!=3 for k in keys):raise ValueError('Invalid attention vectors')
   dots=[sum(a*b for a,b in zip(q,k)) for k in keys];scores=[d/math.sqrt(3) for d in dots];mx=max(scores);ex=[math.exp(s-mx) for s in scores];weights=[e/sum(ex) for e in ex]
   scale=.32/max(1,max(abs(a) for vec in [q]+keys for a in vec));colors=['#a2f4e4','#ffd095','#cbb5ff','#e4b5d4']
   for j,vec in enumerate([q]+keys):
    origin=[-.62+j*.42,-.1,.12];end=[origin[0]+vec[0]*scale,origin[1]+vec[1]*scale,origin[2]+vec[2]*scale];arrow(origin,end,colors[j]);label('q' if j==0 else chr(64+j),origin[0]-.035,.42)
   label('q: '+str(q),-.65,.78)
   for j,(d,w) in enumerate(zip(dots,weights)):label(chr(65+j)+f' · {w*100:.1f}%',-.65+j*.75,-.48)
   label('dot: '+', '.join(f'{d:g}' for d in dots),-.45,-.80)
   evidence.append({'kind':kind,'query':q,'keys':keys,'dots':dots,'scaledScores':scores,'weights':weights,'dimension':3,'teachingProjection':True})
  elif kind in ('diagram','vector','ring'):
   if kind=='vector':
    vec=p.get('components',[1,1,0]);vec=[max(-2,min(2,float(a))) for a in vec[:3]]
    if len(vec)!=3:raise ValueError('Vector requires three components')
    arrow([-.4,-.3,0],[vec[0]*.3,vec[1]*.3,vec[2]*.3],'#a2f4e4');label(p.get('label','Illustrative vector'),-.5,.6)
   elif kind=='ring':
    line([[.5*math.cos(i/64*math.tau),.3*math.sin(i/64*math.tau),.25*math.sin(i/64*math.tau)] for i in range(65)],'#ffd095');label(p.get('label','Illustrative ring'),-.5,.6)
   else:
    nodes=p.get('nodes',['Input','Relationship','Outcome'])[:4]
    for j,n in enumerate(nodes):
     x=-.72+j*1.44/max(1,len(nodes)-1);line([[x-.12,-.15,0],[x+.12,-.15,0],[x+.12,.15,.12],[x-.12,.15,.12],[x-.12,-.15,0]],'#a2f4e4');label(n,x-.12,.32)
     if j:arrow([x-1.44/max(1,len(nodes)-1)+.13,0,0],[x-.14,0,.05],'#ffd095')
   evidence.append({'kind':kind,'illustrative':True})
  else:raise ValueError('Unsupported semantic primitive')
 v.update({'strokes':strokes,'labels':labels,'motion':{'kind':'none','speed':1,'amplitude':0},'semanticEvidence':evidence,'title':str(v.get('title','Explanation'))[:100]})
 v['limits']=str(v.get('limits',''))[:600]+' · Semantic geometry is validated; this is an educational schematic, not atom-scale or a trained model visualization.'
 return v
