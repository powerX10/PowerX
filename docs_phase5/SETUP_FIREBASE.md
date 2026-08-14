# Firebase setup

1. Create/use one Firebase project.
2. Authentication -> Sign-in method:
   - Enable Email/Password
   - Enable Email link (passwordless)
3. Add the production domain to Authorized domains.
4. Create a Firestore database.
5. Deploy `firebase_phase5/firestore.rules` (client access is denied; Admin SDK owns passkey records).
6. Add the Firebase Web config to `apps/control_center/.env.local`.
7. Add Firebase Admin service-account environment values.
8. Set:
   `POWERX_OWNER_EMAIL=syedafsharkhadri63@gmail.com`
9. Generate `POWERX_SESSION_SECRET` with at least 32 random characters.
10. Production must use HTTPS and `POWERX_RP_ID` must match the real domain.

The first passwordless email link verifies ownership of the fixed email. After that,
WebAuthn passkey registration is required. Future login is passkey-only in the UI.
