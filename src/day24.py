from functools import cache
from typing import List, Union, Tuple


def string_to_valley(content: str) -> List[List[str]]:
    return [
        [ch if ch == "." else [ch] for ch in row[1:-1]]
        for row in content.split("\n")[1:-1]
    ]


def valley_to_string(valley: List[List[str]]) -> str:
    first_row = "#." + "".join(["#"] * len(valley[0]))
    content = first_row + "\n"
    for row in valley:
        # Show "." as ".", [">"] as ">" and [">", "<"] as "2"
        content += (
            "#"
            + "".join(
                [
                    ch if ch == "." else (ch[0] if len(ch) == 1 else str(len(ch)))
                    for ch in row
                ]
            )
            + "#\n"
        )
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


def tuple_valley(valley: List[List[Union[str, List[str]]]]):
    return tuple(
        tuple(item if isinstance(item, str) else tuple(x for x in item) for item in row)
        for row in valley
    )


@cache
def simulate_one_minutes(valley: Tuple) -> List:
    the_copy = copy_valley(valley)
    for y in range(len(valley)):
        for x in range(len(valley[0])):
            cell = valley[y][x]
            if isinstance(cell, tuple):
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


class DoneException(Exception):
    def __init__(self, mins):
        super().__init__()
        self.mins = mins


def simulate(valley: List[List[str]], minutes: int) -> List[List[str]]:
    tuple_valleys = []
    for i in range(minutes):
        print(i)
        tuple_valleys.append(tuple_valley(valley))
        # todo wait at (or return to) the start point
        # if is_path(tuple_valleys, 0, 0):
        #     raise DoneException(i)
        # else:

        # The case where we wait at the start position for j moves
        # for j in range(len(tuple_valleys)):
        tv = tuple(tuple_valleys)
        # if is_path(tv[j:], -1, 0):
        if is_path(tv, -1, 0):
            raise DoneException(i)
        valley = simulate_one_minutes(tuple_valleys[-1])

    return valley


@cache
def is_path(valleys, start_y, start_x):

    if not valleys:
        return False

    valley = valleys[0]

    manhattan_distance = ((len(valley)-1) - start_y) + ((len(valley[0])-1) - start_x)
    # If we are right above the exit, we can get there next move
    # Note that there are no vertical blizzards in the first or final columns
    if manhattan_distance == 0:
        return True
    elif manhattan_distance > len(valleys):
        return False

    # if start_y == len(valley) - 1 and start_x == len(valley[0]) - 1:
    #     return True

    if start_y > 0 and valley[start_y - 1][start_x] == ".":
        path_up = is_path(valleys[1:], start_y - 1, start_x)
        if path_up:
            return True

    # special case
    if start_y == 0 and start_x == 0:
        path_from_entrance = is_path(valleys[1:], -1, 0)
        if path_from_entrance:
            return True

    # another special case
    if start_y == -1 and start_x == 0:
        return is_path(valleys[1:], -1, 0) or (valley[0][0] == "." and is_path(valleys[1:], 0, 0))

    if start_y < len(valley) - 1 and valley[start_y + 1][start_x] == ".":
        path_down = is_path(valleys[1:], start_y + 1, start_x)
        if path_down:
            return True

    if start_x > 0 and valley[start_y][start_x - 1] == ".":
        path_left = is_path(valleys[1:], start_y, start_x - 1)
        if path_left:
            return True

    if start_x < len(valley[0]) - 1 and valley[start_y][start_x + 1] == ".":
        path_right = is_path(valleys[1:], start_y, start_x + 1)
        if path_right:
            return True

    # Stay put
    if is_path(valleys[1:], start_y, start_x) and valley[start_y][start_x] == ".":
        return True

    return False


def one(content):
    try:
        simulate(string_to_valley(content), 1_000_000)
    except DoneException as e:
        return e.mins


def two(lines):
    pass


def main():
    with open("../inputs/day24.txt", encoding="utf-8") as f:
        content = f.read()
    print("one:", one(content))
    print("two:", two(content))


if __name__ == "__main__":
    main()
