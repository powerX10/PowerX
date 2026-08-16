export class PowerXUnifiedClient{
 constructor(private baseUrl:string,private apiKey:string,private productId:string){}
 async ask(input:Record<string,unknown>){
  const r=await fetch(`${this.baseUrl.replace(/\/$/,"")}/v1/ma`,{method:"POST",headers:{"Content-Type":"application/json",Authorization:`Bearer ${this.apiKey}`},body:JSON.stringify({...input,product_id:this.productId,founder_mode:false})});
  if(!r.ok)throw new Error(`PowerX ${r.status}: ${await r.text()}`);return r.json();
 }
}
