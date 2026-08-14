import crypto from "node:crypto";
import { cookies } from "next/headers";

const SESSION = "powerx_session";
const BOOT = "powerx_bootstrap";

function secret() {
  const s = process.env.POWERX_SESSION_SECRET;
  if (!s || s.length < 32) throw new Error("POWERX_SESSION_SECRET must be at least 32 characters");
  return s;
}
function sign(value: string) {
  return crypto.createHmac("sha256", secret()).update(value).digest("base64url");
}
function token(kind: string, ttl: number) {
  const payload = `${kind}.${Date.now() + ttl}`;
  return `${payload}.${sign(payload)}`;
}
function verify(value: string | undefined, kind: string) {
  if (!value) return false;
  const [k, exp, sig] = value.split(".");
  if (k !== kind || !exp || !sig) return false;
  const payload = `${k}.${exp}`;
  if (!crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(sign(payload)))) return false;
  return Number(exp) > Date.now();
}
export async function setBootstrap() {
  (await cookies()).set(BOOT, token("bootstrap", 10 * 60_000), { httpOnly:true, secure:process.env.NODE_ENV==="production", sameSite:"strict", path:"/", maxAge:600 });
}
export async function setSession() {
  (await cookies()).set(SESSION, token("owner", 12 * 60 * 60_000), { httpOnly:true, secure:process.env.NODE_ENV==="production", sameSite:"strict", path:"/", maxAge:43200 });
}
export async function hasBootstrap() { return verify((await cookies()).get(BOOT)?.value, "bootstrap"); }
export async function hasSession() { return verify((await cookies()).get(SESSION)?.value, "owner"); }
export async function clearBootstrap() { (await cookies()).delete(BOOT); }
export async function clearSession() { (await cookies()).delete(SESSION); }
