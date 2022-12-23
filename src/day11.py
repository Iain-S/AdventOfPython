class Monkey:
    def __init__(self, items, operation, test, if_true, if_false):
        self.troupe = []
        self.items = items
        self.operation = operation
        self.test = test
        self.if_true = if_true
        self.if_false = if_false
        self.items_inspected = 0

    def join_troupe(self, troupe):
        self.troupe = troupe

    def take_turn(self):
        while len(self.items):
            self.items_inspected += 1

            item = self.items.pop(0)
            item = self.operation(item)
            item //= 3
            send_to = self.if_true if self.test(item) else self.if_false
            self.troupe[send_to].receive(item)

    def receive(self, item):
        self.items.append(item)

    def __eq__(self, other):
        return (
            self.troupe == other.troupe
            and self.items == other.items
            and self.operation(10) == other.operation(10)
            and self.operation(110) == other.operation(110)
            and self.if_true == other.if_true
            and self.if_false == other.if_false
        )


def parse_monkey(text):
    num, items_line, op_line, test_line, true_line, false_line, *_ = text.split("\n")

    # e.g. Starting items: 79, 98
    items = [int(x) for x in items_line[items_line.index(":") + 1 :].split(",")]

    # e.g. Operation: new = old * 19
    index = op_line.index("=")
    op = eval("lambda old: " + op_line[index + 1 :])

    # e.g. Test: divisible by 23
    index = test_line.index("divisible by")
    divisor = int(test_line[index + 12 :])
    test = lambda x: x % divisor == 0

    # e.g. If true: throw to monkey 2
    index = true_line.index("throw to monkey")
    if_true = int(true_line[index + 15 :])

    # e.g. If true: throw to monkey 2
    index = false_line.index("throw to monkey")
    if_false = int(false_line[index + 15 :])

    zero = Monkey(items, op, test, if_true, if_false)
    return zero


def one(text):
    troupe = []
    for monkey_text in text.split("Monkey "):

        if monkey_text:
            troupe.append(parse_monkey(monkey_text))

    for monkey in troupe:
        monkey.join_troupe(troupe)

    for i in range(20):
        for monkey in troupe:
            monkey.take_turn()

    most_inspected = sorted([m.items_inspected for m in troupe])[-2:]
    return most_inspected[0] * most_inspected[1]


def two(lines):
    pass


def main():
    with open("../inputs/day11.txt") as f:
        lines = f.read()
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
