from apps.providers.registry import PROVIDERS
from apps.providers.state import (
    get_failure_count,
)


FAILURE_THRESHOLD = 3


class ProviderRouter:

    @classmethod
    def get_provider(cls):

        available = []

        for name, provider in PROVIDERS.items():

            failures = get_failure_count(name)

            if failures < FAILURE_THRESHOLD:
                available.append((name, provider))

        if not available:
            raise Exception("No healthy providers available")

        return available[0]