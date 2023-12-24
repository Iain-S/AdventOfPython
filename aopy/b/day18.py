"""Solve the day's problem."""
import math
from operator import add

compass = {
    "U": (0, -1),
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0),
}


def dig_loop(lines: list[str]) -> list[str]:
    """Dig a loop."""
    loop = [["#"]]
    x, y = 0, 0
    for line in lines:
        direction, meters, _ = line.split(" ")
        for _ in range(int(meters)):
            x, y = map(add, (x, y), compass[direction])
            if y < 0:
                loop.insert(0, ["." for _ in range(len(loop[0]))])
                y = 0
            elif y >= len(loop):
                loop.append(["." for _ in range(len(loop[0]))])
            if x < 0:
                for row in loop:
                    row.insert(0, ".")
                x = 0
            elif x >= len(loop[0]):
                for row in loop:
                    row.append(".")
            loop[y][x] = "#"

    return ["".join(x) for x in loop]


def dig_interior(loop: list[str]):
    """Dig the interior."""
    loop = [list(x) for x in loop]
    changed = 1

    # hope that the middle is inside the loop
    midx, midy = len(loop) // 2, len(loop[0]) // 2
    loop[midx][midy] = "*"

    while changed > 0:
        changed = 0
        for y in range(1, len(loop) - 1):
            for x in range(1, len(loop[0]) - 1):
                if loop[y][x] == ".":
                    if (
                        loop[y - 1][x] == "*"
                        or loop[y + 1][x] == "*"
                        or loop[y][x - 1] == "*"
                        or loop[y][x + 1] == "*"
                    ):
                        loop[y][x] = "*"
                        changed += 1

    for line in loop:
        for i in range(len(line)):
            if line[i] == "*":
                line[i] = "#"

    return ["".join(x) for x in loop]


def write_to_file(lines: list[str], filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def one(lines: list[str]) -> int:
    loop = dig_loop(lines)
    write_to_file(loop, "./day18_loop.txt")

    excavation = dig_interior(loop)
    write_to_file(excavation, "./day18_exc.txt")

    return sum([x.count("#") for x in excavation])


def two(lines: list[str]) -> int:
    new_lines = []
    for line in lines:
        hexa = line[line.index("#") + 1 : -1]
        direction = {
            "0": "R",
            "1": "D",
            "2": "L",
            "3": "U",
        }[hexa[-1]]
        new_lines.append(" ".join([direction, str(int(hexa[:-1], 16)), ""]))

    distances = set(int(x.split(" ")[1]) for x in new_lines)
    gcd = math.gcd(*distances)

    loop = dig_loop(new_lines)
    # write_to_file(loop, "./day18_loop.txt")

    excavation = dig_interior(loop)
    # write_to_file(excavation, "./day18_exc.txt")

    return sum([x.count("#") for x in excavation])


def main() -> None:
    with open("./inputs/b/day18.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))

    with open("./inputs/b/day18.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("two:", two(lines))


if __name__ == "__main__":
    main()
