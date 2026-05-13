def exponential_backoff(retry_count: int) -> int:
    """
    Returns retry delay in seconds.

    Example:
    1 -> 2s
    2 -> 4s
    3 -> 8s
    """

    return min(2 ** retry_count, 300)