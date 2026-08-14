import asyncio
from contextlib import asynccontextmanager

class ConcurrencyGate:
    def __init__(self, max_concurrent: int = 2):
        if max_concurrent < 1: raise ValueError("max_concurrent must be >=1")
        self._sem = asyncio.Semaphore(max_concurrent)

    @asynccontextmanager
    async def slot(self):
        await self._sem.acquire()
        try:
            yield
        finally:
            self._sem.release()
