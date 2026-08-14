# Final Zerion X1 -> PowerX contract

Zerion X1 owns:
- market data
- indicators
- strategy logic
- backtesting
- risk calculations
- order execution
- broker connectivity

PowerX owns:
- model selection
- model/runtime availability
- AI inference
- fallback
- streaming
- attachment routing
- usage metrics

Primary endpoint:
`POST /v2/inference`

Example body:
```json
{
  "task": "deep_reasoning",
  "messages": [
    {"role":"system","content":"Use only the supplied Zerion context."},
    {"role":"user","content":"<structured Zerion context>"}
  ],
  "max_tokens": 1200,
  "stream": false
}
```
