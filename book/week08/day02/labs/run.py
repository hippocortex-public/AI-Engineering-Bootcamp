"""Scénario J2, lancement depuis n’importe quel répertoire."""
from pathlib import Path
import json
import sys
root=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(root))
from examples.week08.demo import scenario
result=scenario(2)
print(json.dumps(result,ensure_ascii=False,indent=2))
