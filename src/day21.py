from functools import cache


def get_func(monkeys):
    @cache
    def monkey_shouts(monkey_name):
        try:
            return int(monkeys[monkey_name])
        except ValueError:
            monkey_one, operator, monkey_two = monkeys[monkey_name].split(" ")
            value_one = monkey_shouts(monkey_one)
            value_two = monkey_shouts(monkey_two)
            return eval(
                "{a} {x} {b}".format(a=str(value_one), x=operator, b=str(value_two))
            )

    return monkey_shouts


def one(lines):
    monkeys = {k: v for k, v in [line.split(": ") for line in lines]}
    return get_func(monkeys)("root")


def two(lines):
    pass


def main():
    with open("../inputs/day21.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
