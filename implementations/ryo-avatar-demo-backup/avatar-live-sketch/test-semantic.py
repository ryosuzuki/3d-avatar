from semantic import compile_scene
import math
v=compile_scene({'answer':'Compare molecules','scene':{'primitives':[{'kind':'molecule','formula':'H2O'},{'kind':'molecule','formula':'CO2'}]}})
for e in v['semanticEvidence']:
 a,b,c=e['centers'];u=[b[i]-a[i] for i in range(3)];w=[c[i]-a[i] for i in range(3)];angle=math.degrees(math.acos(sum(x*y for x,y in zip(u,w))/math.sqrt(sum(x*x for x in u)*sum(x*x for x in w))))
 assert abs(angle-e['angleDegrees'])<1e-8
 assert len(e['atoms'])==3 and len(e['bonds'])==2
assert v['semanticEvidence'][1]['bonds']==[(0,1,2),(0,2,2)]
for factor in (1,2):
 v=compile_scene({'answer':'Actual teaching attention','scene':{'primitives':[{'kind':'attention','query':[factor,0,0],'keys':[[1,1,0],[-1,0,0]]}]}});e=v['semanticEvidence'][0]
 assert e['dots']==[factor,-factor]
 assert abs(sum(e['weights'])-1)<1e-12
try:compile_scene({'answer':'Unsupported','scene':{'primitives':[{'kind':'molecule','formula':'CH4'}]}})
except ValueError:pass
else:raise AssertionError('Unsupported topology accepted')
print('Verified molecular topology and geometry, scaled softmax, unsupported-topology rejection')
