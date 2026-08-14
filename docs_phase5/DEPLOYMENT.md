# Phase 5 deployment

## Control API
From the merged PowerX root:
```bash
pip install -r requirements-phase5-control-api.txt
export POWERX_CONTROL_TOKEN='<random secret>'
uvicorn apps.control_api.main:app --host 127.0.0.1 --port 8400
```

## Control Center
```bash
cd apps/control_center
npm install
npm run build
npm start
```

Set all values from `.env.example`.

## Security
- Do not expose the control API directly to the public internet.
- Browser talks to Next.js route handlers.
- Next.js server talks to PowerX using server-only secrets.
- Firestore client rules deny all passkey access.
- WebAuthn requires HTTPS in production.
