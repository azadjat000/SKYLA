from __future__ import annotations
import argparse, json
from .config import Config
from .core import SkylaCore
from .doctor import doctor

def main(argv=None):
 p=argparse.ArgumentParser(prog='skyla'); sub=p.add_subparsers(dest='cmd'); sub.add_parser('status'); sub.add_parser('doctor'); sub.add_parser('dashboard'); c=sub.add_parser('command'); c.add_argument('text',nargs='+')
 a=p.parse_args(argv); cfg=Config(); core=SkylaCore(cfg)
 if a.cmd=='doctor': print(json.dumps(doctor(cfg),indent=2)); return
 if a.cmd=='status': print(json.dumps(core.system.snapshot(),indent=2)); return
 if a.cmd=='dashboard': from .dashboard import serve; serve(core,cfg); return
 if a.cmd=='command': print(json.dumps(core.handle(' '.join(a.text)),indent=2)); return
 while True:
  try: text=input('SKYLA> ')
  except (EOFError,KeyboardInterrupt): break
  if text.strip().lower() in {'exit','quit'}: break
  print(core.handle(text)['response'])
if __name__=='__main__': main()
