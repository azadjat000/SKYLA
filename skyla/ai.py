from __future__ import annotations
import json, urllib.request
class Ollama:
    def __init__(self,url): self.url=url.rstrip('/')
    def models(self):
        try:
            with urllib.request.urlopen(self.url+'/api/tags',timeout=2) as r: return json.loads(r.read()).get('models',[])
        except Exception: return []
    def available(self): return bool(self.models())
    def chat(self,prompt,model='qwen3:4b'):
        body=json.dumps({'model':model,'prompt':prompt,'stream':False}).encode(); req=urllib.request.Request(self.url+'/api/generate',body,{'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=120) as r: return json.loads(r.read()).get('response','').strip()
class AIRouter:
    def __init__(self,ollama): self.ollama=ollama
    def model_for(self,text):
        low=text.lower(); return 'qwen2.5-coder:7b' if any(x in low for x in ('code','python','debug','error')) else 'deepseek-r1:7b' if any(x in low for x in ('hard','complex','deeply','reason')) else 'qwen3:4b'
    def answer(self,text):
        model=self.model_for(text)
        try: return self.ollama.chat(text,model),model
        except Exception: return "Ollama is unavailable; deterministic and local features remain operational.",None
