import heapq


def bfs(start, is_done, get_adjacent):
    queue = [start]

    while len(queue) > 0:
        length, item = heapq.heappop(queue)

        if is_done(item):
            return length

        for adjacent in get_adjacent(length, item):
            heapq.heappush(queue, adjacent)


def reachable(start, maximum, get_adjacent):
    queue = [(0, start)]
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


def connected(graph, start):
    queue = [start]
    seen = set()

    while len(queue) > 0:
        current = queue.pop()

        if current in seen:
            continue

        seen.add(current)

        for adjacent in graph[current]:
            if adjacent not in seen:
                queue.append(adjacent)

    return seen

