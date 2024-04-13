from typing import Callable, Optional


def bfs[T](start: T, end: T, get_adjacent: Callable[[T], list[T]]) -> Optional[int]:
    queue: list[tuple[int, T]] = [(0, start)]
    seen: set[T] = set()
    while len(queue) > 0:
        length, item = queue.pop(0)
        if item in seen:
            continue
        seen.add(item)
        if item == end:
            return length
        for adjacent in get_adjacent(item):
            if adjacent not in seen:
                queue.append((length + 1, adjacent))
    return None
