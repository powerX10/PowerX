from pathlib import Path
p=Path("apps/control_center/lib/firebase-admin.ts");s=p.read_text()
if "export function getAdminApp" not in s:
 s += """
export function getAdminApp() {
  const { getApps, initializeApp, cert } = require("firebase-admin/app");
  if (getApps().length) return getApps()[0];
  const key=(process.env.FIREBASE_PRIVATE_KEY||"").replace(/\\\\n/g,"\\n");
  return initializeApp({credential:cert({projectId:process.env.FIREBASE_PROJECT_ID,clientEmail:process.env.FIREBASE_CLIENT_EMAIL,privateKey:key})});
}
"""
p.write_text(s);print("firebase-admin export ready")
