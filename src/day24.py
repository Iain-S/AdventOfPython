from functools import cache
from typing import List


def string_to_valley(content: str) -> List[List[str]]:
    return [[ch if ch == "." else [ch] for ch in row[1:-1]] for row in content.split("\n")[1:-1]]


def valley_to_string(valley: List[List[str]]) -> str:
    first_row = "#." + "".join(["#"]*len(valley[0]))
    content = first_row + "\n"
    for row in valley:
        # Show "." as ".", [">"] as ">" and [">", "<"] as "2"
        content += "#"+"".join([ch if ch == "." else (ch[0] if len(ch)==1 else str(len(ch))) for ch in row])+"#\n"
    content += "".join(reversed(first_row))
    return content


def in_bounds(valley, y, x):
    if y < 0 or y >= len(valley):
        return False

    if x < 0 or x >= len(valley[0]):
        return False

    return True


def copy_valley(valley):
    # return [[ch if isinstance(ch, str) else [x for x in ch] for ch in row] for row in valley]
    return [["." for _ in row] for row in valley]

# @cache
def simulate_one_minutes(valley):
    the_copy = copy_valley(valley)
    for y in range(len(valley)):
        for x in range(len(valley[0])):
            cell = valley[y][x]
            if isinstance(cell, list):
                for item in cell:
                    if item == ">":
                        new_x = x + 1
                        new_y = y
                        if not in_bounds(valley, new_y, new_x):
                            # wrap
                            new_x = 0
                    elif item == "<":
                        new_x = x - 1
                        new_y = y
                        if not in_bounds(valley, new_y, new_x):
                            # wrap
                            new_x = len(valley[0]) - 1
                    elif item == "^":
                        new_x = x
                        new_y = y - 1
                        if not in_bounds(valley, new_y, new_x):
                            # wrap
                            new_y = len(valley) - 1
                    elif item == "v":
                        new_x = x
                        new_y = y + 1
                        if not in_bounds(valley, new_y, new_x):
                            # wrap
                            new_y = 0
                    else:
                        assert False, f"{item=}"

                    if isinstance(the_copy[new_y][new_x], str):
                        the_copy[new_y][new_x] = [item]
                    elif isinstance(the_copy[new_y][new_x], list):
                        the_copy[new_y][new_x].append(item)
                    else:
                        assert False, f"{the_copy[new_y][new_x]}, {new_y}, {new_x}"

    return the_copy


def simulate(valley: List[List[str]], minutes: int) -> List[List[str]]:
    for i in range(minutes):
        valley = simulate_one_minutes(valley)
    return valley


def one(lines):
    pass


def two(lines):
    pass


def main():
    with open("../inputs/day24.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
