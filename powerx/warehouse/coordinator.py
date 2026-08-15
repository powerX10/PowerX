from .checksum import verify_checksums

class WarehouseCoordinator:
    def __init__(self, backend, cache):
        self.backend, self.cache = backend, cache
    def stage(self, spec):
        cached = self.cache.root/spec.folder_name
        if cached.exists() and any(cached.rglob("*")):
            self.cache.touch(spec.id,cached)
            return cached
        if not self.backend.exists(spec.folder_name):
            raise FileNotFoundError(f"{spec.id} is not in Google Drive warehouse")
        self.cache.ensure_space(512*1024*1024)
        p=self.backend.stage_to(spec.folder_name,self.cache.root)
        errs=verify_checksums(p)
        if errs and errs != ["SHA256SUMS missing"]:
            raise RuntimeError("Checksum failure: "+", ".join(errs[:5]))
        self.cache.touch(spec.id,p)
        return p
