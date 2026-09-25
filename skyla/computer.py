from __future__ import annotations
import os, platform, shutil, subprocess, time
class Computer:
    APPS={"open_chrome":["google-chrome","google-chrome-stable","chromium"],"open_firefox":["firefox"],"open_terminal":["x-terminal-emulator","gnome-terminal","konsole"],"open_files":["cinnamon nemo","nemo"],"open_calculator":["gnome-calculator","kcalc"]}
    def launch(self,intent):
        candidates=self.APPS.get(intent,[])
        for candidate in candidates:
            parts=candidate.split(); binary=shutil.which(parts[0])
            if binary:
                subprocess.Popen(parts, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); return f"Opening {parts[0]}."
        return f"No supported executable found for {intent}."
class SystemMonitor:
    def snapshot(self):
        data={"platform":platform.platform(),"kernel":platform.release(),"hostname":platform.node(),"uptime_seconds":None,"cpu_percent":None,"memory_percent":None,"disk_percent":None,"temperatures":{}}
        try:
            import psutil
            data.update(cpu_percent=psutil.cpu_percent(interval=0.1),memory_percent=psutil.virtual_memory().percent,disk_percent=psutil.disk_usage('/').percent,uptime_seconds=int(time.time()-psutil.boot_time()))
            data["memory"]={"total":psutil.virtual_memory().total,"available":psutil.virtual_memory().available}; data["disk"]={"free":psutil.disk_usage('/').free,"total":psutil.disk_usage('/').total}
            try: data["temperatures"]={k:[x.current for x in v] for k,v in psutil.sensors_temperatures().items()}
            except Exception: pass
        except ImportError: pass
        return data
