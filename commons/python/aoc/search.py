import heapq
from typing import Callable, Optional


def bfs[T](start: T, end: T, get_adjacent: Callable[[T], list[T]]) -> Optional[int]:
    queue: list[tuple[int, T]] = [(0, start)]
    seen = set()
    while len(queue) > 0:
        length, item = heapq.heappop(queue)
        if item in seen:
            continue
        seen.add(item)
        if item == end:
            return length
        for adjacent in get_adjacent(item):
            if adjacent not in seen:
                heapq.heappush(queue, (length + 1, adjacent))
    return None


def bfs_paths[
    T
](
    start: tuple[T, str],
    end: T,
    get_adjacent: Callable[[tuple[T, str]], list[tuple[T, str]]],
) -> list[str]:
    queue: list[tuple[int, tuple[T, str]]] = [(0, start)]
    seen = set()
    paths = []
    while len(queue) > 0:
        length, item = heapq.heappop(queue)
        if item in seen:
            continue
        seen.add(item)
        if item[0] == end:
            paths.append(item[1])
            # Stop exploring this direction as soon as we reach end
            continue
        for adjacent in get_adjacent(item):
            if adjacent not in seen:
                heapq.heappush(queue, (length + 1, adjacent))
    return paths


def bfs_complete[
    T
](
    start: tuple[int, T],
    is_done: Callable[[T], bool],
    get_adjacent: Callable[[T], list[tuple[int, T]]],
) -> Optional[int]:
    queue = [start]
    seen: dict[T, int] = dict()
    while len(queue) > 0:
        priority, item = heapq.heappop(queue)
        if is_done(item):
            return priority
        for additional, adjacent in get_adjacent(item):
            entry = (priority + additional, adjacent)
            current = seen.get(entry[1])
            if current is None or entry[0] < current:
                if current is not None:
                    queue.remove((current, entry[1]))
                    heapq.heapify(queue)
                heapq.heappush(queue, entry)
                seen[entry[1]] = entry[0]
    return None


def reachable[
    T
](start: T, maximum: int, get_adjacent: Callable[[T], list[T]]) -> set[T]:
    queue: list[tuple[int, T]] = [(0, start)]
    seen = set()
    while len(queue) > 0:
        length, item = heapq.heappop(queue)
        if item in seen:
            continue
        seen.add(item)
        length += 1
        for adjacent in get_adjacent(item):
            if adjacent not in seen and length <= maximum:
                heapq.heappush(queue, (length, adjacent))
    return seen


def connected[T](graph: dict[T, set[T]], start: T) -> set[T]:
    queue: list[T] = [start]
    seen: set[T] = set()
    while len(queue) > 0:
        current = queue.pop()
        if current in seen:
            continue
        seen.add(current)
        for adjacent in graph[current]:
            if adjacent not in seen:
                queue.append(adjacent)
    return seen
