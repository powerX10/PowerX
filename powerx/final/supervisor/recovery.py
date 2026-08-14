import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable

@dataclass
class RestartPolicy:
    retries: int = 3
    base_delay_seconds: float = 2.0

async def retry_async(
    fn: Callable[[], Awaitable],
    policy: RestartPolicy = RestartPolicy(),
):
    last = None
    for attempt in range(policy.retries):
        try:
            return await fn()
        except Exception as exc:
            last = exc
            await asyncio.sleep(policy.base_delay_seconds * (2 ** attempt))
    raise RuntimeError(f"Operation failed after retries: {last}")
