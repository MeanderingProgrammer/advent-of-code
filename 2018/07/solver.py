import re

from commons.aoc_parser import Parser


STEP_PATTERN = '^Step (.) must be finished before step (.) can begin.$'


class Graph:

    def __init__(self):
        self.nodes = set()
        self.graph = {}

    def add_edge(self, start, end):
        self.nodes.add(start)
        self.nodes.add(end)
        if start not in self.graph:
            self.graph[start] = set()
        self.graph[start].add(end)

    def topo_sort(self):
        completed = []
        while len(completed) != len(self.nodes):
            available = self.next_available(completed)
            completed.append(available)
        return completed

    def get_duration(self, num_workers, base_time):
        completed = []
        queue = WorkerQueue(num_workers, base_time)
        
        duration = 0
        while len(completed) != len(self.nodes):
            duration += 1
            available = self.available(completed)
            queue.enqueu(available)
            completed.extend(queue.tick())

        return duration

    def next_available(self, completed):
        return self.available(completed)[0]

    def available(self, completed):
        available = []
        for node in self.nodes:
            if node not in completed:
                needed = self.graph.get(node, set())
                have_all = all([need in completed for need in needed])
                if have_all:
                    available.append(node)
        available.sort()
        return available

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.graph)


class WorkerQueue:

    def __init__(self, num_workers, base_time):
        self.queue = [Worker(base_time) for i in range(num_workers)]
        self.tasks_seen = set()
        self.tasks_remaining = []

    def tick(self):
        completed = []
        for worker in self.queue:
            worker.tick()
            if worker.done() and worker.task is not None: 
                completed.append(worker.task)
                worker.clear()
        return completed

    def enqueu(self, tasks):
        tasks = [task for task in tasks if task not in self.tasks_seen]
        [self.tasks_seen.add(task) for task in tasks]
        self.tasks_remaining.extend(tasks)
        available_workers = [worker for worker in self.queue if worker.done()]

        tasks_to_assign = min(len(self.tasks_remaining), len(available_workers))
        for i in range(tasks_to_assign):
            available_workers[i].assign(self.tasks_remaining[i])
        self.tasks_remaining = self.tasks_remaining[tasks_to_assign:]


class Worker:

    def __init__(self, base_time):
        self.base_time = base_time
        self.task = None
        self.time_spent_on_task = 0

    def tick(self):
        self.time_spent_on_task += 1

    def done(self):
        if self.task is None:
            return True
        return self.time_spent_on_task >= self.task_time()

    def clear(self):
        self.task = None
        self.time_spent_on_task = 0

    def assign(self, task):
        self.task = task
        self.time_spent_on_task = 0

    def task_time(self):
        return ord(self.task) - ord('A') + 1 + self.base_time


def main():
    graph = get_graph()
    # Part 1: LAPFCRGHVZOTKWENBXIMSUDJQY
    print('Part 1: {}'.format(solve_part_1(graph)))
    # Part 2: 936
    print('Part 2: {}'.format(solve_part_2(graph)))


def solve_part_1(graph):
    order = graph.topo_sort()
    return ''.join(order)


def solve_part_2(graph):
    return graph.get_duration(5, 60)
    

def get_graph():
    graph = Graph()
    for line in Parser().lines():
        match = re.match(STEP_PATTERN, line)
        graph.add_edge(match[2], match[1])
    return graph


if __name__ == '__main__':
    main()
