import crypto from "node:crypto";import{cookies}from"next/headers";const C="powerx_session";
function sec(){const s=process.env.POWERX_SESSION_SECRET;if(!s||s.length<32)throw new Error("POWERX_SESSION_SECRET missing");return s}
function sign(v:string){return crypto.createHmac("sha256",sec()).update(v).digest("base64url")}
export async function createSession(){const e=Date.now()+43200000,b=`owner.${e}`,v=`${b}.${sign(b)}`;(await cookies()).set(C,v,{httpOnly:true,secure:process.env.NODE_ENV==="production",sameSite:"strict",path:"/",maxAge:43200})}
export async function hasSession(){const v=(await cookies()).get(C)?.value;if(!v)return false;const[k,e,s]=v.split(".");if(k!=="owner"||!e||!s)return false;return sign(`${k}.${e}`)===s&&Number(e)>Date.now()}
export async function clearSession(){(await cookies()).delete(C)}
