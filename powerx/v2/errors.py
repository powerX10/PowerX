class PowerXError(Exception): pass
class PowerXRuntimeError(PowerXError): pass
class PowerXPermissionError(PowerXError): pass
class PowerXToolError(PowerXError): pass
class PowerXValidationError(PowerXError): pass
class PowerXExternalError(PowerXError): pass

# Backward-compatible exceptions used by ZIP1/ZIP2.
class AdapterUnavailable(PowerXRuntimeError): pass
class ModelLoadError(PowerXRuntimeError): pass
class InferenceError(PowerXRuntimeError): pass
class WarehouseError(PowerXRuntimeError): pass
class CacheError(PowerXRuntimeError): pass
class RegistryError(PowerXRuntimeError): pass
class WorkerError(PowerXRuntimeError): pass
