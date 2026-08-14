import { NextRequest, NextResponse } from "next/server";
import { adminAuth } from "@/lib/firebase-admin";
import { OWNER_EMAIL } from "@/lib/webauthn";
import { setBootstrap } from "@/lib/session";

export async function POST(req: NextRequest) {
  const { idToken } = await req.json();
  const decoded = await adminAuth.verifyIdToken(idToken, true);
  if (!decoded.email_verified || decoded.email?.toLowerCase() !== OWNER_EMAIL.toLowerCase()) {
    return NextResponse.json({ error: "Owner verification failed" }, { status: 403 });
  }
  await setBootstrap();
  return NextResponse.json({ ok: true });
}
