moves = {
    "R": complex(1, 0),
    "L": complex(-1, 0),
    "U": complex(0, 1),
    "D": complex(0, -1),
}


def one(lines):
    tail = complex(0, 0)
    head = complex(0, 0)
    visited = set()

    for line in lines:
        direction, steps = line.split(" ")
        move = moves[direction]

        for _ in range(int(steps)):
            head = head + move
            to_head = head - tail

            distance = abs(to_head)
            if distance < 2:
                # One step away
                continue

            elif distance == 2:
                # Two steps vertically or horizontally
                tail += to_head/2

            else:
                # Somewhat diagonal
                real = to_head.real * (0.5 if abs(to_head.real) == 2 else 1)
                imag = to_head.imag * (0.5 if abs(to_head.imag) == 2 else 1)
                tail += complex(real, imag)

            visited.add(tail)

    return len(visited) + 1


def two(lines):
    pass


def main():
    with open("../inputs/day9.txt") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
