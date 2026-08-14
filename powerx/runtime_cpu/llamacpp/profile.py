from dataclasses import dataclass


@dataclass(frozen=True)
class LlamaCppProfile:
    id: str
    model_path_env: str
    served_model_name: str
    context_size: int = 8192
    threads: int = 4
    batch_size: int = 256
    gpu_layers: int = 0
    extra_args: tuple[str, ...] = ()

    def server_args(
        self,
        *,
        binary: str,
        model_path: str,
        host: str,
        port: int,
    ) -> list[str]:
        args = [
            binary,
            "--model", model_path,
            "--host", host,
            "--port", str(port),
            "--ctx-size", str(self.context_size),
            "--threads", str(self.threads),
            "--batch-size", str(self.batch_size),
            "--n-gpu-layers", str(self.gpu_layers),
        ]
        args.extend(self.extra_args)
        return args
