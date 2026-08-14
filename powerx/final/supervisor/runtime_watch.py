import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable

@dataclass
class WatchedRuntime:
    id: str
    health: Callable[[], Awaitable[bool]]
    restart: Callable[[], Awaitable[None]]

class RuntimeSupervisor:
    def __init__(self, interval_seconds: float = 15.0):
        self.interval_seconds = interval_seconds
        self._stop = asyncio.Event()

    async def run(self, runtimes: list[WatchedRuntime]):
        while not self._stop.is_set():
            for runtime in runtimes:
                try:
                    if not await runtime.health():
                        await runtime.restart()
                except Exception:
                    pass
            try:
                await asyncio.wait_for(self._stop.wait(), timeout=self.interval_seconds)
            except asyncio.TimeoutError:
                pass

    def stop(self):
        self._stop.set()
