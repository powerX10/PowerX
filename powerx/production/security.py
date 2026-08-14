from __future__ import annotations
import hashlib
import hmac
import os
import time
from collections import defaultdict, deque


class APIKeyValidator:
    def __init__(self, expected_key: str | None = None):
        self.expected_key = expected_key or os.getenv("POWERX_API_KEY")

    def configured(self) -> bool:
        return bool(self.expected_key)

    def validate(self, supplied: str | None) -> bool:
        if not self.expected_key or not supplied:
            return False
        return hmac.compare_digest(self.expected_key, supplied)


class SlidingWindowRateLimiter:
    def __init__(self, requests: int = 60, window_seconds: int = 60):
        self.requests = requests
        self.window_seconds = window_seconds
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, identity: str, now: float | None = None) -> bool:
        now = time.time() if now is None else now
        q = self._hits[identity]
        cutoff = now - self.window_seconds

        while q and q[0] <= cutoff:
            q.popleft()

        if len(q) >= self.requests:
            return False

        q.append(now)
        return True


def key_fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:12]
