def calc_highest_y(highpoints):
    """The y value of the highest occupied square."""
    highest_y = 0
    for column in highpoints:
        column_max = calc_highest_in_col(column)
        if column_max > highest_y:
            highest_y = column_max

    return highest_y


def calc_highest_in_col(column):
    for i in range(len(column)):
        j = len(column) - i - 1
        if column[j]:
            return j

    assert False, "Bottomed out"



class Rock:
    def __init__(self, highest_y):
        """Spawn the rock above highest_y."""
        del highest_y

        # Rock shapes are lists of (one or two) rectangles
        self.xy_positions = None
        self.heights_widths = None

    def intersects_down(self, highpoints) -> bool:
        """Will the rock crash if we move it any further down?"""
        assert len(self.heights_widths) == len(self.xy_positions)
        for i, position in enumerate(self.xy_positions):
            x, y = position
            height, width = self.heights_widths[i]

            for j in range(width):
                if len(highpoints[x + j]) > y-1 and highpoints[x+j][y-1]:
                    return True

        return False

    def intersects_side(self, direction, highpoints) -> bool:
        """Will the rock crash into the wall or another rock if we move it in direction?"""
        assert len(self.heights_widths) == len(self.xy_positions)
        assert direction in ("<", ">")

        for i, position in enumerate(self.xy_positions):
            x, y = position
            height, width = self.heights_widths[i]

            if direction == "<":
                if x - 1 < 0:
                    return True

                column = highpoints[x-1]
                for elevation in range(height):
                    if y+elevation < len(column) and column[y+elevation]:
                        return True

            else:
                if x + width > 6:
                    return True

                column = highpoints[x + width]
                for elevation in range(height):
                    try:
                        if y + elevation < len(column) and column[y + elevation]:
                            return True
                    except IndexError as e:
                        print(e)

        return False

    def move_side(self, direction) -> None:
        """Move the rock in direction."""
        delta = -1 if direction == "<" else 1
        for i in range(len(self.xy_positions)):
            self.xy_positions[i] = self.xy_positions[i][0] + delta, self.xy_positions[i][1]

    def move_down(self) -> None:
        """Move the rock down."""
        for i in range(len(self.xy_positions)):
            self.xy_positions[i] = self.xy_positions[i][0], self.xy_positions[i][1] - 1
            assert self.xy_positions[i][1] > 0


class RockOne(Rock):
    def __init__(self, highest_y):
        super().__init__(highest_y)
        self.heights_widths = ((1, 4),)  # -

        self.xy_positions = [(2, highest_y + 4)]


class RockTwo(Rock):
    def __init__(self, highest_y):
        super().__init__(highest_y)
        self.heights_widths = ((1, 3), (3, 1))  # +

        self.xy_positions = [
            (2, highest_y + 5),
            (3, highest_y + 4)
        ]


class RockThree(Rock):
    def __init__(self, highest_y):
        super().__init__(highest_y)
        self.heights_widths = ((1, 3), (2, 1))  # _|

        self.xy_positions = [
            (2, highest_y + 4),
            (4, highest_y + 5)
        ]


class RockFour(Rock):
    def __init__(self, highest_y):
        super().__init__(highest_y)
        self.heights_widths = ((4, 1),)  # |

        self.xy_positions = [(2, highest_y + 4)]


class RockFive(Rock):
    def __init__(self, highest_y):
        super().__init__(highest_y)
        self.heights_widths = ((2, 2),)  # ::

        self.xy_positions = [(2, highest_y + 4)]


def one(lines):
    directions = repeat(lines[0])
    highpoints = [[1] for _ in range(7)]

    for i, RockClass in enumerate(repeat([RockOne, RockTwo, RockThree, RockFour, RockFive])):

        # print(i)
        # for row in zip(*highpoints):
        #     print(row)

        rock = RockClass(calc_highest_y(highpoints))

        if i == 2022:
            break

        while True:

            direction = next(directions)
            if not rock.intersects_side(direction, highpoints):
                rock.move_side(direction)

            if rock.intersects_down(highpoints):
                combine(highpoints, rock)
                break
            else:
                rock.move_down()

    return calc_highest_y(highpoints)


def repeat(iterable):
    """Yield items from iterable forever."""
    while True:
        for x in iterable:
            yield x


def combine(highpoints, rock):
    """Combines a stopped rock with previous highpoints.

    :param highpoints: As for intersects()
    :param rock: A Rock
    """
    assert not highpoints[0] is highpoints[1]

    max_height = 0
    for i, position in enumerate(rock.xy_positions):
        x, y = position
        height, width = rock.heights_widths[i]
        if height + y > max_height:
            max_height = height+y

    # Make highpoints rectangular by padding with 0s
    for column in highpoints:
        if len(column) < max_height:
            column.extend([0]*(max_height - len(column)))

    for i, position in enumerate(rock.xy_positions):
        x, y = position
        height, width = rock.heights_widths[i]

        for j in range(width):
            for k in range(height):
                # assert highpoints[x+j][y+k] == 0
                highpoints[x+j][y+k] = 1


def two(lines):
    pass


def main():
    with open("../inputs/day17.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
