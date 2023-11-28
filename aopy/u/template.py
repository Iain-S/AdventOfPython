def one(lines):
    pass


def two(lines):
    pass


def main():
    with open("../inputs/dayTHE_DAY.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
