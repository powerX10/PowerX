# PowerX Phase 8 — Google Drive Warehouse + Runtime Fabric

Google Drive is the permanent PowerX model warehouse:
`MyDrive/PowerX/Models/`

Flow:
Google Drive master model -> runtime-local temporary cache -> CPU/RAM or GPU/VRAM -> output.

Runtime policy:
- Continuous/light jobs: CPU first.
- Device-local jobs: capable mobile first.
- Heavy/deep/image/video jobs: Google Colab 16 GB GPU first.
- Cloud/Modal/Beam stay optional.

Mobile model policy starts at 3B:
- 6 GB RAM + 4 GB free cache => 3B
- 10 GB RAM + 6 GB free cache => 4B
- 16 GB RAM + 8 GB free cache => 6B
- below that => route to CPU/GPU instead of forcing a model.

Important: CPU/mobile/GPU form one orchestration fabric; their RAM/VRAM is not added
together for a single model automatically.

Colab warehouse setup after merge:
1. Mount Google Drive.
2. `python scripts_phase8/warehouse_init.py`
3. `python runtime_nodes/colab/seed_warehouse.py`

This seeds model files directly from Hugging Face into Google Drive in the Colab session;
the phone does not receive the warehouse files.

Default source models:
- Qwen/Qwen2.5-3B-Instruct
- Qwen/Qwen3-4B
- 01-ai/Yi-1.5-6B-Chat

For CPU/mobile llama.cpp, add quantized GGUF variants to the same warehouse manifest.
The Phase 8 code supports staging them from Drive into each runtime's temporary cache.

Start fabric API:
`uvicorn apps.fabric_api.main:app --host 0.0.0.0 --port 8300`
