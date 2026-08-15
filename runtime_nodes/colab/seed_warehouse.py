import os
from pathlib import Path
from powerx.warehouse.catalog import DEFAULT_MODELS
from powerx.warehouse.hf_seed import seed_huggingface_model
from runtime_nodes.colab.drive_mount import mount_powerx_drive

root=Path(mount_powerx_drive())
for spec in DEFAULT_MODELS:
    print("Seeding",spec.id)
    print(seed_huggingface_model(spec,root,token=os.getenv("HF_TOKEN")))
