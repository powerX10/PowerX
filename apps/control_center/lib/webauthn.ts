export const OWNER_EMAIL = process.env.POWERX_OWNER_EMAIL || "syedafsharkhadri63@gmail.com";
export const rpID = process.env.POWERX_RP_ID || "localhost";
export const expectedOrigin = process.env.POWERX_ORIGIN || "http://localhost:3000";
export const rpName = "PowerX";
export const ownerDoc = () => `owners/${Buffer.from(OWNER_EMAIL).toString("base64url")}`;
