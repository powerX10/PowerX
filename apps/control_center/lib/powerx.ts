export async function control(path:string,init:RequestInit={}){
  const b=process.env.POWERX_CONTROL_API_URL,t=process.env.POWERX_CONTROL_TOKEN;
  if(!b||!t)return{ok:false,error:"PowerX control backend is not configured yet."};
  const r=await fetch(b.replace(/\/$/,"")+path,{
    ...init,
    headers:{...(init.headers||{}),Authorization:`Bearer ${t}`},
    cache:"no-store"
  });
  return r.json();
}

export async function infer(body:unknown){
  const b=process.env.POWERX_PRODUCTION_API_URL;
  const k=process.env.POWERX_PRODUCTION_API_KEY;
  if(!b||!k)return{ok:false,error:"PowerX inference backend is not configured yet."};

  const r=await fetch(b.replace(/\/$/,"")+"/v1/chat",{
    method:"POST",
    headers:{
      "Content-Type":"application/json",
      Authorization:`Bearer ${k}`
    },
    body:JSON.stringify(body),
    cache:"no-store"
  });

  const data=await r.json().catch(()=>({ok:false,error:`PowerX backend returned HTTP ${r.status}`}));
  if(!r.ok && data && typeof data==="object" && !("ok" in data)){
    return {ok:false,error:`PowerX backend returned HTTP ${r.status}`,detail:data};
  }
  return data;
}
