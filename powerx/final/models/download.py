from pathlib import Path
import hashlib
import os
import tempfile
import httpx

class DownloadError(RuntimeError): pass

def sha256_file(path: str | Path, chunk: int = 4 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while data := f.read(chunk):
            h.update(data)
    return h.hexdigest()

async def download_file(
    url: str,
    destination: str | Path,
    *,
    expected_sha256: str | None = None,
    bearer_token: str | None = None,
    timeout: float = 600.0,
) -> dict:
    dest = Path(destination).expanduser().resolve()
    dest.parent.mkdir(parents=True, exist_ok=True)

    headers = {}
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"

    fd, tmp_name = tempfile.mkstemp(prefix=dest.name + ".", dir=str(dest.parent))
    os.close(fd)
    tmp = Path(tmp_name)

    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            async with client.stream("GET", url, headers=headers) as response:
                response.raise_for_status()
                with tmp.open("wb") as f:
                    async for chunk in response.aiter_bytes(1024 * 1024):
                        f.write(chunk)

        digest = sha256_file(tmp)
        if expected_sha256 and digest.lower() != expected_sha256.lower():
            raise DownloadError("SHA256 checksum mismatch")

        tmp.replace(dest)
        return {
            "ok": True,
            "path": str(dest),
            "size_bytes": dest.stat().st_size,
            "sha256": digest,
        }
    except Exception:
        tmp.unlink(missing_ok=True)
        raise
