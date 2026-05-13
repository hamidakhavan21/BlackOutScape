from collections import defaultdict

provider_failures = defaultdict(int)


def mark_failure(provider_name: str):
    provider_failures[provider_name] += 1


def reset_failures(provider_name: str):
    provider_failures[provider_name] = 0


def get_failure_count(provider_name: str) -> int:
    return provider_failures[provider_name]
