import heapq


def bfs(start, end, get_adjacent):
    queue = [(0, start)]
    seen = set()

    while len(queue) > 0:
        length, item = heapq.heappop(queue)

        if item in seen:
            continue

        if item == end:
            return length

        seen.add(item)

        for adjacent in get_adjacent(item):
            if adjacent in seen:
                continue
            heapq.heappush(queue, (length + 1, adjacent))
