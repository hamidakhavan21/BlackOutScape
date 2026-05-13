import random
import time
import uuid

from apps.providers.base.provider import BaseProvider


class KavenegarProvider(BaseProvider):
    def send(self, payload: dict) -> dict:
        latency = random.randint(100, 1000)

        time.sleep(latency / 1000)

        success = random.choice([True, True, True, False])

        if not success:
            raise Exception("Provider temporary failure")

        return {
            "provider": "kavenegar",
            "latency_ms": latency,
            "status": "sent",
            "provider_message_id": str(uuid.uuid4()),
        }
