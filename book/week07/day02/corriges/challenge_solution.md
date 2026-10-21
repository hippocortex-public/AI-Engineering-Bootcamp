# Solution du challenge

Utiliser tempfile.TemporaryDirectory et Engine(path). Faire ingest, close, puis Engine(path). Vérifier received, appeler process, vérifier awaiting_review. Le test test_restart_durability fournit cette séquence. Ne pas utiliser :memory:, car une nouvelle connexion aurait une nouvelle base.
