"""PowerX Modal CPU worker — real inference implementation.

Supports the CPU-first adapters needed for general chat/reasoning, financial
classification, embeddings/reranking, Whisper STT, and Chronos forecasting.
Models are staged on demand from the PowerX Google Drive warehouse into a
persistent Modal Volume cache.

Specialized adapters not implemented in this worker return HTTP 422 so the
PowerX runtime fabric can fail over to another configured provider.
"""
import base64
import os
import pathlib
from typing import Any

import modal

app = modal.App("powerx-modal-cpu")
volume = modal.Volume.from_name("powerx-model-cache", create_if_missing=True)

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install(
        "rclone",
        "build-essential",
        "cmake",
        "git",
        "pkg-config",
        "libopenblas-dev",
        "libsndfile1",
    )
    # CPU worker: install the CPU-only PyTorch wheel explicitly.  Installing
    # bare `torch` from the default Linux index may pull hundreds of MB of CUDA
    # libraries even though this container has no GPU.
    .pip_install(
        "torch==2.9.1",
        index_url="https://download.pytorch.org/whl/cpu",
        extra_options="--resume-retries 20 --timeout 180",
    )
    .pip_install(
        "fastapi",
        "uvicorn",
        "httpx",
        "numpy",
        "transformers",
        "sentence-transformers",
        "chronos-forecasting",
        "soundfile",
        extra_options="--resume-retries 20 --timeout 180",
    )
    .run_commands(
        "CMAKE_ARGS='-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS' "
        "pip install --no-cache-dir llama-cpp-python"
    )
    .add_local_python_source("powerx")
    .add_local_dir("config_phase12", remote_path="/root/config_phase12")
    .add_local_file("data/model_cms.json", remote_path="/root/data/model_cms.json")
)

secret = modal.Secret.from_name("powerx-drive")


