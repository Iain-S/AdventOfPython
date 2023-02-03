import unittest
from src.day23 import one, two, Elf, display_elves, double_grove, calc_score


class TestOne(unittest.TestCase):
    def test_example(self):
        with open("../examples/day23.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = 110
        actual = one(content)
        self.assertEqual(expected, actual)

    def test_double_grove(self):
        expected = [[]]
        actual = double_grove([[]])
        self.assertListEqual(expected, actual)

    def test_calc_score(self):
        expected = 110
        grove = [
            [".", ".", ".", ".", ".", ".", "#", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", "."],
            [".", "#", ".", "#", ".", ".", "#", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", "#", ".", ".", ".", ".", ".", "."],
            [".", ".", "#", ".", ".", ".", ".", ".", "#", ".", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", "#", "#", ".", ".", "."],
            [".", ".", ".", ".", "#", "#", ".", ".", ".", ".", ".", "."],
            [".", "#", ".", ".", ".", ".", ".", ".", ".", ".", "#", "."],
            [".", ".", ".", "#", ".", "#", ".", ".", "#", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", "#", ".", ".", "#", ".", ".", "#", ".", "."],
        ]
        actual = calc_score(grove)
        self.assertEqual(expected, actual)

    def test_simulate(self):
        with open("../examples/day23.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        one(content)

    def test_display_elves(self):
        elf = Elf(0, 0)
        expected = ["#"]
        actual = display_elves([elf])
        self.assertListEqual(expected, actual)

        expected = ["##"]
        actual = display_elves([Elf(-1, 1), Elf(-1, 0)])
        self.assertListEqual(expected, actual)

        expected = ["#", "#"]
        actual = display_elves([Elf(-1, 1), Elf(0, 1)])
        self.assertListEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day23.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = -1
        actual = two(content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
