import json,os,shutil
from powerx.mobile_profiles import choose_profile
def memory_gb():
 try:return os.sysconf("SC_PHYS_PAGES")*os.sysconf("SC_PAGE_SIZE")/1024**3
 except:return 0.0
def status():
 free=shutil.disk_usage(os.path.expanduser("~")).free/1024**3;p=choose_profile(memory_gb(),free,True)
 return {"ram_gb":round(memory_gb(),2),"free_storage_gb":round(free,2),"profile":p.__dict__ if p else None,"fallback":"cpu" if not p else None}
if __name__=="__main__":print(json.dumps(status(),indent=2))
