import unittest, asyncio
from powerx.final.resources.queue import ConcurrencyGate
class T(unittest.IsolatedAsyncioTestCase):
    async def test_gate(self):
        g=ConcurrencyGate(1)
        async with g.slot():
            self.assertTrue(True)
if __name__=="__main__":unittest.main()
