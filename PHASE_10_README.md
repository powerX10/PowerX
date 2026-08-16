# PowerX Phase 10 — Trading Intelligence Swarm + Zerion X1 Bridge

Adds a configurable 20-specialist trading analysis layer. Roles are config-driven, not mapped to hardcoded model IDs. Phase 9 Model CMS resolves which model/runtime (CPU/GPU/mobile/cloud) serves each capability.

Specialists cover price action, chart vision, market structure/SMC, support/resistance, indicators, momentum, trend/regime, multi-timeframe, volatility, liquidity/order-flow, fundamentals, financial news, macro, derivatives, forecasting, risk, portfolio/hedging, strategy selection, research/backtesting and independent consensus.

Start:
`uvicorn apps.trading_api.main:app --host 0.0.0.0 --port 8500`

This layer produces probability/confidence-based analysis. It does not guarantee profit and does not bypass Zerion X1's user-confirmation/risk controls.
