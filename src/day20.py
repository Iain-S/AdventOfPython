def one(lines):
    length = len(lines)
    indexes = [x for x in range(length)]
    values = [int(x) for x in lines]

    for i in range(length):
        index = indexes.index(i)
        value = values[index]

        try:
            move_right(indexes, index, value)
            move_right(values, index, value)
        except AssertionError as e:
            print(e)

    return calc_coords(values)


def calc_coords(numbers):
    zero_index = numbers.index(0)
    result = 0
    for x in (1_000, 2_000, 3_000):
        index = (zero_index + x) % (len(numbers))
        result += numbers[index]

    return result


def move_right(a_list, i, spaces):
    """Move what is currently at index i spaces to the right."""
    new_index = ((i + spaces) % (len(a_list)-1))

    new_index = len(a_list) -1 if new_index == 0 else new_index

    x = a_list.pop(i)
    a_list.insert(new_index, x)


def two(lines):
    pass


def main():
    with open("../inputs/day20.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
