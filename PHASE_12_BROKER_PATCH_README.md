# PowerX Phase 12 Broker Patch

Adds the missing server-side broker required by the Colab GPU16 and mobile
pull workers.

Endpoints:
- POST /workers/jobs
- GET /workers/pull?runtime_class=gpu16|mobile
- POST /workers/result
- GET /workers/jobs/{job_id}

Jobs are stored in SQLite and survive API process restarts.
Worker endpoints honor POWERX_WORKER_TOKEN when it is set.
