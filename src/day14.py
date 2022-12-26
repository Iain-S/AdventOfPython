import numpy as np


class Cave:
    def __init__(self, paths):
        xmin = 10_000
        xmax = 1
        ymin = 0
        ymax = 0

        for path in paths:
            for x, y in path:
                xmin = min(xmin, x)
                xmax = max(xmax, x)
                ymax = max(ymax, y)

        self.contents = np.zeros((xmax - xmin + 1, ymax - ymin + 1))

        for path in paths:
            for start, stop in zip(path[:-1], path[1:]):
                startx = min(start[0], stop[0]) - xmin
                stopx = max(start[0], stop[0]) + 1 - xmin
                starty = min(start[1], stop[1])
                stopy = max(start[1], stop[1]) + 1
                self.contents[starty:stopy, startx:stopx] = 4

        self.sourcex = 500 - xmin
        self.contents[0, self.sourcex] = 1
        self.falling_sand = []  # only the sand in motion
        self.static_sand = []

    def take_turn(self):
        i = 0
        while i < len(self.falling_sand):
            # Note these are in y,x not x,y
            particle = self.falling_sand[i]
        # for i, particle in self.falling_sand:
            self.contents[particle[0], particle[1]] = 0

            if self.contents[particle[0]+1, particle[1]] == 0:
                # down
                particle[0] += 1
            elif self.contents[particle[0]+1, particle[1]-1] == 0:
                # diag left
                particle[0] += 1
                particle[1] -= 1
            elif self.contents[particle[0]+1, particle[1]+1] == 0:
                # diag right
                particle[0] += 1
                particle[1] += 1
            else:
                # stops
                self.static_sand.append(self.falling_sand.pop(i))
                i -= 1

            self.contents[particle[0], particle[1]] = 3
            i += 1

        # Add a new grain
        assert self.contents[1, self.sourcex] == 0
        self.contents[1, self.sourcex] = 3
        self.falling_sand.append([1, self.sourcex])


def get_paths(lines):
    paths = []
    for line in lines:
        path = []
        for pair in line.split(" -> "):
            path.append(eval(pair))
        paths.append(path)
    return paths


def build_cave(lines):
    cave = Cave(get_paths(lines))

    return cave


def one(lines):
    cave = Cave(get_paths(lines))
    while True:
        try:
            cave.take_turn()
        except IndexError:
            # If sand goes outside of the cave then we know it will fall forever
            return len(cave.static_sand)


def two(lines):
    pass


def main():
    with open("../inputs/day14.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
