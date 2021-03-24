def find_all(s, pattern):
    indexes, start = [], 0
    while start < len(s):
        index = s.find(pattern, start)
        if index == -1:
            break
        indexes.append(index)
        start = index + 1
    return indexes

