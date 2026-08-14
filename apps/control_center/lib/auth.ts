export const OWNER_EMAIL=(process.env.POWERX_OWNER_EMAIL||"syedafsharkhadri63@gmail.com").toLowerCase();
export const rpID=process.env.POWERX_RP_ID||"localhost";export const origin=process.env.POWERX_ORIGIN||"http://localhost:3000";export const ownerKey=Buffer.from(OWNER_EMAIL).toString("base64url");
