import unittest, tempfile, os
from powerx.final.metrics.store import UsageStore
class T(unittest.IsolatedAsyncioTestCase):
    async def test_store(self):
        fd,path=tempfile.mkstemp();os.close(fd)
        try:
            s=UsageStore(path);await s.init();await s.record(request_id="1",task="x",model_id="m",runtime="cpu",latency_ms=10,ok=True)
            d=await s.summary();self.assertEqual(d["requests"],1)
        finally: os.unlink(path)
if __name__=="__main__":unittest.main()
