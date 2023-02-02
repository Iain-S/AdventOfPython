from itertools import chain

testing = False

def split_on(a_string, char):
    b = a_string.split(char)
    c = list(chain(*[[b[0]]] + [[char, x] for x in b[1:]]))
    return c


def parse_instructions(instruction_string):
    a = split_on(instruction_string, "R")
    b = list(chain(*[split_on(x, "L") for x in a]))
    for i in range(len(b)):
        try:
            b[i] = int(b[i])
        except ValueError:
            pass

    return b


ROTATIONS = {
    "RR": "D",
    "RL": "U",
    "DR": "L",
    "DL": "R",
    "LR": "U",
    "LL": "D",
    "UR": "R",
    "UL": "L",
}

ARROWS = {
    "R": ">",
    "D": "v",
    "U": "^",
    "L": "<",
}

FACING_VALUES = {
    "R": 0,
    "D": 1,
    "L": 2,
    "U": 3,
}

NOT_EMPTY = (".", "#", ">", "<", "^", "v")

DIM = 50

def one(content):
    a, b = content.split("\n\n")
    board_map = [list(line) for line in a.split("\n")]
    instructions = parse_instructions(b)

    last_position, last_facing = simulate(board_map, instructions)

    [print("".join(x)) for x in board_map]

    rownum = last_position[0] + 1
    colnum = last_position[1] + 1
    facing_val = FACING_VALUES[last_facing]
    return (1000 * rownum) + (4 * colnum) + facing_val


def simulate(board_map, instructions):
    pos = 0, board_map[0].index(".")  # y, x from top left
    direction = "R"
    board_map[pos[0]][pos[1]] = ARROWS[direction]

    for i_inst, instruction in enumerate(instructions):
        if isinstance(instruction, str):
            direction = ROTATIONS[direction + instruction]
            board_map[pos[0]][pos[1]] = ARROWS[direction]
        else:
            for _ in range(instruction):
                if direction in ("R", "L"):
                    row = board_map[pos[0]]

                    if direction == "R":
                        if pos[1] + 1 >= len(row):
                            # wrap around
                            x = min([row.index(z) for z in NOT_EMPTY if z in row])
                        else:
                            x = pos[1] + 1

                        next_pos = pos[0], x
                        tile_to_right = row[x]
                        if tile_to_right == "#":
                            # stop
                            break
                        else:
                            # move right
                            pos = next_pos
                            board_map[pos[0]][pos[1]] = ARROWS[direction]
                    else:
                        # Left
                        if pos[1] - 1 < 0 or row[pos[1] - 1] == " ":
                            # wrap around
                            x = len(row) - 1
                        else:
                            x = pos[1] - 1

                        next_pos = pos[0], x
                        tile_to_left = row[x]
                        if tile_to_left == "#":
                            # stop
                            break
                        else:
                            # move left
                            pos = next_pos
                            board_map[pos[0]][pos[1]] = ARROWS[direction]
                else:
                    # Up or Down
                    above = pos[0]
                    while True:
                        if above - 1 < 0 or board_map[above - 1][pos[1]] == " ":
                            break
                        else:
                            above -= 1

                    below = pos[0]
                    while True:
                        if (
                            below + 1 >= len(board_map)
                            or pos[1] >= len(board_map[below + 1])
                            or board_map[below + 1][pos[1]] == " "
                        ):
                            break
                        else:
                            below += 1

                    column = [c[pos[1]] for c in board_map[above : below + 1]]

                    if column[0] == " " or column[-1] == " ":
                        print("error!")

                    r_pos = pos[0] - above, pos[1]

                    if direction == "D":
                        if r_pos[0] + 1 >= len(column):
                            # wrap around
                            y = 0
                        else:
                            y = r_pos[0] + 1

                        next_r_pos = y, r_pos[1]
                        # try:
                        tile_below = column[y]
                        # except IndexError:
                        #     pass
                        if tile_below == "#":
                            # stop
                            break
                        else:
                            # move down
                            r_pos = next_r_pos
                            board_map[r_pos[0] + above][r_pos[1]] = ARROWS[direction]

                    else:
                        # Up
                        if r_pos[0] - 1 < 0:
                            # wrap around

                            # here
                            y = len(column) - 1
                        else:
                            y = r_pos[0] - 1

                        next_r_pos = y, r_pos[1]
                        tile_above = column[y]
                        if tile_above == "#":
                            # stop
                            break
                        else:
                            # move up
                            r_pos = next_r_pos
                            board_map[r_pos[0] + above][r_pos[1]] = ARROWS[direction]

                    pos = r_pos[0] + above, r_pos[1]

    return pos, direction

def make_seams():
    pass

def myrange(pointa,pointb):
    # inclusive ranges in either direction
    if pointa[0] == pointb[0]:
        # horizontal
        x = pointa[1]
        y = pointb[1]
        a = pointa[0]

        return [(a, j) for j in (range(x, y + 1) if y > x else range(x, y-1, -1))]
    else:
        # vertical
        x = pointa[0]
        y = pointb[0]
        a = pointa[1]
        return [(j, a) for j in (range(x, y + 1) if y > x else range(x, y-1, -1))]

