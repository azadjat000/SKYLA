from skyla.config import Config
from skyla.database import Database

def test_memory_persists(tmp_path):
 db=Database(tmp_path/'x.sqlite3'); db.remember('project','SKYLA'); assert db.search_memory('SKYLA')[0]['value']=='SKYLA'

def test_config(tmp_path):
 c=Config(data_dir=tmp_path); assert c.sample_rate==8000
