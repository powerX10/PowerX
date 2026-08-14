import { NextRequest, NextResponse } from "next/server";
import { inference } from "@/lib/powerx-server";
export async function POST(req:NextRequest){
  try{return NextResponse.json(await inference(await req.json()));}
  catch(e){return NextResponse.json({error:String(e)},{status:500});}
}
