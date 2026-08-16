import{NextRequest,NextResponse}from"next/server";
import{hasSession}from"@/lib/session";
import{infer}from"@/lib/powerx";
export async function POST(req:NextRequest){
 if(!(await hasSession()))return NextResponse.json({error:"Unauthorized"},{status:401});
 const body=await req.json();
 return NextResponse.json(await infer({...body,product_id:"powerx",founder_mode:true}));
}
