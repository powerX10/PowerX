from __future__ import annotations
import statistics

class ForecastEnsemble:
    @staticmethod
    def consensus(results: list[dict]) -> dict:
        valid=[r for r in results if isinstance(r,dict) and isinstance(r.get("forecast"),list) and r["forecast"]]
        if not valid: return {"ok":False,"forecast":[],"models":[]}
        n=min(len(r["forecast"]) for r in valid)
        rows=[]
        for i in range(n):
            vals=[float(r["forecast"][i]) for r in valid]
            rows.append(statistics.median(vals))
        return {"ok":True,"forecast":rows,"models":[r.get("model","unknown") for r in valid],"method":"median"}
