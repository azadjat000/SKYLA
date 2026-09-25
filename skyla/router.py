from dataclasses import dataclass
import re
@dataclass
class Intent: name:str; confidence:float; slots:dict
class Router:
    patterns=[("open_chrome",r"\b(open|launch|start)?\s*(google\s+)?chrome\s*(open|khol[o|o]|karo)?\b"),("open_firefox",r"\b(open|launch|start)\s*firefox|firefox\s*(khol|open)"),("open_terminal",r"\b(open|launch|start)\s*(the\s*)?terminal\b|terminal\s*(kholo|open|karo)"),("open_files",r"\b(open|launch|show)\s*(files|file manager)|file\s*khol"),("open_calculator",r"\b(open|launch)\s*(calculator|calc)"),("system_info",r"\b(system|ram|memory|cpu|disk|status|uptime|temperature).*(info|information|usage|status|use|report)?\b|how much ram"),("news",r"\b(news|headlines|latest news)\b"),("coding",r"\b(write|debug|fix|explain|review)\b.*\b(code|python|error|bug|program)\b"),("remember",r"\b(remember|yaad rakho|yaad rakhna)\b"),("memory_search",r"\b(what do you remember|recall|remember about|kya yaad)\b")]
    def route(self,text):
        t=re.sub(r"[^\w\s?]"," ",text.lower()).strip()
        for name, pat in self.patterns:
            if re.search(pat,t): return Intent(name,0.96,{"text":text})
        return Intent("chat",0.35,{"text":text})
