import { NextResponse } from "next/server";
import { control } from "@/lib/powerx-server";
export async function GET(){ try{return NextResponse.json(await control("/settings"));}catch(e){return NextResponse.json({error:String(e)},{status:500});} }
