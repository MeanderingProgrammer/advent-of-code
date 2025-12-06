import heapq
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Search[T]:
    start: T
    end: T
    neighbors: Callable[[T], list[T]]

    def bfs(self) -> int | None:
        return self.traverse(front=True)

    def dfs(self) -> int | None:
        return self.traverse(front=False)

    def traverse(self, front: bool) -> int | None:
        queue: list[tuple[int, T]] = [(0, self.start)]
        seen: set[T] = set()
        while len(queue) > 0:
            # Remove from either the front (BFS) or back (DFS)
            length, item = queue.pop(0 if front else -1)
            if item in seen:
                continue
            seen.add(item)
            if item == self.end:
                return length
            for adjacent in self.neighbors(item):
                if adjacent not in seen:
                    queue.append((length + 1, adjacent))
        return None


@dataclass(frozen=True)
class Dijkstra[T]:
    start: T
    done: Callable[[T], bool]
    neighbors: Callable[[T], list[tuple[int, T]]]

    def run(self) -> int | None:
        queue: list[tuple[int, T]] = [(0, self.start)]
        seen: set[T] = set()
        while len(queue) > 0:
            value, item = heapq.heappop(queue)
            if item in seen:
                continue
            seen.add(item)
            if self.done(item):
                return value
            for cost, adjacent in self.neighbors(item):
                if adjacent not in seen:
                    heapq.heappush(queue, (value + cost, adjacent))
        return None
