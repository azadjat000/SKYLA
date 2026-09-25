from skyla.router import Router

def test_deterministic_routes():
 r=Router(); assert r.route('Open Chrome').name=='open_chrome'; assert r.route('Chrome kholo').name=='open_chrome'; assert r.route('Terminal kholo').name=='open_terminal'; assert r.route('what is my RAM usage').name=='system_info'
