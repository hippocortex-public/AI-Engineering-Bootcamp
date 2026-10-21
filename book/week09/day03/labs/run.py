"""Scénario J3, exécutable depuis n’importe quel dossier."""
from pathlib import Path
import sys
import json
root=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(root))
from examples.week09.demo import scenario
print(json.dumps(scenario(3),ensure_ascii=False,allow_nan=False,indent=2))
