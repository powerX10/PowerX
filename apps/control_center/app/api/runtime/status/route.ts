import{NextResponse}from"next/server";import{hasSession}from"@/lib/session";import{snapshot}from"@/lib/runtime-broker";
export async function GET(){if(!(await hasSession()))return NextResponse.json({error:"Unauthorized"},{status:401});return NextResponse.json({ok:true,...await snapshot()})}
