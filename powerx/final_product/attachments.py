import base64,mimetypes
from pathlib import Path
MAX_INLINE_BYTES=20*1024*1024
def encode_file(path):
    p=Path(path);raw=p.read_bytes()
    if len(raw)>MAX_INLINE_BYTES:raise ValueError("attachment exceeds 20MiB")
    return {"name":p.name,"mime_type":mimetypes.guess_type(p.name)[0] or "application/octet-stream","data_b64":base64.b64encode(raw).decode()}
