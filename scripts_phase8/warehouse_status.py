import os
from pathlib import Path
root=Path(os.getenv("POWERX_DRIVE_MODELS_ROOT","/content/drive/MyDrive/PowerX/Models"))
print("root",root,"exists",root.exists())
if root.exists():
    for p in [x for x in root.iterdir() if x.is_dir()]:
        total=sum(x.stat().st_size for x in p.rglob("*") if x.is_file())
        print(p.name,f"{total/(1024**3):.2f} GiB")
