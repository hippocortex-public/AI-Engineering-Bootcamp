"""Lancer depuis n’importe quel répertoire; aucun accès réseau."""
from pathlib import Path
import json
import sys
root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(root))
from examples.week07.demo import scenario
print(json.dumps(scenario(6), ensure_ascii=False, indent=2))
