"""Tests for the day's solutions."""
import unittest
from aopy.b.day6 import one, two, winning_strategies


class TestOne(unittest.TestCase):
    def setUp(self) -> None:
        with open("./examples/b/day6.txt", encoding="utf-8") as f:
            self.content = [line.rstrip() for line in f]

    def test_example(self) -> None:
        expected = 288
        actual = one(self.content)
        self.assertEqual(expected, actual)

    def test_winning_strategies(self) -> None:
        expected = [2, 3, 4, 5]
        actual = winning_strategies((7, 9))
        self.assertEqual(expected, actual)

        expected = 8
        actual = len(winning_strategies((15, 40)))
        self.assertEqual(expected, actual)

        expected = 9
        actual = len(winning_strategies((30, 200)))
        self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def setUp(self) -> None:
        with open("./examples/b/day6.txt", encoding="utf-8") as f:
            self.content = [line.rstrip() for line in f]

    def test_example(self) -> None:
        expected = 71_503
        actual = two(self.content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
