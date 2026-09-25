from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json

def serve(core,cfg):
 class H(BaseHTTPRequestHandler):
  def send(self,code,obj):
   raw=json.dumps(obj,default=str).encode(); self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
  def do_GET(self):
   if self.path=='/api/status': return self.send(200,core.system.snapshot())
   if self.path=='/api/models': return self.send(200,{'models':core.ai.ollama.models()})
   if self.path=='/api/logs': return self.send(200,core.db.logs())
   if self.path=='/api/memory': return self.send(200,core.db.search_memory())
   if self.path=='/api/projects': return self.send(200,[dict(x,exists=__import__('os').path.isdir(x['path'])) for x in cfg.projects])
   if self.path=='/api/voice': return self.send(200,{'device':cfg.audio_device,'sample_rate':cfg.sample_rate,'available':__import__('shutil').which('pw-record') is not None})
   if self.path in ('/','/index.html'):
    raw=b'<h1>SKYLA</h1><p>Local control center</p><script>fetch("/api/status").then(r=>r.json()).then(x=>document.body.innerHTML+="<pre>"+JSON.stringify(x,null,2)+"</pre>")</script>'; self.send_response(200); self.send_header('Content-Type','text/html'); self.end_headers(); self.wfile.write(raw); return
   self.send(404,{'error':'not found'})
  def do_POST(self):
   if self.path not in ('/api/chat','/api/command'): return self.send(404,{'error':'not found'})
   try: body=json.loads(self.rfile.read(int(self.headers.get('Content-Length',0)))); return self.send(200,core.handle(body.get('text',''),bool(body.get('confirmed'))))
   except Exception as e: return self.send(400,{'error':str(e)})
  def log_message(self,*args): pass
 ThreadingHTTPServer((cfg.dashboard_host,cfg.dashboard_port),H).serve_forever()
