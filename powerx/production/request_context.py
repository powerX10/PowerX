from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class RequestContext:
    request_id: str

    @classmethod
    def create(cls, supplied: str | None = None):
        value = supplied.strip() if supplied else ""
        return cls(request_id=value[:128] if value else str(uuid.uuid4()))
