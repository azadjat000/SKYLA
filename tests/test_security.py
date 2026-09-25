from skyla.core import Security

def test_security():
 s=Security(); assert s.allowed('open_chrome'); assert not s.allowed('shutdown'); assert s.allowed('shutdown',confirmed=True)
