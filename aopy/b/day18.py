"""Solve the day's problem."""
from operator import add, mul
from functools import partial

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


def dig_interior(loop_: list[str]) -> list[str]:
    """Dig the interior."""
    loop = [list(x) for x in loop_]
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
    # loop = dig_loop(lines)
    # write_to_file(loop, "./day18_loop.txt")
    #
    # excavation = dig_interior(loop)
    # write_to_file(excavation, "./day18_exc.txt")
    #
    # plan_a = sum([x.count("#") for x in excavation])
    plan_a = 52_035
    print("Plan A: ", plan_a)

    lines_b = [line.split(" ") for line in lines]
    lines_c = [(line[0], int(line[1])) for line in lines_b]
    loop = walk_loop(lines_c)
    bounding_rect = calc_bounding_rect(loop)
    # sys.setrecursionlimit(1500)
    plan_b = get_area(loop, bounding_rect)
    print("Plan B: ", plan_b)
    return plan_b


def two(lines: list[str]) -> int:
    new_lines = []
    for line in lines:
        hexa = line[line.index("#") + 1: -1]
        direction = {
            "0": "R",
            "1": "D",
            "2": "L",
            "3": "U",
        }[hexa[-1]]
        new_lines.append(" ".join([direction, str(int(hexa[:-1], 16)), ""]))

    distances = set(int(x.split(" ")[1]) for x in new_lines)
    return 0


def main() -> None:
    with open("./inputs/b/day18.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))

    with open("./inputs/b/day18.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("two:", two(lines))


tpoint = tuple[int, int]
tpointpair = tuple[tpoint, tpoint]
trect = tpointpair
tloop = list[tpointpair]


def walk_loop(directions: list[tuple[str, int]]) -> tloop:
    """Follow the instructions and take notes of our position."""
    x, y = 0, 0
    result = []

    for direction in directions:
        newx, newy = map(
            add, (x, y), map(partial(mul, direction[1]), compass[direction[0]])
        )
        result.append(((x, y), (newx, newy)))
        x, y = newx, newy

    return result


def calc_bounding_rect(loop: tloop) -> trect:
    """Get a rectangle that bounds the loop."""
    top_left = (min([x[0][0] for x in loop]) - 1, min([x[0][1] for x in loop]) - 1)
    bottom_right = (max([x[1][0] for x in loop]) + 1, max([x[1][1] for x in loop]) + 1)
    return top_left, bottom_right


def rect_in_loop(loop: tloop, rect: trect) -> bool:
    """Is rect entirely within loop?"""
    # We can assume that the loop and rectangle don't intersect.
    bounding_rect = calc_bounding_rect(loop)
    a_line = rect[0], (rect[0][0], bounding_rect[0][1])

    # If the new line intersects the loop, the rectangle is entirely within the loop.
    return intersects(loop, a_line)


def point_in_rect(point: tpoint, rect: trect) -> bool:
    """Is the point inside the rectangle?"""
    top_left, bottom_right = rect
    if (point[0] >= top_left[0] and point[1] >= top_left[1]) and (
            point[0] <= bottom_right[0] and point[1] <= bottom_right[1]
    ):
        return True
    return False


def intersects(loop: tloop, rect: trect) -> bool:
    """Does the loop cut across the rectangle?"""
    top_left, bottom_right = rect
    for starts_at, finishes_at in loop:
        # If either end of the line segment is in the rectangle
        if point_in_rect(starts_at, rect) or point_in_rect(finishes_at, rect):
            return True

        # Else, if it cuts through vertically...
        if top_left[0] <= starts_at[0] <= bottom_right[0] and (
                (starts_at[1] < top_left[1] and finishes_at[1] > bottom_right[1])
                or (starts_at[1] < bottom_right[1] and finishes_at[1] < top_left[1])
        ):
            return True

        # Else, if it cuts through horizontally...
        x = top_left[1] <= starts_at[1] <= bottom_right[1]
        y = starts_at[0] < top_left[0] and finishes_at[0] > bottom_right[0]
        z = starts_at[0] < bottom_right[0] and finishes_at[0] < top_left[0]
        if x and (y or z):
            return True

    return False


def split_range(start: int, stop: int) -> tuple[tuple[int, int], tuple[int, int]]:
    diff = stop - start
    return (start, start - 1 + ((diff + 1) // 2)), (start + ((diff + 1) // 2), stop)


def split_rect(rect: trect) -> tuple[trect, ...]:
    """Split rect into quadrants."""

    size = (rect[1][0] - rect[0][0] + 1) * (rect[1][1] - rect[0][1] + 1)
    assert size > 1

    left, right = split_range(rect[0][0], rect[1][0])
    upper, lower = split_range(rect[0][1], rect[1][1])

    # top left
    tl = ((left[0], upper[0]), (left[1], upper[1]))
    # top right
    tr = ((right[0], upper[0]), (right[1], upper[1]))
    # bottom right
    br = ((right[0], lower[0]), (right[1], lower[1]))
    # bottom left
    bl = ((left[0], lower[0]), (left[1], lower[1]))

    if size == 2:
        if rect[0][0] == rect[1][0]:
            # vertical
            assert tr != br
            return tr, br
        else:
            # horizontal
            assert bl != br
            return bl, br

    assert tl[0][0] <= tl[1][0]
    assert tl[0][1] <= tl[1][1]
    assert tr[0][0] <= tr[1][0]
    assert tr[0][1] <= tr[1][1]
    assert br[0][0] <= br[1][0]
    assert br[0][1] <= br[1][1]
    assert bl[0][0] <= bl[1][0]
    assert bl[0][1] <= bl[1][1]

    return tl, tr, br, bl


def get_area(loop: tloop, rect: trect) -> int:
    """Get the area of the rect that is enclosed by loop."""
    rect_area = (rect[1][0] - rect[0][0] + 1) * (rect[1][1] - rect[0][1] + 1)
    if intersects(loop, rect):
        if rect_area == 1:
            # Count the loop in the area calculation.
            return 1

        # Sum the areas of the four quadrants.
        rects = split_rect(rect)
        areas = [get_area(loop, x) for x in rects]
        return sum(areas)
        # return sum([get_area(loop, x) for x in split_rect(rect)])
    elif rect_in_loop(loop, rect):
        return rect_area

    # The rectangle must be entirely outside the loop.
    return 0


if __name__ == "__main__":
    main()
