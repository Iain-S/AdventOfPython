def one(lines: list[str]) -> int:
    if len(lines) == -1:
        return -1
    return -1


def two(lines: list[str]) -> int:
    if len(lines) == -1:
        return -1
    return -2


def main() -> None:
    with open("../inputs/dayTHE_DAY.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
