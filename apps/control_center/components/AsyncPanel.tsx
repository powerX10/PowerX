"use client";
import {useEffect,useState} from "react";
export function AsyncPanel({url,children}:{url:string,children:(d:any)=>React.ReactNode}){const[d,setD]=useState<any>();const[e,setE]=useState("");useEffect(()=>{fetch(url).then(r=>r.json()).then(setD).catch(x=>setE(String(x)))},[url]);if(e)return <div className="error">{e}</div>;if(!d)return <div className="skeleton"/>;return <>{children(d)}</>}
