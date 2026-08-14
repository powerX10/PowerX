import json
from powerx.production.endpoint_config import registry_from_env

registry = registry_from_env()
print(json.dumps([x.__dict__ for x in registry.all()], indent=2))
