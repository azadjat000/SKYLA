from __future__ import annotations
import shutil,sys
from .ai import Ollama
def doctor(cfg):
 checks=[]
 checks.append({'name':'python','status':'PASS','detail':sys.version.split()[0]})
 checks.append({'name':'database','status':'PASS' if cfg.db_path.parent.exists() else 'FAIL','detail':str(cfg.db_path)})
 checks.append({'name':'ollama','status':'PASS' if Ollama(cfg.ollama_url).available() else 'WARN','detail':cfg.ollama_url})
 for binary in ('pw-record','git'):
  checks.append({'name':binary,'status':'PASS' if shutil.which(binary) else 'WARN','detail':'installed' if shutil.which(binary) else 'not found'})
 return checks
