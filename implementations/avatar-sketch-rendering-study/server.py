from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import json,numpy as np
from shapely.geometry import Polygon
from inflate import inflate
R=Path(__file__).parent
class H(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(R),**kw)
 def log_message(self,*a):pass
 def end_headers(self):
  self.send_header('Cross-Origin-Opener-Policy','same-origin');self.send_header('Cross-Origin-Embedder-Policy','require-corp');self.send_header('Cache-Control','no-store');super().end_headers()
 def do_POST(self):
  try:
   if self.path!='/api/inflate':raise ValueError('Unsupported endpoint')
   n=int(self.headers.get('Content-Length',0));assert 0<n<32768
   obj=json.loads(self.rfile.read(n));points=np.asarray(obj['points'],dtype=float);assert 3<=len(points)<=256 and points.shape[1]==2 and np.isfinite(points).all();thickness=float(obj.get('thickness',.32));assert .01<=thickness<=1
   mesh=inflate(points,thickness,subdivisions=2);center=mesh.bounds.mean(0);factor=.85/np.ptp(mesh.vertices,axis=0).max();poly=Polygon(points);cent=np.array(poly.centroid.coords[0]);span=np.ptp(points,axis=0).max();boundary=(points-cent)/span;boundary=(np.c_[boundary,np.zeros(len(points))]-center)*factor;vertices=(mesh.vertices-center)*factor
   data={'name':'fallback','model':'Immediate closed-boundary inflation','vertices':vertices.tolist(),'faces':mesh.faces.tolist(),'adjacency':mesh.face_adjacency.tolist(),'edges':mesh.face_adjacency_edges.tolist(),'sourceStrokePaths':[np.vstack([boundary,boundary[0]]).tolist()],'sourceStrokeIdentity':'Actual uploaded polygon points, no category lookup','registration':{'exactBoundaryXY':True},'conditionedImage':None,'fallbackWatertight':bool(mesh.is_watertight),'cueTimes':{'drawEnd':4,'imageEnd':4,'morphEnd':7,'turnStart':8}};status=200
  except Exception as e:data={'error':str(e) if isinstance(e,(ValueError,AssertionError)) else type(e).__name__};status=400
  payload=json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)
 def do_GET(self):
  if '..' in self.path or self.path.split('?')[0].endswith(('.py','.md','.lock')):self.send_error(404);return
  super().do_GET()
ThreadingHTTPServer(('127.0.0.1',8842),H).serve_forever()
