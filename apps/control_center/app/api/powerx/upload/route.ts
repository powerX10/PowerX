import { NextRequest, NextResponse } from "next/server";
import { requireOwner } from "@/lib/powerx-server";
export async function POST(req:NextRequest){
  try{
    await requireOwner();
    const fd=await req.formData(); const file=fd.get("file");
    if(!(file instanceof File)) return NextResponse.json({error:"File required"},{status:400});
    if(file.size>25*1024*1024) return NextResponse.json({error:"25MB limit"},{status:413});
    const upstream=new FormData(); upstream.set("file",file);
    const r=await fetch(process.env.POWERX_CONTROL_API_URL!.replace(/\/$/,"")+"/files",{method:"POST",headers:{"Authorization":`Bearer ${process.env.POWERX_CONTROL_TOKEN}`},body:upstream});
    return NextResponse.json(await r.json(),{status:r.status});
  }catch(e){return NextResponse.json({error:String(e)},{status:500});}
}
