from .schema import ModelSpec

DEFAULT_MODELS = [
    ModelSpec("qwen2.5-3b-instruct","3b","transformers",
              ("chat","research","code","file_analyze"),
              "Qwen/Qwen2.5-3B-Instruct", min_ram_gb=6.0,
              notes="Minimum PowerX mobile tier."),
    ModelSpec("qwen3-4b","4b","transformers",
              ("chat","reasoning","code","research"),
              "Qwen/Qwen3-4B", min_ram_gb=8.0,
              notes="Balanced mobile/CPU tier."),
    ModelSpec("yi-1.5-6b-chat","6b","transformers",
              ("chat","reasoning","research","code"),
              "01-ai/Yi-1.5-6B-Chat", min_ram_gb=12.0,
              notes="Upper mobile tier; quantization recommended."),
]
