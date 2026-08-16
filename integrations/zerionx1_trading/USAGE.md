# Zerion X1 -> PowerX Trading API

Call `POST /v1/trading/analyze` with live market context prepared by Zerion X1. PowerX does not invent market data; Zerion should pass candles, indicators, fundamentals, news, derivatives and portfolio context when available.

The response contains specialist findings, conflicts, consensus confidence and beginner explanation. Live order placement remains a separate Zerion risk/execution concern.
