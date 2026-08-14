import { NextResponse } from "next/server";
import { generateRegistrationOptions } from "@simplewebauthn/server";
import { db } from "@/lib/firebase-admin";
import { hasBootstrap } from "@/lib/session";
import { OWNER_EMAIL, rpID, rpName, ownerDoc } from "@/lib/webauthn";

export async function GET() {
  if (!(await hasBootstrap())) return NextResponse.json({ error:"Unauthorized" }, { status:401 });
  const snap = await db.collection(`${ownerDoc()}/passkeys`).get();
  const passkeys = snap.docs.map(d => d.data());
  const options = await generateRegistrationOptions({
    rpName, rpID, userName: OWNER_EMAIL, attestationType:"none",
    excludeCredentials: passkeys.map(p => ({ id:p.id, transports:p.transports || [] })),
    authenticatorSelection: { residentKey:"required", userVerification:"required", authenticatorAttachment:"platform" },
  });
  await db.doc(`${ownerDoc()}/state/registration`).set({ challenge:options.challenge, createdAt:Date.now() });
  return NextResponse.json(options);
}
