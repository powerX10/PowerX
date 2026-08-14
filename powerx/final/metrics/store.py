import aiosqlite
import time

SCHEMA = '''
CREATE TABLE IF NOT EXISTS usage_events(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts INTEGER NOT NULL,
  request_id TEXT,
  task TEXT,
  model_id TEXT,
  runtime TEXT,
  latency_ms INTEGER,
  ok INTEGER NOT NULL,
  input_chars INTEGER DEFAULT 0,
  output_chars INTEGER DEFAULT 0
);
'''

class UsageStore:
    def __init__(self, path: str = "data/powerx-usage.db"):
        self.path = path

    async def init(self):
        async with aiosqlite.connect(self.path) as db:
            await db.executescript(SCHEMA)
            await db.commit()

    async def record(self, **event):
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "INSERT INTO usage_events(ts,request_id,task,model_id,runtime,latency_ms,ok,input_chars,output_chars) VALUES(?,?,?,?,?,?,?,?,?)",
                (
                    int(time.time()), event.get("request_id"), event.get("task"),
                    event.get("model_id"), event.get("runtime"), event.get("latency_ms"),
                    1 if event.get("ok") else 0, event.get("input_chars",0), event.get("output_chars",0)
                )
            )
            await db.commit()

    async def summary(self):
        async with aiosqlite.connect(self.path) as db:
            cur = await db.execute("SELECT COUNT(*), SUM(ok), AVG(latency_ms) FROM usage_events")
            total, success, avg_latency = await cur.fetchone()
            return {
                "requests": total or 0,
                "successes": success or 0,
                "avg_latency_ms": round(avg_latency or 0, 2),
            }
