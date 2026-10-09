"""Closed numerical sketch catalog inspired by Jev's select/order/parameter approach.
No generated executable code. Equations and geometry are local, audited functions.
"""
import math,re
from facts import canonical_answer
KINDS=['attention','wave','pendulum','projectile','orbit','spring','growth','decay','normal','bayes','circuit','lens','vector','molecule','flow','bars','triangle','unitcircle','exponential','damped']
C=['#8cebd8','#ffc87c','#c3aeff','#ffaaa2']
def num(p,k,d,lo,hi):
 v=p.get(k,d)
 if not isinstance(v,(int,float)) or not math.isfinite(v):raise ValueError(f'{k} must be a finite number')
 if not lo<=v<=hi:raise ValueError(f'{k} must be between {lo} and {hi} for this sketch family')
 return v
def compile_scene(v):
 items=v.get('scene',{}).get('primitives',[])
 if not 1<=len(items)<=3:raise ValueError('One to three primitives required')
 strokes=[];labels=[];evidence=[];controls=[]
 def line(ps,c=C[0],role='curve'):strokes.append({'points':[[float(x),float(y),0] for x,y in ps],'color':c,'role':role})
 def label(s,x,y,size=38):labels.append({'text':str(s)[:42],'x':x,'y':y,'fontSize':size})
 def arrow(x,y,X,Y,c=C[0]):
  line([(x,y),(X,Y)],c);a=math.atan2(Y-y,X-x);line([(X-.04*math.cos(a-.5),Y-.04*math.sin(a-.5)),(X,Y),(X-.04*math.cos(a+.5),Y-.04*math.sin(a+.5))],c)
 def circle(x,y,r,c=C[0]):line([(x+r*math.cos(j*math.tau/48),y+r*math.sin(j*math.tau/48)) for j in range(49)],c)
 def control(index,k,val,lo,hi,step):controls.append({'index':index,'key':k,'value':val,'min':lo,'max':hi,'step':step})
 # At most one numerical plot dominates the board. Multi-beat explanations are step ordered.
 for i,p in enumerate(items):
  kind=p.get('kind');p=dict(p)
  if kind not in KINDS:raise ValueError('Unknown catalog kind')
  start=len(strokes);metrics={'kind':kind}
  def plot(fn,xmax,ymax,caption,ymin=0,xoffset=0):
   zero=-.43+.82*(0-ymin)/(ymax-ymin)
   arrow(-.78,zero,.78,zero,'#728b9b');arrow(-.78,-.45,-.78,.46,'#728b9b')
   line([(-.76+1.48*j/100,-.43+.82*(fn(xmax*j/100)-ymin)/(ymax-ymin)) for j in range(101)])
   label(caption,-.7,.64);label(f'{ymax:.2g}',-.87,.45,24);label(f'{ymin:.2g}',-.87,-.43,24);label(f'{xoffset:g}',-.78,-.58);label(f'x = {xmax+xoffset:g}',.48,-.58)
  if kind=='triangle':
   a=num(p,'a',3,.1,6);b=num(p,'b',4,.1,6);c=math.hypot(a,b);scale=.9/max(a,b);line([(-.55,-.35),(-.55+scale*a,-.35),(-.55,-.35+scale*b),(-.55,-.35)]);line([(-.55,-.25),(-.45,-.25),(-.45,-.35)],C[1]);label('Right triangle • a² + b² = c²',-.7,.65);label(f'a {a:g} • b {b:g} • c {c:.2f}',-.7,-.6);metrics.update(a=a,b=b,hypotenuse=c);control(i,'a',a,.1,6,.1);control(i,'b',b,.1,6,.1)
  elif kind=='unitcircle':
   angle=num(p,'angle',45,0,360);a=math.radians(angle);circle(0,0,.42);arrow(0,0,.42*math.cos(a),.42*math.sin(a),C[1]);line([(.42*math.cos(a),0),(.42*math.cos(a),.42*math.sin(a))],C[2]);label('Unit circle • x = cos θ • y = sin θ',-.7,.65);label(f'{angle:g}° • sin {math.sin(a):.3f} • cos {math.cos(a):.3f}',-.7,-.6);metrics.update(angleDegrees=angle,sin=math.sin(a),cos=math.cos(a));control(i,'angle',angle,0,360,5)
  elif kind=='exponential':
   rate=num(p,'rate',.1,.02,.3);plot(lambda x:(1+rate)**x,10,(1+rate)**10*1.1,'Compound growth • (1 + r)^t');metrics.update(rate=rate,valueAt10=(1+rate)**10);control(i,'rate',rate,.02,.3,.01)
  elif kind=='damped':
   damping=num(p,'damping',.3,.05,1);freq=num(p,'frequency',1,.2,2);plot(lambda x:math.exp(-damping*x)*math.cos(math.tau*freq*x),6,1.1,'Damped oscillation • exp(-bt) cos(2πft)',-1.1);metrics.update(damping=damping,frequency=freq);control(i,'damping',damping,.05,1,.05)
  elif kind=='attention':
   scale=num(p,'scale',1,.1,4);q=p.get('query',[1,0,1]);ks=p.get('keys',[[1,0,1],[0,1,0],[-1,0,1]])
   if not isinstance(q,list) or len(q)!=3 or not isinstance(ks,list) or len(ks)!=3 or any(not isinstance(k,list) or len(k)!=3 for k in ks):raise ValueError('Attention needs 3 vectors')
   q=[num({'v':a},'v',0,-5,5) for a in q];ks=[[num({'v':a},'v',0,-5,5) for a in k] for k in ks]
   scores=[sum(a*b for a,b in zip(q,k))*scale/math.sqrt(3) for k in ks];ex=[math.exp(s-max(scores)) for s in scores];ws=[e/sum(ex) for e in ex]
   label('Scaled dot product → softmax',-.7,.66);label('q = '+str(q),-.7,.45)
   for j,w in enumerate(ws):
    x=-.65+j*.5;line([(x,-.4),(x,-.4+w*.8),(x+.25,-.4+w*.8),(x+.25,-.4)],C[j]);label(f'{chr(65+j)} {100*w:.1f}%',x,-.58)
   metrics.update(query=q,keys=ks,scores=scores,weights=ws);control(i,'scale',scale,.1,4,.1)
  elif kind in ['wave','pendulum','spring']:
   amp=num(p,'amplitude',.7,.1,1.5);freq=num(p,'frequency',1,.2,3);phase=num(p,'phase',0,0,6.28)
   plot(lambda x:amp*math.sin(math.tau*freq*x+phase),2,1.6,'Sine motion: amplitude × sin(2πft + phase)',-1.6);metrics.update(amplitude=amp,frequency=freq,phase=phase)
   control(i,'amplitude',amp,.1,1.5,.05);control(i,'frequency',freq,.2,3,.1)
  elif kind=='projectile':
   speed=num(p,'speed',12,3,22);angle=num(p,'angle',45,10,80);g=9.81;a=math.radians(angle);T=2*speed*math.sin(a)/g;R=speed*math.cos(a)*T;H=(speed*math.sin(a))**2/(2*g)
   maxX=speed**2/g*1.1;maxY=maxX*.82/1.48
   arrow(-.78,-.43,.78,-.43,'#728b9b');arrow(-.78,-.45,-.78,.46,'#728b9b');line([(-.76+1.48*(R*j/100)/maxX,-.43+.82*((R*j/100)*math.tan(a)-g*(R*j/100)**2/(2*(speed*math.cos(a))**2))/maxY) for j in range(101)])
   label('Projectile • equal axis units • g = 9.81',-.7,.64);label(f'{maxY:.2f} m',-.87,.45,24);label('0',-.87,-.43,24);label('0',-.78,-.58);label(f'x = {maxX:.2f} m',.38,-.58);label(f'range {R:.2f} m • height {H:.2f} m',-.6,.45);metrics.update(range=R,maxHeight=H,flightTime=T,axisMaxX=maxX,axisMaxY=maxY,axisScaleRatio=1);control(i,'angle',angle,10,80,1);control(i,'speed',speed,3,22,.5)
  elif kind=='orbit':
   eccentricity=num(p,'eccentricity',.4,0,.85);b=math.sqrt(1-eccentricity**2);line([(.5*math.cos(j*math.tau/100),.5*b*math.sin(j*math.tau/100)) for j in range(101)]);circle(-.5*eccentricity,0,.04,C[1]);label('Kepler ellipse • star at one focus',-.7,.65);label(f'e = {eccentricity:.2f}',-.3,-.6);metrics.update(eccentricity=eccentricity);control(i,'eccentricity',eccentricity,0,.85,.05)
  elif kind in ['growth','decay']:
   rate=num(p,'rate',.5,.05,2);fn=(lambda x:math.exp(-rate*x)) if kind=='decay' else (lambda x:1/(1+math.exp(-rate*(x-5))))
   plot(fn,10,1.1,'Exponential decay' if kind=='decay' else 'Logistic growth • carrying capacity = 1');metrics.update(rate=rate,valueAt10=fn(10));control(i,'rate',rate,.05,2,.05)
  elif kind=='normal':
   sigma=num(p,'sigma',1,.3,2);mu=num(p,'mean',0,-2,2);plot(lambda x:math.exp(-.5*((x-4-mu)/sigma)**2)/(sigma*math.sqrt(2*math.pi)),8,1.4,'Normal density • horizontal x = -4 to 4',0,-4);metrics.update(sigma=sigma,mean=mu);control(i,'sigma',sigma,.3,2,.1);control(i,'mean',mu,-2,2,.1)
  elif kind=='bayes':
   prior=num(p,'prior',.1,.01,.9);sensitivity=num(p,'sensitivity',.9,.1,.99);fpr=num(p,'falsePositive',.05,.01,.5);post=prior*sensitivity/(prior*sensitivity+(1-prior)*fpr)
   label('Bayes: evidence updates a prior',-.7,.65)
   for j,(n,x) in enumerate([('Prior',prior),('Posterior',post)]):
    y=.22-j*.5;line([(-.7,y),(-.7+1.4*x,y)],C[j]);label(f'{n}: {100*x:.1f}%',-.7,y+.12)
   metrics.update(prior=prior,posterior=post,sensitivity=sensitivity,falsePositive=fpr);control(i,'prior',prior,.01,.9,.01);control(i,'falsePositive',fpr,.01,.5,.01)
  elif kind=='circuit':
   voltage=num(p,'voltage',9,1,24);resistance=num(p,'resistance',100,10,1000);line([(-.65,-.07),(-.65,-.3),(.65,-.3),(.65,.3),(.12,.3)]);line([(-.12,.3),(-.65,.3),(-.65,.07)]);line([(-.77,.07),(-.53,.07)],C[2]);line([(-.72,-.07),(-.58,-.07)],C[2]);line([(-.12,.3),(-.1,.4),(-.05,.2),(0,.4),(.05,.2),(.1,.4),(.12,.3)],C[1]);label('Ideal resistor • I = V/R',-.65,.66);label(f'{voltage:g} V / {resistance:g} Ω = {1000*voltage/resistance:.1f} mA',-.65,-.6);metrics.update(currentA=voltage/resistance,powerW=voltage**2/resistance);control(i,'voltage',voltage,1,24,1);control(i,'resistance',resistance,10,1000,10)
  elif kind=='lens':
   f=num(p,'focalLength',1,.5,2);d=num(p,'objectDistance',3,2.1,6);di=1/(1/f-1/d);line([(0,-.4),(0,.4)]);line([(-.75,0),(.75,0)],'#728b9b');arrow(-.6,0,-.6,.3);arrow(.6,0,.6,-.3*min(1.3,di/d),C[1]);line([(-.6,.3),(0,.3),(.6,-.3*min(1.3,di/d))],C[2]);label('Thin converging lens • not to scale',-.7,.65);label(f'1/f = 1/do + 1/di • di = {di:.2f}',-.7,-.6);metrics.update(imageDistance=di,magnification=-di/d);control(i,'objectDistance',d,2.1,6,.1)
  elif kind=='vector':
   x=num(p,'x',1,-2,2);y=num(p,'y',1,-2,2);line([(-.65,0),(.65,0)],'#728b9b');line([(0,-.45),(0,.45)],'#728b9b');arrow(0,0,.25*x,.25*y);label('Vector • components and magnitude',-.7,.65);label(f'({x:.1f}, {y:.1f}) • norm {math.hypot(x,y):.2f}',-.6,-.6);metrics.update(x=x,y=y,norm=math.hypot(x,y));control(i,'x',x,-2,2,.1);control(i,'y',y,-2,2,.1)
  elif kind=='molecule':
   formula=p.get('formula','H2O')
   if formula not in ['H2O','CO2']:raise ValueError('Only H2O/CO2 molecular topology validated')
   centers=[(0,.1),(-.5*math.sin(math.radians(52.25)),.1-.5*math.cos(math.radians(52.25))),(.5*math.sin(math.radians(52.25)),.1-.5*math.cos(math.radians(52.25)))] if formula=='H2O' else [(0,0),(-.45,0),(.45,0)]
   for x,y in centers[1:]:
    line([(0,centers[0][1]),(x,y)],C[1])
    if formula=='CO2':line([(0,.04),(x,.04)],C[1])
   for j,(x,y) in enumerate(centers):circle(x,y,.1,C[0] if j==0 else C[2]);label(('O' if j==0 else 'H') if formula=='H2O' else ('C' if j==0 else 'O'),x-.03,y-.02)
   label(formula+' • '+('bent 104.5°' if formula=='H2O' else 'linear 180°'),-.6,.65);metrics.update(formula=formula,angleDegrees=104.5 if formula=='H2O' else 180)
  elif kind=='bars':
   values=p.get('values',[.2,.5,.8]);names=p.get('names',['A','B','C']);values=[num({'v':z},'v',.5,0,1) for z in values[:4]]
   for j,z in enumerate(values):
    x=-.7+j*1.4/max(len(values),1);line([(x,-.4),(x,-.4+.8*z),(x+.2,-.4+.8*z),(x+.2,-.4)],C[j]);label(str(names[j] if j<len(names) else j),x,-.58)
   label(p.get('label','Illustrative values • normalized'),-.7,.65);metrics.update(values=values)
  else:
   if 'inputs' in p or 'outputs' in p:
    inputs=p.get('inputs');outputs=p.get('outputs');process=p.get('process','Process')
    if not isinstance(inputs,list) or not isinstance(outputs,list) or not 1<=len(inputs)<=3 or not 1<=len(outputs)<=3:raise ValueError('Input-process-output flow needs 1–3 input labels and 1–3 output labels')
    def box(x,y,n):
     line([(x-.13,y-.08),(x+.13,y-.08),(x+.13,y+.08),(x-.13,y+.08),(x-.13,y-.08)]);label(str(n),x-.12,y+.15,28)
    box(0,0,process)
    for j,n in enumerate(inputs):
     y=((len(inputs)-1)/2-j)*.3;box(-.65,y,n);arrow(-.51,y,-.14,0,C[1])
    for j,n in enumerate(outputs):
     y=((len(outputs)-1)/2-j)*.3;box(.65,y,n);arrow(.14,0,.51,y,C[2])
    label('Inputs → process → outputs',-.7,.65);metrics.update(layout='input-process-output',inputs=inputs,outputs=outputs,process=process)
   else:
    nodes=p.get('nodes',['Input','Process','Output'])[:4]
    for j,n in enumerate(nodes):
     x=-.68+j*1.36/max(1,len(nodes)-1);line([(x-.13,-.12),(x+.13,-.12),(x+.13,.12),(x-.13,.12),(x-.13,-.12)])
     name=str(n).split('(')[0].strip()
     if re.search('attention',name,re.I):name='Attention'
     elif re.search('residual',name,re.I):name='Residual add'
     elif re.search('feed.?forward',name,re.I):name='Feed-forward'
     elif re.search('embedding',name,re.I):name='Embeddings'
     words=name.split();rows=['']
     for word in words:
      if len(rows[-1])+len(word)+1>12 and rows[-1]:
       if len(rows)<2:rows.append('')
       else:rows[-1]=rows[-1][:11]+'…';break
      rows[-1]=(rows[-1]+' '+word).strip()
     for row,text in enumerate(rows[:2]):label(text[:12],x-.12,.35-row*.13,28)
     if j:arrow(x-1.36/max(1,len(nodes)-1)+.14,0,x-.14,0,C[1])
    label('Sequential concept flow',-.7,.65);metrics.update(layout='sequence',nodes=nodes)
  evidence.append(metrics);p['kind']=kind;items[i]=p
  for s in strokes[start:]:s['beat']=i
  for l in labels:
   if 'beat' not in l:l['beat']=i
 raw_answer=str(v.get('answer',''))[:2000];answer,facts=canonical_answer(raw_answer,evidence,items,v.get("language"))
 return {'modelAnswer':raw_answer,'answerFacts':facts,'language':v.get('language','auto'),'answerSource':('Model-generated concept-flow explanation' if all(e['kind']=='flow' for e in evidence) else 'Catalog-authored conceptual beat + canonical local calculations, selected and parameterized by model'),'title':str(v.get('title','Live sketch'))[:90],'answer':answer,'limits':str(v.get('limits','Educational schematic.'))[:700],'scene':{'primitives':items},'strokes':strokes,'labels':labels,'semanticEvidence':evidence,'controls':controls,'motion':{'kind':'none','speed':1,'amplitude':0}}
