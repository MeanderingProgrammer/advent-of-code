from dataclasses import dataclass
from typing import Callable, Optional


@dataclass(frozen=True)
class Search[T]:
    start: T
    end: T
    neighbors: Callable[[T], list[T]]

    def bfs(self) -> Optional[int]:
        return self.traverse(front=True)

    def dfs(self) -> Optional[int]:
        return self.traverse(front=False)

    def traverse(self, front: bool) -> Optional[int]:
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
