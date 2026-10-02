from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass
from threading import Lock
from time import monotonic

from .auth import Principal


class QuotaExceeded(Exception):
    def __init__(self, retry_after: int) -> None:
        super().__init__("Quota exceeded")
        self.retry_after = retry_after


@dataclass
class Window:
    started: float
    count: int = 0


class FixedWindowLimiter:
    """Fenêtre locale par identité ; atomique entre threads d'un processus."""

    def __init__(self, limit: int = 10, seconds: float = 60, clock: Callable[[], float] = monotonic) -> None:
        if limit < 1 or not math.isfinite(seconds) or seconds <= 0:
            raise ValueError("Quota and duration must be positive")
        self.limit = limit
        self.seconds = seconds
        self.clock = clock
        self._windows: dict[tuple[str, str], Window] = {}
        self._lock = Lock()

    def consume(self, principal: Principal) -> None:
        key = (principal.tenant, principal.subject)
        with self._lock:
            now = self.clock()
            window = self._windows.get(key)
            if window is None or now - window.started >= self.seconds:
                window = Window(now)
                self._windows[key] = window
            if window.count >= self.limit:
                remaining = self.seconds - (now - window.started)
                raise QuotaExceeded(max(1, math.ceil(remaining)))
            window.count += 1
