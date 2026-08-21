"use client";
export default function Error({error,reset}:{error:Error&{digest?:string};reset:()=>void}){return <div className="fixError"><div><h2>PowerX page failed to load</h2><p>{error?.message||"A temporary server error occurred."}</p><button onClick={()=>reset()}>Try again</button></div></div>}
