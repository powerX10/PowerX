import os
from pathlib import Path
from powerx.warehouse.catalog import DEFAULT_MODELS
from powerx.warehouse.manifest import WarehouseManifest
root=Path(os.getenv("POWERX_DRIVE_MODELS_ROOT","/content/drive/MyDrive/PowerX/Models"))
root.mkdir(parents=True,exist_ok=True)
WarehouseManifest(root/"powerx-models.json").save(DEFAULT_MODELS)
print("warehouse",root)
print("models",len(DEFAULT_MODELS))
