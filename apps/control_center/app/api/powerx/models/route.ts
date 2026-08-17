import{NextResponse}from"next/server";import{hasSession}from"@/lib/session";import{models}from"@/lib/powerx-model-catalog";
export async function GET(){if(!(await hasSession()))return NextResponse.json({error:"Unauthorized"},{status:401});return NextResponse.json({ok:true,models:await models()})}