@app.function(
    image=image,
    cpu=4.0,
    memory=16384,
    timeout=3600,
    volumes={"/cache": volume},
    secrets=[secret],
    min_containers=0,
    max_containers=4,
)
@modal.asgi_app()
def api():
    import numpy as np
    import torch
    from fastapi import FastAPI, HTTPException, Request

    from powerx.controlplane.store import ControlPlaneStore
    from powerx.final_runtime.warehouse import RcloneWarehouse

    conf = os.getenv("RCLONE_CONFIG_B64", "")
    if conf:
        p = pathlib.Path.home() / ".config/rclone/rclone.conf"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(base64.b64decode(conf))

    os.environ["POWERX_RUNTIME_CACHE"] = "/cache/cpu"
    os.environ.setdefault("POWERX_MODEL_CMS_DB", "/root/data/model_cms.json")

    store = ControlPlaneStore()
    warehouse = RcloneWarehouse()
    loaded: dict[str, tuple[str, Any]] = {}

    web = FastAPI(title="PowerX Modal CPU Worker")

    def auth(req: Request):
        token = os.getenv("POWERX_WORKER_TOKEN")
        if token and req.headers.get("authorization") != f"Bearer {token}":
            raise HTTPException(401, "unauthorized")

    def model_entry(model_id: str):
        try:
            model = store.get(model_id)
        except KeyError:
            raise HTTPException(404, f"unknown model_id: {model_id}")
        if not model.enabled:
            raise HTTPException(409, f"model disabled: {model_id}")
        if not model.warehouse_path:
            raise HTTPException(422, f"warehouse_path missing: {model_id}")
        return model

    def stage(model):
        return warehouse.stage(
            model.warehouse_path,
            "/cache/cpu",
            model.id,
        )

    def load(model):
        if model.id in loaded:
            return loaded[model.id]

        adapter = str((model.config or {}).get("adapter") or "")
        local = stage(model)

        if adapter in {"llamacpp", "llamacpp_vision"}:
            if adapter == "llamacpp_vision":
                raise HTTPException(
                    422,
                    "vision GGUF is routed to gpu16/vision worker; CPU Modal worker does not load mmproj",
                )
            from llama_cpp import Llama

            cfg = (model.config or {}).get("cpu", {})
            obj = Llama(
                model_path=str(local),
                n_ctx=int(cfg.get("context_size", 8192)),
                n_threads=int(cfg.get("threads", 4)),
                n_gpu_layers=0,
                verbose=False,
            )

        elif adapter == "transformers_text_classification":
            from transformers import AutoModelForSequenceClassification, AutoTokenizer

            tok = AutoTokenizer.from_pretrained(str(local), local_files_only=True)
            mdl = AutoModelForSequenceClassification.from_pretrained(
                str(local),
                local_files_only=True,
            )
            mdl.eval()
            obj = (tok, mdl)

        elif adapter == "transformers_text_generation":
            from transformers import AutoModelForCausalLM, AutoTokenizer

            tok = AutoTokenizer.from_pretrained(
                str(local),
                local_files_only=True,
                trust_remote_code=True,
            )
            mdl = AutoModelForCausalLM.from_pretrained(
                str(local),
                local_files_only=True,
                trust_remote_code=True,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True,
            )
            mdl.eval()
            obj = (tok, mdl)

        elif adapter == "sentence_transformers":
            from sentence_transformers import SentenceTransformer

            obj = SentenceTransformer(str(local), device="cpu")

        elif adapter == "transformers_reranker":
            from transformers import AutoModelForSequenceClassification, AutoTokenizer

            tok = AutoTokenizer.from_pretrained(str(local), local_files_only=True)
            mdl = AutoModelForSequenceClassification.from_pretrained(
                str(local),
                local_files_only=True,
            )
            mdl.eval()
            obj = (tok, mdl)

        elif adapter == "chronos":
            from chronos import BaseChronosPipeline

            obj = BaseChronosPipeline.from_pretrained(
                str(local),
                device_map="cpu",
            )

        elif adapter in {"whisper", "transformers_asr"}:
            from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor

            proc = AutoProcessor.from_pretrained(str(local), local_files_only=True)
            mdl = AutoModelForSpeechSeq2Seq.from_pretrained(
                str(local),
                local_files_only=True,
                torch_dtype=torch.float32,
            )
            mdl.eval()
            obj = (proc, mdl)

        else:
            raise HTTPException(
                422,
                f"adapter '{adapter}' is not implemented on modal-cpu-primary",
            )

        loaded[model.id] = (adapter, obj)
        volume.commit()
        return loaded[model.id]

    def infer_loaded(model, payload: dict):
        adapter, obj = load(model)

        if adapter == "llamacpp":
            llm = obj
            messages = payload.get("messages")
            if messages:
                out = llm.create_chat_completion(
                    messages=messages,
                    max_tokens=int(payload.get("max_tokens", 512)),
                    temperature=float(payload.get("temperature", 0.2)),
                )
                return out

            prompt = str(payload.get("prompt") or payload.get("text") or "")
            if not prompt:
                raise HTTPException(422, "prompt/text/messages required")
            return llm(
                prompt,
                max_tokens=int(payload.get("max_tokens", 512)),
                temperature=float(payload.get("temperature", 0.2)),
            )

        if adapter == "transformers_text_classification":
            tok, mdl = obj
            text = str(payload.get("text") or "")
            if not text:
                raise HTTPException(422, "text required")
            inputs = tok(text, return_tensors="pt", truncation=True, max_length=512)
            with torch.inference_mode():
                logits = mdl(**inputs).logits[0]
                probs = torch.softmax(logits, dim=-1)
            labels = getattr(mdl.config, "id2label", {}) or {}
            return {
                "scores": [
                    {
                        "label": str(labels.get(i, i)),
                        "score": float(probs[i]),
                    }
                    for i in range(len(probs))
                ]
            }

        if adapter == "transformers_text_generation":
            tok, mdl = obj
            messages = payload.get("messages")
            if messages and hasattr(tok, "apply_chat_template"):
                prompt = tok.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True,
                )
            else:
                prompt = str(payload.get("prompt") or payload.get("text") or "")
            if not prompt:
                raise HTTPException(422, "prompt/text/messages required")

            inputs = tok(prompt, return_tensors="pt")
            with torch.inference_mode():
                generated = mdl.generate(
                    **inputs,
                    max_new_tokens=int(payload.get("max_tokens", 256)),
                    do_sample=float(payload.get("temperature", 0.0)) > 0,
                    temperature=max(float(payload.get("temperature", 0.2)), 1e-5),
                )
            new_tokens = generated[0][inputs["input_ids"].shape[1] :]
            return {"text": tok.decode(new_tokens, skip_special_tokens=True)}

        if adapter == "sentence_transformers":
            texts = payload.get("texts")
            if texts is None:
                one = payload.get("text")
                texts = [one] if one is not None else None
            if not texts:
                raise HTTPException(422, "text or texts required")
            vectors = obj.encode(
                list(map(str, texts)),
                normalize_embeddings=bool(payload.get("normalize", True)),
            )
            return {"embeddings": np.asarray(vectors).tolist()}

        if adapter == "transformers_reranker":
            tok, mdl = obj
            query = str(payload.get("query") or "")
            docs = payload.get("documents") or []
            if not query or not docs:
                raise HTTPException(422, "query and documents required")
            pairs = [[query, str(d)] for d in docs]
            inputs = tok(
                pairs,
                padding=True,
                truncation=True,
                return_tensors="pt",
                max_length=512,
            )
            with torch.inference_mode():
                logits = mdl(**inputs).logits
            if logits.shape[-1] == 1:
                scores = logits[:, 0].float().tolist()
            else:
                scores = torch.softmax(logits, dim=-1)[:, -1].float().tolist()
            ranked = sorted(
                [
                    {"index": i, "document": docs[i], "score": float(scores[i])}
                    for i in range(len(docs))
                ],
                key=lambda x: x["score"],
                reverse=True,
            )
            return {"ranked": ranked}

        if adapter == "chronos":
            series = payload.get("series")
            horizon = int(payload.get("horizon", 12))
            if not isinstance(series, list) or not series:
                raise HTTPException(422, "series must be a non-empty numeric list")
            context = torch.tensor(series, dtype=torch.float32)
            forecast = obj.predict(context, prediction_length=horizon)
            arr = forecast.detach().cpu().numpy()
            return {
                "samples": arr.tolist(),
                "median": np.median(arr, axis=-1).tolist(),
            }

        if adapter in {"whisper", "transformers_asr"}:
            proc, mdl = obj
            audio = payload.get("audio")
            sampling_rate = int(payload.get("sampling_rate", 16000))
            if not isinstance(audio, list) or not audio:
                raise HTTPException(
                    422,
                    "audio must be a non-empty list of float PCM samples",
                )
            features = proc(
                np.asarray(audio, dtype=np.float32),
                sampling_rate=sampling_rate,
                return_tensors="pt",
            )
            with torch.inference_mode():
                ids = mdl.generate(**features)
            return {"text": proc.batch_decode(ids, skip_special_tokens=True)[0]}

        raise HTTPException(422, f"unsupported adapter: {adapter}")

    @web.get("/health")
    def health():
        return {
            "ok": True,
            "provider": "modal",
            "runtime_class": "cpu",
            "real_inference": True,
            "loaded_models": list(loaded.keys()),
        }

    @web.post("/infer")
    async def infer(req: Request):
        auth(req)
        body = await req.json()
        model_id = str(body.get("model_id") or "")
        if not model_id:
            raise HTTPException(422, "model_id required")
        model = model_entry(model_id)
        result = infer_loaded(model, body.get("payload") or {})
        return {
            "ok": True,
            "provider": "modal",
            "runtime_class": "cpu",
            "model_id": model_id,
            "capability": body.get("capability"),
            "result": result,
        }

    return web
