# PowerX Phase 12 Chat + Mobile Runtime Completion

This patch completes the two missing runtime pieces:

1. **PowerX Chat backend wiring**
   - Control Center now calls `/v1/chat`.
   - A Modal-deployable PowerX Production Gateway forwards chat to the already-live
     Modal CPU worker (`qwen25-3b-general` by default).
   - The old `/v1/inference/chat` path remains supported for compatibility.

2. **Actual phone inference runtime**
   - Termux bootstrap builds only `llama-cli` (not `llama-server`) to avoid the
     current Android/Termux server build issues.
   - Qwen2.5-0.5B-Instruct Q4_K_M (~491 MB) is automatically downloaded and cached.
   - A local stdlib HTTP server exposes `127.0.0.1:8080/infer`.
   - The mobile broker worker pulls only mobile-class jobs and returns local results.
   - Users never manually download model weights.

The mobile implementation is CPU-local by default because Android GPU backends are
device/vendor dependent. PowerX still routes small tasks to the phone; unsupported
or unsuitable tasks should fall back to CPU cloud nodes.

## Install / verify

```bash
cd ~/PowerX
unzip -o /storage/emulated/0/Download/PowerX_Phase_12_Chat_Mobile_Completion.zip

python -m compileall -q   powerx/runtime_fabric   apps/powerx_production_api   deploy_phase12/mobile_edge

python -m unittest discover -s tests_phase12_completion -v
```

## Production gateway

```bash
bash scripts_phase12/configure_production_gateway.sh
modal deploy deploy_phase12/production_gateway_modal/app.py
```

Take the returned `https://...modal.run` URL, then:

```bash
bash scripts_phase12/set_control_center_backend.sh 'https://YOUR-GATEWAY.modal.run'
cd ~/PowerX/apps/control_center
npm run typecheck
npm run build
```

## Mobile runtime

```bash
cd ~/PowerX
bash scripts_phase12/start_mobile_runtime.sh
```

The first run automatically builds llama.cpp CLI and downloads/caches the tiny model.
Later starts reuse the cached binary and model.
