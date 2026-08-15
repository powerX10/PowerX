from pathlib import Path
from huggingface_hub import snapshot_download
from .checksum import write_checksums

def seed_huggingface_model(spec, warehouse_root: Path, token=None):
    target = warehouse_root.expanduser()/spec.folder_name
    target.mkdir(parents=True, exist_ok=True)
    kwargs = dict(repo_id=spec.source_repo, revision=spec.revision,
                  local_dir=str(target), token=token)
    if spec.allow_patterns:
        kwargs["allow_patterns"] = list(spec.allow_patterns)
    snapshot_download(**kwargs)
    write_checksums(target)
    return target
