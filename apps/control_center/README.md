# PowerX Control Center — Vercel Ready

Deploy this folder as a standalone Next.js project.

Vercel:
- Framework: Next.js
- Root Directory: this folder
- Output Directory: default / override OFF
- Build Command: default
- Install Command: default

Required for frontend build/login:
NEXT_PUBLIC_FIREBASE_API_KEY
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN
NEXT_PUBLIC_FIREBASE_PROJECT_ID
NEXT_PUBLIC_FIREBASE_APP_ID

Required for owner login/passkey:
FIREBASE_PROJECT_ID
FIREBASE_CLIENT_EMAIL
FIREBASE_PRIVATE_KEY
POWERX_OWNER_EMAIL
POWERX_SESSION_SECRET
POWERX_RP_ID
POWERX_ORIGIN

Required later for actual PowerX backends:
POWERX_PRODUCTION_API_URL
POWERX_PRODUCTION_API_KEY
POWERX_CONTROL_API_URL
POWERX_CONTROL_TOKEN
