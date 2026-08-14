# PowerX Phase 4 — Production Orchestration

Final additive phase. Extract after Phases 1, 2 and 3.

PowerX remains an AI-model orchestration service. Zerion X1 owns all trading logic.

This phase adds:
- runtime endpoint registry
- GPU -> CPU -> mobile fallback
- model/task endpoint resolution
- health-aware selection
- unified inference coordinator
- API-key authentication helpers
- in-memory rate limiter
- request IDs
- JSON audit logs
- production preflight
- Zerion X1 Python client
- Docker/systemd examples

No fake inference is implemented. If no healthy compatible model runtime exists,
the coordinator returns a clear unavailable error rather than fabricated output.
