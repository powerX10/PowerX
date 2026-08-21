try:
    from uni2ts.model.moirai import MoiraiForecast,MoiraiModule
    print("Moirai API import OK")
except Exception as e:
    print("Moirai API not ready:",e)
    raise SystemExit(2)
