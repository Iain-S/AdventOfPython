def text_to_stacks(starting_text):
    """Convert the header text to a list of lists."""
    starting_lines = starting_text.split("\n")[::-1]

    # The last col tells us how many empty stacks to initialise
    stacks = [[] for _ in range(int(starting_lines[0][-2]))]

    # The blocks are padded with whitespace so we get " " where there is no crate
    for line in starting_lines[1:]:
        for i, c in enumerate(line[1::4]):
            if c != " ":
                stacks[i].append(c)

    return stacks


def rearrange(lines, mover_function):
    starting_state, moves = lines.split("\n\n")

    stacks = text_to_stacks(starting_state)

    for move in moves.split("\n"):
        if move:
            words = move.split(" ")
            how_many, from_stack_idx, to_stack_idx = (int(x) for x in words[1::2])
            mover_function(
                how_many, stacks[from_stack_idx - 1], stacks[to_stack_idx - 1]
            )

    return "".join([stack[-1] for stack in stacks])


def one(lines):
    def crate_mover(how_many, from_stack, to_stack):

        if how_many == 0:
            return

        to_stack.append(from_stack.pop())
        crate_mover(how_many - 1, from_stack, to_stack)

    return rearrange(lines, crate_mover)


def two(lines):
    def crate_mover_9001(how_many, from_stack, to_stack):

        if how_many == 0:
            return

        temp = []
        for _ in range(how_many):
            temp.append(from_stack.pop())

        to_stack.extend(temp[::-1])

    return rearrange(lines, crate_mover_9001)


def main():
    with open("../../AoC_2022/src/inputs/05.txt") as f:
        lines = f.read()
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
