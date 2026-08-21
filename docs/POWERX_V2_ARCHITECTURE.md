# PowerX V2 Architecture

## Non-negotiable design

- Google Drive/rclone is a warehouse, not the inference disk.
- Lightning AI is the first runtime provider, not the permanent platform lock-in.
- PowerX API stays provider-independent.
- MA is an orchestrator, not a single model.
- Long videos are generated as checkpointed chapters/clips and then composed into one MP4.

## Runtime flow

User request -> PowerX API -> MA/Router -> Model registry -> Cache manager -> Lightning worker -> result/artifact.

## Zip plan

1. Zip 1: registry, cache, runtime broker, API, smoke tests.
2. Zip 2: real model adapters for GGUF/Transformers/STT/TTS.
3. Zip 3: video director pipeline, chunked MP4 generation, FFmpeg composer.
4. Zip 4: Zerion trading agent + Bilux tutor agent + tool permissions.
