import { NextRequest, NextResponse } from "next/server";
import { control } from "@/lib/powerx-server";
export async function POST(req:NextRequest){
  try { const body=await req.json(); return NextResponse.json(await control("/runtime/action",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)})); }
  catch(e){ return NextResponse.json({error:String(e)},{status:500}); }
}
