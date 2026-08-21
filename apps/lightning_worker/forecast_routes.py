from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from powerx.v2.adapters.chronos_forecast import ChronosForecastAdapter
from powerx.v2.adapters.timesfm_forecast import TimesFMForecastAdapter
from powerx.v2.adapters.granite_ttm_forecast import GraniteTTMForecastAdapter
from powerx.v2.forecasting import ForecastEnsemble

router=APIRouter(prefix="/v2/forecast",tags=["forecast"])
class Req(BaseModel):
    values:list[float]; horizon:int=12; models:dict[str,str]=Field(default_factory=dict)

@router.post("")
def forecast(req:Req):
    results=[]; errors={}
    adapters={
        "chronos":ChronosForecastAdapter,
        "timesfm":TimesFMForecastAdapter,
        "granite_ttm":GraniteTTMForecastAdapter,
    }
    for name,path in req.models.items():
        cls=adapters.get(name)
        if not cls: continue
        try: results.append(cls(path).run({"values":req.values,"horizon":req.horizon}))
        except Exception as e: errors[name]=str(e)
    return {"consensus":ForecastEnsemble.consensus(results),"results":results,"errors":errors}
