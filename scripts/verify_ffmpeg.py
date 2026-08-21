import shutil,sys
for x in ("ffmpeg","ffprobe"):
    p=shutil.which(x)
    print(x,p or "MISSING")
    if not p: sys.exit(2)
