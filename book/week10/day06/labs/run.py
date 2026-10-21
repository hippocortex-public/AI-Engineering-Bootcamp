"""Scénario J6, lancé depuis n’importe quel dossier."""
from pathlib import Path
import sys
import json
root=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(root))
from examples.week10.demo import scenario
print(json.dumps(scenario(6),ensure_ascii=False,allow_nan=False,indent=2))
