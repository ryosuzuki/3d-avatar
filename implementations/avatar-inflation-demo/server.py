from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
class H(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(Path(__file__).parent),**kw)
 def log_message(self,*a):pass
 def end_headers(self):
  self.send_header('Cross-Origin-Opener-Policy','same-origin');self.send_header('Cross-Origin-Embedder-Policy','require-corp');super().end_headers()
ThreadingHTTPServer(('127.0.0.1',8832),H).serve_forever()
