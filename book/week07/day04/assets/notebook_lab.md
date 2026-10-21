# Exemple exécutable autonome

Ce fragment illustre le concept du jour. Le moteur complet et ses scénarios sont dans examples/week07.

```python
now = 1000
attempts = 0
ready_at = now
history = []
while attempts < 3:
    now = max(now, ready_at)
    attempts += 1
    history.append(now)
    ready_at = now + 2 ** attempts
assert history == [1000, 1002, 1006]
print({"attempt_times": history, "terminal": "dead_letter"})
```
