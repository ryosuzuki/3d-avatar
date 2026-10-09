from catalog import compile_scene,KINDS
import math

def scene(kind,**p):return compile_scene({'answer':'Test','scene':{'primitives':[{'kind':kind,**p}]}})
for k in KINDS:
 s=scene(k);assert s['strokes'] and all(math.isfinite(z) for p in s['strokes'] for v in p['points'] for z in v)
a=scene('attention',query=[1,0,1],keys=[[1,0,1],[0,1,0],[-1,0,1]])['semanticEvidence'][0]
assert abs(sum(a['weights'])-1)<1e-12 and a['scores'][0]==2/math.sqrt(3)
b=scene('bayes',prior=.01,sensitivity=.9,falsePositive=.05)['semanticEvidence'][0];assert abs(b['posterior']-.009/(.009+.0495))<1e-12
p=scene('projectile',speed=12,angle=45)['semanticEvidence'][0];assert abs(p['range']-144/9.81)<1e-10
p=scene('triangle',a=3,b=4)['semanticEvidence'][0];assert p['hypotenuse']==5
p=scene('circuit',voltage=9,resistance=100)['semanticEvidence'][0];assert p['currentA']==.09
p=scene('lens',focalLength=1,objectDistance=3)['semanticEvidence'][0];assert abs(p['imageDistance']-1.5)<1e-12
p=scene('normal',sigma=.3,mean=-2);assert all(-.8<=pt[0]<=.8 for s in p['strokes'] for pt in s['points'])
p=scene('vector',x=-2,y=2);assert all(-.8<=pt[0]<=.8 for s in p['strokes'] for pt in s['points'])
print('20 catalog defaults; attention, Bayes, projectile, triangle, circuit, lens numeric checks; finite geometry and boundary checks passed')

# Bar height must encode weight proportion with zero baseline, not arbitrary offset.
s=scene('attention',query=[1,0,1],keys=[[1,0,1],[0,1,0],[-1,0,1]])
for j,w in enumerate(s['semanticEvidence'][0]['weights']):
 pts=s['strokes'][j]['points'];assert abs((pts[1][1]-pts[0][1])-.8*w)<1e-12
# Equal normalized x/y units preserve e=0 as a circle and H2O's angle.
s=scene('orbit',eccentricity=0)['strokes'][0]['points'];assert abs(max(p[0] for p in s)-max(p[1] for p in s))<1e-12
s=scene('molecule',formula='H2O')['strokes'];u=s[0]['points'][1];v=s[1]['points'][1];o=s[0]['points'][0];u=[u[i]-o[i] for i in range(2)];v=[v[i]-o[i] for i in range(2)];angle=math.degrees(math.acos(sum(a*b for a,b in zip(u,v))/math.hypot(*u)/math.hypot(*v)));assert abs(angle-104.5)<1e-10
print('Attention bar proportions, circular orbit, H2O rendered-coordinate angle passed')

# Incorrect model arithmetic must never reach display, narration or canonical history.
s=compile_scene({'answer':'Softmax normalizes relevance. Computed weights are 0.71, 0.14, 0.14.','scene':{'primitives':[{'kind':'attention','query':[1,0,1],'keys':[[1,0,1],[0,1,0],[-1,0,1]]}]}})
assert '0.71' not in s['answer'] and '61.34%' in s['answer'] and '0.71' in s['modelAnswer']
print('Canonical answer strips model arithmetic and includes locally computed weights')

s=compile_scene({'answer':'Increasing scale makes weights uniform.','scene':{'primitives':[{'kind':'attention','scale':2,'query':[1,0,1],'keys':[[1,0,1],[0,1,0],[-1,0,1]]}]}})
assert s['semanticEvidence'][0]['weights'][0] > a['weights'][0] and 'strengthens existing score contrasts' in s['answer'] and 'makes weights uniform' not in s['answer']
s=compile_scene({'language':'ja','answer':'テスト','scene':{'primitives':[{'kind':'triangle','a':3,'b':4}]}})
assert '5.000' in s['answer'] and '直角三角形' in s['answer']
s=scene('triangle',a=.5,b=math.sqrt(.75));assert abs(s['semanticEvidence'][0]['hypotenuse']-1)<1e-12
print('Multiplicative attention, Japanese canonical facts, auxiliary unit-triangle bounds passed')

for angle in [30,45,80]:
 s=scene('projectile',speed=12,angle=angle);curve=next(x['points'] for x in s['strokes'] if len(x['points'])==101);o,u,v=curve[:3];s1=(u[1]-o[1])/(u[0]-o[0]);s2=(v[1]-o[1])/(v[0]-o[0]);assert abs(2*s1-s2-math.tan(math.radians(angle)))<1e-10
a=next(x['points'] for x in scene('projectile',speed=12,angle=45)['strokes'] if len(x['points'])==101);b=next(x['points'] for x in scene('projectile',speed=12,angle=30)['strokes'] if len(x['points'])==101);assert abs(a[-1][0]-b[-1][0])>.1 and abs(max(p[1] for p in a)-max(p[1] for p in b))>.1
print('Projectile launch angle preserved by equal geometric axis units; angle change changes curve, not only labels')

s=scene('flow',inputs=['Light','Water','CO2'],process='Photosynthesis',outputs=['Sugar','Oxygen']);assert s['semanticEvidence'][0]['layout']=='input-process-output' and len(s['strokes'])==16
assert all(abs(v[0])<=.9 and abs(v[1])<=.8 for st in s['strokes'] for v in st['points'])
print('Parallel input/process/output flow has three merging inputs and two branching outputs, within board bounds')
