import hashlib
import json
from uuid import UUID


def normalize(obj):
    if isinstance(obj, dict):
        return {k: normalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalize(v) for v in obj]
    if isinstance(obj, UUID):
        return str(obj)
    return obj


def generate_payload_hash(payload: dict) -> str:
    normalized_payload = normalize(payload)

    normalized = json.dumps(
        normalized_payload,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(normalized.encode()).hexdigest()
