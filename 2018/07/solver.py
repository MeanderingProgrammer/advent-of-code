import re
from dataclasses import dataclass
from typing import Optional

from aoc import answer
from aoc.parser import Parser


@dataclass
class Worker:
    base_time: int
    task: Optional[str] = None
    time_spent_on_task: int = 0

    def clear(self) -> None:
        self.task = None
        self.time_spent_on_task = 0

    def assign(self, task: str) -> None:
        self.task = task
        self.time_spent_on_task = 0

    def tick(self) -> None:
        self.time_spent_on_task += 1

    def done(self) -> bool:
        if self.task is None:
            return True
        task_time = ord(self.task) - ord("A") + 1 + self.base_time
        return self.time_spent_on_task >= task_time


@dataclass
class WorkerQueue:
    queue: list[Worker]
    tasks_seen: set[str]
    tasks_remaining: list[str]

    def tick(self) -> list[str]:
        completed: list[str] = []
        for worker in self.queue:
            worker.tick()
            if worker.done() and worker.task is not None:
                completed.append(worker.task)
                worker.clear()
        return completed

    def enqueu(self, tasks: list[str]) -> None:
        unseen_tasks = [task for task in tasks if task not in self.tasks_seen]
        [self.tasks_seen.add(task) for task in unseen_tasks]
        self.tasks_remaining.extend(unseen_tasks)
        available_workers = self.available_workers()
        tasks_to_assign = min(len(self.tasks_remaining), len(available_workers))
        for i in range(tasks_to_assign):
            available_workers[i].assign(self.tasks_remaining[i])
        self.tasks_remaining = self.tasks_remaining[tasks_to_assign:]

    def available_workers(self) -> list[Worker]:
        return [worker for worker in self.queue if worker.done()]


@dataclass(frozen=True)
class Graph:
    nodes: set[str]
    graph: dict[str, set[str]]

    def add_edge(self, start: str, end: str) -> None:
        self.nodes.add(start)
        self.nodes.add(end)
        if start not in self.graph:
            self.graph[start] = set()
        self.graph[start].add(end)

    def topo_sort(self) -> list[str]:
        completed: list[str] = []
        while len(completed) != len(self.nodes):
            available = self.available(completed)[0]
            completed.append(available)
        return completed

    def available(self, completed: list[str]) -> list[str]:
        available: list[str] = []
        for node in self.nodes:
            if node in completed:
                continue
            needed = self.graph.get(node, set())
            if all([need in completed for need in needed]):
                available.append(node)
        available.sort()
        return available

    def get_duration(self, num_workers: int, base_time: int) -> int:
        queue = WorkerQueue(
            queue=[Worker(base_time) for _ in range(num_workers)],
            tasks_seen=set(),
            tasks_remaining=[],
        )
        completed = []
        duration = 0
        while len(completed) != len(self.nodes):
            duration += 1
            available = self.available(completed)
            queue.enqueu(available)
            completed.extend(queue.tick())
        return duration


def main() -> None:
    graph = get_graph()
    answer.part1("LAPFCRGHVZOTKWENBXIMSUDJQY", "".join(graph.topo_sort()))
    answer.part2(936, graph.get_duration(5, 60))


def get_graph() -> Graph:
    graph = Graph(nodes=set(), graph=dict())
    for line in Parser().lines():
        match = re.match("^Step (.) must be finished before step (.) can begin.$", line)
        assert match is not None
        graph.add_edge(match[2], match[1])
    return graph


if __name__ == "__main__":
    main()
