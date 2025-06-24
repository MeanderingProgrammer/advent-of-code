from aoc import answer
from aoc.parser import Parser


class Group:
    def __init__(self, group: str):
        group = Group.remove_special(group)
        group, garbage_removed = Group.remove_garbage(group)
        self.group: str = group
        self.removed: int = garbage_removed

    @staticmethod
    def remove_special(group: str) -> str:
        result: str = ""
        index: int = 0
        while index < len(group):
            char = group[index]
            if char == "!":
                index += 2
            else:
                result += char
                index += 1
        return result

    @staticmethod
    def remove_garbage(group: str) -> tuple[str, int]:
        result: str = ""
        index: int = 0
        removed: int = 0
        while index < len(group):
            char = group[index]
            if char == "<":
                end = group[index:].index(">")
                removed += end - 1
                index += end
            else:
                result += char
            index += 1
        return result, removed

    def score(self) -> int:
        score: int = 0
        level: int = 0
        for char in self.group:
            if char == "{":
                level += 1
                score += level
            elif char == "}":
                level -= 1
        return score


@answer.timer
def main() -> None:
    group = Group(Parser().string())
    answer.part1(15922, group.score())
    answer.part2(7314, group.removed)


if __name__ == "__main__":
    main()
