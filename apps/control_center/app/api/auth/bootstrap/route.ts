import { NextRequest, NextResponse } from "next/server";
import { getAdminAuth } from "@/lib/firebase-admin";
import { createSession } from "@/lib/session";

const OWNER_EMAIL =
  (process.env.POWERX_OWNER_EMAIL ||
    "syedafsharkhadri63@gmail.com").toLowerCase();

export async function POST(req: NextRequest) {
  try {
    const { idToken } = await req.json();

    if (!idToken) {
      return NextResponse.json(
        { error: "Missing ID token" },
        { status: 400 }
      );
    }

    const decoded = await getAdminAuth().verifyIdToken(idToken, true);

    if (
      !decoded.email ||
      decoded.email.toLowerCase() !== OWNER_EMAIL
    ) {
      return NextResponse.json(
        { error: "Unauthorized PowerX account" },
        { status: 403 }
      );
    }

    await createSession();

    return NextResponse.json({
      ok: true,
      email: decoded.email,
    });
  } catch (error) {
    return NextResponse.json(
      { error: String(error) },
      { status: 401 }
    );
  }
}
