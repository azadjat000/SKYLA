from __future__ import annotations
import re, time
class Security:
    SAFE={'open_chrome','open_firefox','open_files','open_calculator','system_info','memory_search','remember','news','chat'}
    RISK={'open_terminal':'LOW','coding':'MEDIUM','delete_file':'HIGH','install_package':'HIGH','shutdown':'CRITICAL','shell':'CRITICAL'}
    def risk(self,intent): return 'SAFE' if intent in self.SAFE else self.RISK.get(intent,'MEDIUM')
    def allowed(self,intent,confirmed=False): return self.risk(intent) in ('SAFE','LOW') or confirmed
class SkylaCore:
    def __init__(self,config):
        from .database import Database
        from .router import Router
        from .computer import Computer,SystemMonitor
        from .ai import AIRouter,Ollama
        self.config=config; self.db=Database(config.db_path); self.router=Router(); self.computer=Computer(); self.system=SystemMonitor(); self.ai=AIRouter(Ollama(config.ollama_url)); self.security=Security()
    def handle(self,text,confirmed=False):
        started=time.perf_counter(); intent=self.router.route(text); name=intent.name; result=''
        if not self.security.allowed(name,confirmed): result=f"Confirmation required for {name} ({self.security.risk(name)} risk)."
        elif name.startswith('open_'): result=self.computer.launch(name)
        elif name=='system_info': result=self.system.snapshot()
        elif name=='remember':
            m=re.search(r'(?:remember|yaad rakho)(?: that)?\s+(.+?)\s*(?:is|=)\s*(.+)$',text,re.I); result='Tell me what to remember.' if not m else (self.db.remember(m.group(1).strip(),m.group(2).strip()),'Saved.')[1]
        elif name=='memory_search': result=self.db.search_memory(text)
        elif name=='chat': result,model=self.ai.answer(text)
        elif name=='news': result='News requires an explicitly configured web provider; no current web data is being fabricated.'
        else: result='This capability is not yet available.'
        self.db.log(user_input=text,intent=name,confidence=intent.confidence,module='core',action=name,result=str(result),latency_ms=(time.perf_counter()-started)*1000)
        return {'intent':name,'confidence':intent.confidence,'response':result}
