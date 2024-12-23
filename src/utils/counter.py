from typing import Generator


def up_and_down(limit: int) -> Generator[int, None, None]:
    """
    Generator function that counts up to a limit and back down to 0.
    E.g. limit = 3 yields: (1, 2, 3, 2, 1, 0, 1, 2,...)

    Args:
        limit (int): The upper limit.
    """
    if limit <= 0:
        print("Limit must be > 0.")
        return None
    while True:
        for i in range(1, limit + 1):
            yield i
        for i in range(limit - 1, -1, -1):
            yield i
