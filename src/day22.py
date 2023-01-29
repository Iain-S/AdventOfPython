from itertools import chain


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

NOT_EMTPY = (".", "#", ">", "<", "^", "v")


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
            if direction in ("R", "L"):
                row = board_map[pos[0]]

                if direction == "R":
                    for _ in range(instruction):
                        if pos[1] + 1 >= len(row):
                            # wrap around
                            x = min([row.index(z) for z in NOT_EMTPY if z in row])
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
                    for _ in range(instruction):
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

                # column = [board_map[i][pos[1]] for i in range(above, below+1)]
                column = [c[pos[1]] for c in board_map[above : below + 1]]

                if column[0] == " " or column[-1] == " ":
                    print("error!")

                r_pos = pos[0] - above, pos[1]

                if direction == "D":
                    for _ in range(instruction):
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
                    for _ in range(instruction):
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


def two(content):
    pass


def main():
    with open("../inputs/day22.txt", encoding="utf-8") as f:
        content = f.read()
    print("one:", one(content))
    print("two:", two(content))


if __name__ == "__main__":
    main()