def make_seam(first, second):
    inverse = {
        "U": "D",
        "D": "U",
        "L": "R",
        "R": "L",
    }
    j = myrange(first[0], first[1])
    k = myrange(second[0], second[1])
    assert len(j) == len(k), f"{j}, {k}"

    result = {}
    for i in range(len(j)):
        result[(j[i], first[2])] = (k[i], second[2])

    for i in range(len(j)):
        result[(k[i], inverse[second[2]])] = (j[i], inverse[first[2]])

    return result

def new_direction_pos(direction, pos):
    # change direction and y,x position
    if testing:
        seams = {}
        if direction == "R":
            if 0 <= pos[0] <= 3:
                direction = "L"
                pos = 8 + 3 - pos[0], 15

            elif 4 <= pos[0] <= 7:
                direction = "D"
                # pos = 8, pos[0]-7+12
                # pos = 8, 16 - (8 - pos[0])
                pos = 8, 15 - (pos[0]-4)

            elif 8 <= pos[0] <= 11:
                direction = "L"
                pos = 3 - (pos[0] - 8), 11

            else:
                assert False, pos

        elif direction == "L":
            if 0 <= pos[0] <= 3:
                direction = "D"
                pos = 4, pos[0] + 4

            elif 4 <= pos[0] <= 7:
                direction = "U"
                pos = 11, 12 + ( 8 - pos[0])

            elif 8 <= pos[0] <= 11:
                direction = "U"
                pos = 7, 7 - (pos[0]-8)

            else:
                assert False, pos

        elif direction == "U":
            if 0 <= pos[1] <= 3:
                direction = "D"
                pos = 0, 11-pos[1]
            elif 4 <= pos[1] <= 7:
                direction = "R"
                pos = pos[1]-4, 8
            elif 8 <= pos[1] <= 11:
                direction = "D"
                pos = 4, 8 - (pos[1] - 8)
            elif 12 <= pos[1] <= 15:
                direction = "L"
                pos = 11 - (pos[1] - 12), 11
            else:
                assert False, pos

        else:
            # Down
            if 0 <= pos[1] <= 3:
                direction = "U"
                pos = 11, 11-pos[1]
            elif 4 <= pos[1] <= 7:
                direction = "R"
                pos = 7, 11 - (pos[1]-4)
            elif 8 <= pos[1] <= 11:
                direction = "U"
                pos = 7, 3-(pos[1]-8)
            elif 12 <= pos[1] <= 15:
                direction = "R"
                pos = 4 + (pos[1]-12), 0
            else:
                assert False, pos

    else:
        # not testing
        dim = 5
        if direction == "R":
            if 0 <= pos[0] <= dim-1:
                direction = "L"
                pos = (3*dim) - 1 - pos[0], (dim*2)-1
            elif dim <= pos[0] <= (2*dim)-1:
                direction = "U"
                pos = dim-1, (2*dim) + (pos[0]-dim)
            elif 2*dim <= pos[0] <= (3*dim)-1:
                direction = "L"
                pos = dim-(pos[0]-(2*dim))-1, (3*dim)-1
            else:
                # todo
                direction = ""
                pass


        elif direction == "L":
            pass
        elif direction == "D":
            pass
        else:
            # Up
            pass

    return direction, pos

def walk_edge(board_map, direction, pos):
    pass

def is_edge(board_map, pos):
    if pos[0] == 0 or pos[0] == len(board_map) - 1:
        return True
    elif pos[1] == 0 or pos[1] == len(board_map[pos[0]]) - 1:
        return True
    else:
        if " " in (board_map[pos[0]-1][pos[1]], board_map[pos[0]+1][pos[1]], board_map[pos[0]][pos[1]-1], board_map[pos[0]][pos[1]+1]):
            return True
        else:
            return False

def new_direction_pos_two(board_map, direction, pos):
    # change direction and y,x position

    r_direction = ROTATIONS[direction+"R"]
    r_pos = pos
    rotation = 90

    for _ in range(DIM):
        if r_direction == "L":
            if r_pos[1]-1 >= 0 and board_map[r_pos[0]][r_pos[1]-1] in NOT_EMPTY:
                # move forward
                r_pos = r_pos[0], r_pos[1] - 1

                if not is_edge(board_map, r_pos):
                    # must be at an inner corner
                    if False:
                        pass



            # elif new_l_pos[1] < 0 or board_map[new_l_pos[0]][new_l_pos[1]] == " ":
            else:

                # turn right
                pass


        elif r_direction == "R":
            pass

        elif r_direction == "U":
            pass

        else:
            # Down
            pass


    return direction, pos


