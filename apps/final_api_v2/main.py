from fastapi import FastAPI
from pydantic import BaseModel,Field
from powerx.v2.router_final import route_request
from powerx.v2.envelope import PowerXRequest
from powerx.v2.zerion.parser import parse_trading_request
from powerx.v2.zerion.risk import evaluate_setup
app=FastAPI(title="PowerX V2 Final API")
class Req(BaseModel):
    product_id:str="powerx";user_id:str|None=None;text:str="";metadata:dict=Field(default_factory=dict)
@app.get("/health")
def health():return {"ok":True,"service":"powerx-v2-final"}
@app.post("/v2/route")
def route(req:Req):
    env=PowerXRequest(req.product_id,req.user_id,req.text,req.metadata);route=route_request(req.product_id,req.text);result={"request":env.to_dict(),"route":route}
    if route=="zerion":
        intent=parse_trading_request(req.text,req.metadata.get("defaults"));result["intent"]=intent.__dict__
        if "setup" in req.metadata:result["evaluation"]=evaluate_setup(intent,req.metadata["setup"])
    return result
