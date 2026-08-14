import { NextRequest, NextResponse } from "next/server";
import { verifyAuthenticationResponse } from "@simplewebauthn/server";
import { db } from "@/lib/firebase-admin";
import { setSession } from "@/lib/session";
import { expectedOrigin, ownerDoc, rpID } from "@/lib/webauthn";

export async function POST(req: NextRequest) {
  const response = await req.json();
  const state = (await db.doc(`${ownerDoc()}/state/authentication`).get()).data();
  const ref = db.doc(`${ownerDoc()}/passkeys/${response.id}`);
  const snap = await ref.get();
  if (!state?.challenge || !snap.exists) return NextResponse.json({ verified:false }, { status:400 });
  const p = snap.data()!;
  const verification = await verifyAuthenticationResponse({
    response, expectedChallenge:state.challenge, expectedOrigin, expectedRPID:rpID,
    credential:{ id:p.id, publicKey:new Uint8Array(Buffer.from(p.publicKey,"base64")), counter:p.counter, transports:p.transports || [] }
  });
  if (!verification.verified) return NextResponse.json({ verified:false }, { status:401 });
  await ref.update({ counter:verification.authenticationInfo.newCounter, lastUsedAt:Date.now() });
  await setSession();
  return NextResponse.json({ verified:true });
}
