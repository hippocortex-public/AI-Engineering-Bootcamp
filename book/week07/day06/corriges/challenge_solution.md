# Solution du challenge

Après process, conserver proposal_hash. Appeler decide deux fois avec approve et reviewer-demo; les deux appels retournent published. Compter publications :1. Appeler reject avec le même hash :Conflict. Le test test_approval_idempotent est la correction exécutable.
