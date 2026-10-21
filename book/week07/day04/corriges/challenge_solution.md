# Solution du challenge

Le test test_retry_backoff_and_dead_letter montre les trois échecs avec horloge injectée. Après replay et tick, état awaiting_review. Interroger audit pour event_id : la séquence contient retry, retry, dead_letter, replayed, draft_created. Aucun effet de publication ne doit exister.