def simulate_two(board_map, instructions):
    pos = 0, board_map[0].index(".")  # y, x from top left
    direction = "R"
    board_map[pos[0]][pos[1]] = ARROWS[direction]

    for i_inst, instruction in enumerate(instructions):
        if isinstance(instruction, str):
            direction = ROTATIONS[direction + instruction]
            board_map[pos[0]][pos[1]] = ARROWS[direction]
        else:
            for _ in range(instruction):
                if direction in ("R", "L"):
                    row = board_map[pos[0]]

                    if direction == "R":
                        if pos[1] + 1 >= len(row):
                            # wrap around
                            next_direction, next_pos = new_direction_pos(direction, pos)
                            if board_map[next_pos[0]][next_pos[1]] == "#":
                                # stop
                                break
                            else:
                                pos = next_pos
                                direction = next_direction
                                board_map[pos[0]][pos[1]] = ARROWS[direction]
                        else:
                            x = pos[1] + 1
                            next_pos = pos[0], x
                            tile_to_right = row[x]

                            if tile_to_right == "#":
                                # stop
                                break
                            else:
                                # move right
                                pos = next_pos
                                board_map[pos[0]][pos[1]] = ARROWS[direction]
                    else:
                        # Left
                        if pos[1] - 1 < 0 or row[pos[1] - 1] == " ":
                            # wrap around
                            next_direction, next_pos = new_direction_pos(direction, pos)
                            if board_map[next_pos[0]][next_pos[1]] == "#":
                                # stop
                                break
                            else:
                                pos = next_pos
                                direction = next_direction
                                board_map[pos[0]][pos[1]] = ARROWS[direction]
                        else:
                            x = pos[1] - 1

                            next_pos = pos[0], x
                            tile_to_left = row[x]
                            if tile_to_left == "#":
                                # stop
                                break
                            else:
                                # move left
                                pos = next_pos
                                board_map[pos[0]][pos[1]] = ARROWS[direction]
                else:
                    # Up or Down
                    above = pos[0]
                    while True:
                        if above - 1 < 0 or len(board_map[above-1]) < pos[1] or board_map[above - 1][pos[1]] == " ":
                            break
                        else:
                            above -= 1

                    below = pos[0]
                    while True:
                        if (
                                below + 1 >= len(board_map)
                                or pos[1] >= len(board_map[below + 1])
                                or board_map[below + 1][pos[1]] == " "
                        ):
                            break
                        else:
                            below += 1

                    column = [c[pos[1]] for c in board_map[above : below + 1]]

                    if column[0] == " " or column[-1] == " ":
                        print("error!")

                    r_pos = pos[0] - above, pos[1]

                    if direction == "D":
                        if r_pos[0] + 1 >= len(column):
                            # wrap around
                            next_direction, next_pos = new_direction_pos(direction, pos)
                            if board_map[next_pos[0]][next_pos[1]] == "#":
                                # stop
                                break
                            else:
                                pos = next_pos
                                direction = next_direction
                                board_map[pos[0]][pos[1]] = ARROWS[direction]
                        else:
                            y = r_pos[0] + 1

                            next_r_pos = y, r_pos[1]
                            tile_below = column[y]
                            if tile_below == "#":
                                # stop
                                break
                            else:
                                # move down
                                r_pos = next_r_pos
                                board_map[r_pos[0] + above][r_pos[1]] = ARROWS[direction]

                            pos = r_pos[0] + above, r_pos[1]

                    else:
                        # Up
                        if r_pos[0] - 1 < 0:
                            # wrap around
                            next_direction, next_pos = new_direction_pos(direction, pos)
                            if board_map[next_pos[0]][next_pos[1]] == "#":
                                # stop
                                break
                            else:
                                pos = next_pos
                                direction = next_direction
                                board_map[pos[0]][pos[1]] = ARROWS[direction]
                        else:
                            y = r_pos[0] - 1

                            next_r_pos = y, r_pos[1]
                            tile_above = column[y]
                            if tile_above == "#":
                                # stop
                                break
                            else:
                                # move up
                                r_pos = next_r_pos
                                board_map[r_pos[0] + above][r_pos[1]] = ARROWS[direction]

                            pos = r_pos[0] + above, r_pos[1]

    return pos, direction


class Cube:
    def __init__(self,
                 front_face,
                 left_face,
                 right_face,
                 back_face,
                 top_face,
                 bottom_face):
        pass

    def walk(self, instructions):
        pass




def two(content):
    a, b = content.split("\n\n")
    board_map = [list(line) for line in a.split("\n")]
    instructions = parse_instructions(b)

    last_position, last_facing = simulate_two(board_map, instructions)

    [print("".join(x)) for x in board_map]

    rownum = last_position[0] + 1
    colnum = last_position[1] + 1
    facing_val = FACING_VALUES[last_facing]
    return (1000 * rownum) + (4 * colnum) + facing_val


def main():
    with open("../inputs/day22.txt", encoding="utf-8") as f:
        content = f.read()
    print("one:", one(content))
    print("two:", two(content))


if __name__ == "__main__":
    main()
