import { hasSession } from "@/lib/session";

export async function requireOwner(){ if (!(await hasSession())) throw new Error("UNAUTHORIZED"); }
export async function control(path:string, init:RequestInit={}){
  await requireOwner();
  const base=process.env.POWERX_CONTROL_API_URL!;
  const token=process.env.POWERX_CONTROL_TOKEN!;
  const r=await fetch(base.replace(/\/$/,"")+path,{...init,headers:{...(init.headers||{}),"Authorization":`Bearer ${token}`},cache:"no-store"});
  if(!r.ok) throw new Error(await r.text()); return r.json();
}
export async function inference(body:unknown){
  await requireOwner();
  const r=await fetch(process.env.POWERX_PRODUCTION_API_URL!.replace(/\/$/,"")+"/v1/inference/chat",{
    method:"POST",headers:{"Content-Type":"application/json","Authorization":`Bearer ${process.env.POWERX_PRODUCTION_API_KEY}`},
    body:JSON.stringify(body),cache:"no-store"
  });
  if(!r.ok) throw new Error(await r.text()); return r.json();
}
