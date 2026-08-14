import { NextResponse } from "next/server";
import { generateAuthenticationOptions } from "@simplewebauthn/server";
import { db } from "@/lib/firebase-admin";
import { ownerDoc, rpID } from "@/lib/webauthn";

export async function GET() {
  const snap = await db.collection(`${ownerDoc()}/passkeys`).get();
  if (snap.empty) return NextResponse.json({ error:"NOT_ENROLLED" }, { status:404 });
  const passkeys = snap.docs.map(d => d.data());
  const options = await generateAuthenticationOptions({
    rpID, userVerification:"required",
    allowCredentials:passkeys.map(p => ({ id:p.id, transports:p.transports || [] }))
  });
  await db.doc(`${ownerDoc()}/state/authentication`).set({ challenge:options.challenge, createdAt:Date.now() });
  return NextResponse.json(options);
}
