from __future__ import annotations

import json
import os
import sqlite3
import threading
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class BrokerJob:
    id: str
    runtime_class: str
    capability: str
    payload: dict[str, Any]
    status: str
    created_at: float
    claimed_at: float | None = None
    completed_at: float | None = None
    result: dict[str, Any] | None = None
    error: str | None = None


class JobBroker:
    """Small durable SQLite broker for pull workers (Colab/mobile).

    Designed for a single PowerX control API instance. Workers pull jobs by
    runtime_class, then POST results. Jobs survive API process restarts.
    """

    def __init__(self, path: str | None = None):
        self.path = Path(
            os.path.expanduser(
                path
                or os.getenv(
                    "POWERX_BROKER_DB",
                    "~/.local/share/powerx/runtime_broker.sqlite3",
                )
            )
        )
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._init()

    def _connect(self):
        conn = sqlite3.connect(self.path, timeout=30, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init(self):
        with self._connect() as c:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    runtime_class TEXT NOT NULL,
                    capability TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    claimed_at REAL,
                    completed_at REAL,
                    result_json TEXT,
                    error TEXT
                )
                """
            )
            c.execute(
                "CREATE INDEX IF NOT EXISTS idx_jobs_runtime_status "
                "ON jobs(runtime_class, status, created_at)"
            )

    def submit(
        self,
        runtime_class: str,
        capability: str,
        payload: dict[str, Any],
    ) -> BrokerJob:
        now = time.time()
        job_id = uuid.uuid4().hex
        with self._connect() as c:
            c.execute(
                """
                INSERT INTO jobs
                (id, runtime_class, capability, payload_json, status, created_at)
                VALUES (?, ?, ?, ?, 'queued', ?)
                """,
                (
                    job_id,
                    runtime_class,
                    capability,
                    json.dumps(payload),
                    now,
                ),
            )
        return self.get(job_id)

    def pull(self, runtime_class: str, stale_after: float = 900.0) -> BrokerJob | None:
        now = time.time()
        stale_before = now - stale_after

        with self._lock:
            with self._connect() as c:
                c.execute(
                    """
                    UPDATE jobs
                    SET status='queued', claimed_at=NULL
                    WHERE runtime_class=? AND status='running'
                      AND claimed_at IS NOT NULL AND claimed_at < ?
                    """,
                    (runtime_class, stale_before),
                )

                row = c.execute(
                    """
                    SELECT id FROM jobs
                    WHERE runtime_class=? AND status='queued'
                    ORDER BY created_at ASC
                    LIMIT 1
                    """,
                    (runtime_class,),
                ).fetchone()

                if row is None:
                    return None

                c.execute(
                    """
                    UPDATE jobs
                    SET status='running', claimed_at=?
                    WHERE id=? AND status='queued'
                    """,
                    (now, row["id"]),
                )

                if c.total_changes == 0:
                    return None

                job_id = row["id"]

        return self.get(job_id)

    def complete(
        self,
        job_id: str,
        *,
        ok: bool,
        result: dict[str, Any] | None = None,
        error: str | None = None,
    ) -> BrokerJob:
        status = "completed" if ok else "failed"
        with self._connect() as c:
            row = c.execute("SELECT id FROM jobs WHERE id=?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            c.execute(
                """
                UPDATE jobs
                SET status=?, completed_at=?, result_json=?, error=?
                WHERE id=?
                """,
                (
                    status,
                    time.time(),
                    json.dumps(result) if result is not None else None,
                    error,
                    job_id,
                ),
            )
        return self.get(job_id)

    def get(self, job_id: str) -> BrokerJob:
        with self._connect() as c:
            row = c.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
        if row is None:
            raise KeyError(job_id)
        return self._row(row)

    def _row(self, row) -> BrokerJob:
        return BrokerJob(
            id=row["id"],
            runtime_class=row["runtime_class"],
            capability=row["capability"],
            payload=json.loads(row["payload_json"]),
            status=row["status"],
            created_at=row["created_at"],
            claimed_at=row["claimed_at"],
            completed_at=row["completed_at"],
            result=json.loads(row["result_json"]) if row["result_json"] else None,
            error=row["error"],
        )
