import { NextRequest, NextResponse } from "next/server";
import { verifyRegistrationResponse } from "@simplewebauthn/server";
import { db } from "@/lib/firebase-admin";
import { clearBootstrap, hasBootstrap, setSession } from "@/lib/session";
import { expectedOrigin, ownerDoc, rpID } from "@/lib/webauthn";

export async function POST(req: NextRequest) {
  if (!(await hasBootstrap())) return NextResponse.json({ error:"Unauthorized" }, { status:401 });
  const response = await req.json();
  const state = (await db.doc(`${ownerDoc()}/state/registration`).get()).data();
  if (!state?.challenge) return NextResponse.json({ error:"Registration challenge missing" }, { status:400 });
  const verification = await verifyRegistrationResponse({
    response, expectedChallenge:state.challenge, expectedOrigin, expectedRPID:rpID,
  });
  if (!verification.verified || !verification.registrationInfo)
    return NextResponse.json({ verified:false }, { status:400 });
  const info = verification.registrationInfo;
  const c = info.credential;
  await db.doc(`${ownerDoc()}/passkeys/${c.id}`).set({
    id:c.id,
    publicKey:Buffer.from(c.publicKey).toString("base64"),
    counter:c.counter,
    transports:c.transports || [],
    deviceType:info.credentialDeviceType,
    backedUp:info.credentialBackedUp,
    createdAt:Date.now()
  });
  await setSession(); await clearBootstrap();
  return NextResponse.json({ verified:true });
}
