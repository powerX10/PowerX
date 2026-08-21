from __future__ import annotations
import asyncio, uuid
from dataclasses import dataclass, field
from typing import Any
from .runtime import RuntimeBroker
from .schema import PowerXRequest, PowerXResponse

@dataclass
class Job:
    id: str
    request: PowerXRequest
    status: str = "queued"
    result: PowerXResponse | None = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

class JobQueue:
    def __init__(self):
        self.jobs: dict[str, Job] = {}
        self.broker = RuntimeBroker()

    def submit(self, req: PowerXRequest) -> Job:
        job = Job(id=str(uuid.uuid4()), request=req)
        self.jobs[job.id] = job
        asyncio.create_task(self._run(job))
        return job

    async def _run(self, job: Job) -> None:
        job.status = "running"
        try:
            job.result = await self.broker.run(job.request)
            job.status = "done" if job.result.ok else "failed"
            if job.result.errors:
                job.error = "; ".join(job.result.errors)
        except Exception as e:
            job.status = "failed"
            job.error = str(e)

    def get(self, job_id: str) -> Job | None:
        return self.jobs.get(job_id)
