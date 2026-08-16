# PowerX Phase 12 Modal Broker Deploy

Deploys the Runtime Fabric API and durable SQLite worker broker to Modal.

The broker uses the existing `powerx-drive` Modal secret for
`POWERX_WORKER_TOKEN` and stores its SQLite DB on a persistent Modal Volume.

Deploy:
`modal deploy deploy_phase12/broker_modal/app.py`
