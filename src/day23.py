from typing import List


class Elf:
    def __init__(self, y, x, proposals):
        self.y = y
        self.x = x
        self.next = "N"
        self.proposals = proposals

    def first_half(self):
        pass

    def second_half(self):
        pass


def display_elves(elves: List[Elf]) -> List[str]:
    minx, miny, maxx, maxy = 10_000, 10_000, -10_000, -10_000
    for elf in elves:
        minx = min(minx, elf.x)
        miny = min(miny, elf.y)
        maxx = max(maxx, elf.x)
        maxy = max(maxy, elf.y)

    array = [["." for __ in range(maxx + 1 - minx)] for _ in range(maxy + 1 - miny)]

    for elf in elves:
        array[elf.y - miny][elf.x - minx] = "#"

    return ["".join(x) for x in array]


def double_grove(grove: List[List[str]]):
    half_y = len(grove) // 2
    if half_y * 2 < len(grove):
        half_y += 1
    # new_y = len(grove) * 2
    new_y = half_y * 2 + len(grove)
    # y_offset = len(grove) // 2
    y_offset = half_y
    # if new_y % 2 == 1:
    #     new_y += 1
    #     y_offset += 1

    half_x = len(grove[0]) // 2
    if half_x * 2 < len(grove[0]):
        half_x += 1
    new_x = half_x * 2 + len(grove[0])
    x_offset = half_x

    new_grove = [["." for __ in range(new_x)] for _ in range(new_y)]
    for y in range(len(grove)):
        for x in range(len(grove[0])):
            if grove[y][x] == "#":
                new_grove[y + y_offset][x + x_offset] = "#"

    return new_grove


def one(lines):
    grove = [[ch for ch in line] for line in lines]
    return simulate(grove)


def simulate(grove):
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    dirs_i = 0
    for _ in range(10):
        # First half
        for y in 1, len(grove) - 2:
            for cell in grove[y]:
                if cell == "#":
                    grove = double_grove(grove)
                    break

        for row in grove:
            for x in 1, len(row) - 2:
                if row[x] == "#":
                    grove = double_grove(grove)
                    break

        for y in range(len(grove)):
            for x in range(len(grove[0])):
                if grove[y][x] == "#":
                    by_self = True
                    for i in range(4):
                        dir = dirs[(dirs_i + i) % len(dirs)]
                        x_new = x + dir[1]
                        y_new = y + dir[0]

                        left = (y_new - 1, x_new) if dir[0] == 0 else (y_new, x_new - 1)
                        right = (
                            (y_new + 1, x_new) if dir[0] == 0 else (y_new, x_new + 1)
                        )
                        if (
                            grove[y_new][x_new] == "#"
                            or grove[left[0]][left[1]] == "#"
                            or grove[right[0]][right[1]] == "#"
                        ):
                            by_self = False
                    if by_self:
                        break

                    for i in range(4):
                        dir = dirs[(dirs_i + i) % len(dirs)]
                        x_new = x + dir[1]
                        y_new = y + dir[0]

                        left = (y_new - 1, x_new) if dir[0] == 0 else (y_new, x_new - 1)
                        right = (
                            (y_new + 1, x_new) if dir[0] == 0 else (y_new, x_new + 1)
                        )
                        if (
                            grove[y_new][x_new] == "."
                            and grove[left[0]][left[1]] != "#"
                            and grove[right[0]][right[1]] != "#"
                        ):
                            grove[y_new][x_new] = "1"
                            break
                        else:
                            try:
                                num = int(grove[y_new][x_new])
                                num += 1
                                grove[y_new][x_new] = str(num)
                                break
                            except ValueError:
                                pass

        # Second half
        for y in range(len(grove)):
            for x in range(len(grove[0])):
                if grove[y][x] == "#":
                    for i in range(4):
                        dir = dirs[(dirs_i + i) % len(dirs)]
                        x_new = x + dir[1]
                        y_new = y + dir[0]
                        if grove[y_new][x_new] == "1":
                            grove[y_new][x_new] = "#"
                            grove[y][x] = "."
                            break

        for y in range(len(grove)):
            for x in range(len(grove[0])):
                try:
                    int(grove[y][x])
                    grove[y][x] = "."
                except ValueError:
                    pass

        dirs_i += 1

    total =calc_score(grove)
    return total


def calc_score(grove):
    # drop empty start and end rows
    for i in 0, -1:
        while True:
            is_empty = True
            for cell in grove[i]:
                if cell == "#":
                    is_empty = False

            if is_empty:
                grove.pop(i)
            else:
                break

    # drop empty start and end columns
    for i in 0, -1:
        while True:
            is_empty = True
            for j in range(len(grove)):
                cell = grove[j][i]
                if cell == "#":
                    is_empty = False

            if is_empty:
                for j in range(len(grove)):
                    grove[j].pop(i)
            else:
                break

    total = 0
    for y in range(len(grove)):
        for x in range(len(grove[0])):
            if grove[y][x] == ".":
                total += 1

    return total






def two(lines):
    pass


def main():
    with open("../inputs/day23.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
