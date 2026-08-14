# PowerX Phase 5 — Control Center

Additive only. Extract after Phases 1–4.

## Owner login
The only allowed account is:

`syedafsharkhadri63@gmail.com`

First login:
1. Send Firebase passwordless email link.
2. Verify the email link.
3. Enroll a platform WebAuthn passkey.
4. The browser/OS prompts for fingerprint, face, PIN, or another platform authenticator.

Later logins:
- Press **Unlock PowerX**
- WebAuthn/passkey prompt appears
- No email/password form is required

Fingerprint templates never reach PowerX or Firebase. WebAuthn stores/verifies public-key credentials.

## Firebase use
Firebase is used only for:
- passwordless first-owner verification
- server-side Firestore persistence of WebAuthn public credentials/challenges

PowerX AI inference, GPU/CPU/mobile runtimes, model files, and trading logic do not depend on Firebase.

## Apps
- `apps/control_center` — Next.js control-center UI
- `apps/control_api` — secured runtime/model-control API

## Setup
See:
- `docs_phase5/SETUP_FIREBASE.md`
- `docs_phase5/DEPLOYMENT.md`
