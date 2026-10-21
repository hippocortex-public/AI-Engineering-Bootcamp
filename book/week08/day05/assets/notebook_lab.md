# Lab exécutable

Cellules autonomes à partir du dépôt; aucune requête réseau.

```python
from pathlib import Path
import sys
cwd = Path.cwd().resolve()
root = next((p for p in (cwd, *cwd.parents) if (p / "examples/week08/ops.py").is_file()), None)
assert root is not None, "Ouvrir le notebook depuis le dépôt décompressé"
sys.path.insert(0, str(root))
from copy import deepcopy
from examples.week08.demo import load
from examples.week08.ops import govern
data = load("baseline")
config_hash = data["runs"][0]["config_hash"]
valid = govern(data["manifest"], config_hash, data["policy"], "2026-10-20")
assert valid["accepted"]
changed = deepcopy(data["manifest"])
changed["config_hash"] = "another-configuration"
invalid = govern(changed, config_hash, data["policy"], "2026-10-20")
assert not invalid["accepted"] and "configuration_changed" in invalid["reasons"]
print(valid, invalid)
```
