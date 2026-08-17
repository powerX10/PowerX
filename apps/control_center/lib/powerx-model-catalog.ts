import { getAdminDb } from "@/lib/firebase-admin";
export type RC="mobile"|"cpu"|"gpu16";
export type M={id:string;name:string;capabilities:string[];runtimeOrder:RC[];enabled:boolean;sourceRepo?:string;file?:string};
const B:M[]=[
{id:"qwen25-3b-general",name:"Qwen2.5 3B General",capabilities:["chat"],runtimeOrder:["mobile","cpu","gpu16"],enabled:true,sourceRepo:"Qwen/Qwen2.5-3B-Instruct-GGUF",file:"qwen2.5-3b-instruct-q4_k_m.gguf"},
{id:"qwen3-4b-reasoning",name:"Qwen3 4B Reasoning",capabilities:["chat","deep_reasoning","chart_analysis"],runtimeOrder:["mobile","cpu","gpu16"],enabled:true,sourceRepo:"Qwen/Qwen3-4B-GGUF",file:"Qwen3-4B-Q4_K_M.gguf"},
{id:"qwen25-coder-3b",name:"Qwen2.5 Coder 3B",capabilities:["coding"],runtimeOrder:["mobile","cpu","gpu16"],enabled:true,sourceRepo:"Qwen/Qwen2.5-Coder-3B-Instruct-GGUF",file:"qwen2.5-coder-3b-instruct-q4_k_m.gguf"},
{id:"qwen25-vl-3b-chart",name:"Qwen2.5 VL 3B",capabilities:["vision","chart_analysis"],runtimeOrder:["cpu","gpu16"],enabled:true},
{id:"phi4-mini-deep",name:"Phi-4 Mini Deep",capabilities:["deep_reasoning"],runtimeOrder:["cpu","gpu16"],enabled:true},
{id:"finbert-sentiment",name:"FinBERT Sentiment",capabilities:["financial_sentiment"],runtimeOrder:["cpu"],enabled:true},
{id:"finbert-tone",name:"FinBERT Tone",capabilities:["financial_sentiment"],runtimeOrder:["cpu"],enabled:true},
{id:"financial-news-distilroberta",name:"Financial News DistilRoBERTa",capabilities:["financial_sentiment"],runtimeOrder:["cpu"],enabled:true},
{id:"financialbert-sentiment",name:"FinancialBERT Sentiment",capabilities:["financial_sentiment"],runtimeOrder:["cpu"],enabled:true},
{id:"chronos-small",name:"Chronos Small",capabilities:["forecasting"],runtimeOrder:["cpu","gpu16"],enabled:true},
{id:"timesfm-200m",name:"TimesFM 200M",capabilities:["forecasting"],runtimeOrder:["cpu"],enabled:true},
{id:"moirai-small",name:"Moirai Small",capabilities:["forecasting"],runtimeOrder:["cpu"],enabled:true},
{id:"granite-ttm",name:"Granite TTM",capabilities:["forecasting"],runtimeOrder:["cpu"],enabled:true},
{id:"granite-tspulse",name:"Granite TSPulse",capabilities:["anomaly_detection"],runtimeOrder:["cpu"],enabled:true},
{id:"bge-reranker-base",name:"BGE Reranker",capabilities:["rerank"],runtimeOrder:["cpu"],enabled:true},
{id:"minilm-embedding",name:"MiniLM Embedding",capabilities:["embedding"],runtimeOrder:["cpu"],enabled:true},
{id:"whisper-small",name:"Whisper Small",capabilities:["speech_to_text"],runtimeOrder:["cpu","gpu16"],enabled:true},
{id:"kokoro-tts",name:"Kokoro TTS",capabilities:["text_to_speech"],runtimeOrder:["cpu","gpu16"],enabled:true},
{id:"sdxl-base",name:"SDXL Base",capabilities:["image_generate","image_edit"],runtimeOrder:["gpu16","cpu"],enabled:true},
{id:"wan21-1.3b",name:"Wan 2.1 1.3B",capabilities:["video_generate"],runtimeOrder:["gpu16","cpu"],enabled:true}
];
export async function models(){const s=await getAdminDb().collection("powerx_model_overrides").get();const o=new Map(s.docs.map(d=>[d.id,d.data() as any]));return B.map(m=>{const x=o.get(m.id)||{};return{...m,name:x.displayName||m.name,enabled:x.enabled??m.enabled,runtimeOrder:x.runtime&&x.runtime!=="auto"?[x.runtime,...m.runtimeOrder.filter(r=>r!==x.runtime)]:m.runtimeOrder}})}
export function capability(text:string,a:any[]=[]){const t=(text||"").toLowerCase();if(a.some(x=>String(x.mime_type||"").startsWith("audio/")))return"speech_to_text";if(a.some(x=>String(x.mime_type||"").startsWith("image/")))return"vision";if(/(generate|create|banao).*(image|photo|picture)/i.test(t))return"image_generate";if(/(generate|create|banao).*video/i.test(t))return"video_generate";if(/\b(code|python|typescript|javascript|github)\b/i.test(t))return"coding";if(/\b(chart|candlestick|price action)\b/i.test(t))return"chart_analysis";if(/\b(forecast|time series)\b/i.test(t))return"forecasting";if(/\b(sentiment|news tone)\b/i.test(t))return"financial_sentiment";if(/\b(tts|read aloud|voice reply)\b/i.test(t))return"text_to_speech";if(/\b(deep analysis|strategy|portfolio|macro|risk)\b/i.test(t))return"deep_reasoning";return"chat"}
