from __future__ import annotations
import json, os
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class Config:
    data_dir: Path = field(default_factory=lambda: Path(os.getenv("SKYLA_DATA_DIR", "~/.local/share/skyla")).expanduser())
    db_path: Path = field(init=False)
    ollama_url: str = field(default_factory=lambda: os.getenv("SKYLA_OLLAMA_URL", "http://127.0.0.1:11434"))
    dashboard_host: str = field(default_factory=lambda: os.getenv("SKYLA_HOST", "127.0.0.1"))
    dashboard_port: int = field(default_factory=lambda: int(os.getenv("SKYLA_PORT", "8765")))
    default_model: str = field(default_factory=lambda: os.getenv("SKYLA_MODEL", "qwen3:4b"))
    whisper_model: str = field(default_factory=lambda: os.getenv("SKYLA_WHISPER_MODEL", "small"))
    audio_device: str = field(default_factory=lambda: os.getenv("SKYLA_AUDIO_DEVICE", "bluez_input.41_8F_5F_44_62_76.0"))
    sample_rate: int = field(default_factory=lambda: int(os.getenv("SKYLA_SAMPLE_RATE", "8000")))
    projects: list[dict] = field(default_factory=list)
    def __post_init__(self):
        self.db_path = self.data_dir / "skyla.sqlite3"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.projects = self.projects or self._default_projects()
    def _default_projects(self):
        home = Path.home()
        return [{"name":"SKYLA","path":str(home/"Desktop"/"Skyla"),"description":"Personal assistant"}, {"name":"NERA-PC-Control","path":str(home/"Desktop"/"Nera-PC-Control"),"description":"Previous assistant implementation"}, {"name":"MedBillSky","path":str(home/"Desktop"/"MedBillSky"),"description":"Pharmacy management project"}]
    @classmethod
    def load(cls, path: str | Path | None = None):
        cfg = cls()
        if path and Path(path).exists():
            raw = json.loads(Path(path).read_text())
            for key, value in raw.items():
                if hasattr(cfg, key): setattr(cfg, key, Path(value).expanduser() if key == "data_dir" else value)
            cfg.db_path = cfg.data_dir / "skyla.sqlite3"; cfg.data_dir.mkdir(parents=True, exist_ok=True)
        return cfg
