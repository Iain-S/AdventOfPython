"""Tests for the day's solutions."""
import unittest
from aopy.b.day0 import one, two


class TestOne(unittest.TestCase):
    def setUp(self) -> None:
        with open("./examples/b/day6.txt", encoding="utf-8") as f:
            self.content = [line.rstrip() for line in f]

    def test_example(self) -> None:
        expected = -1
        actual = one(self.content)
        self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def setUp(self) -> None:
        with open("./examples/b/day6.txt", encoding="utf-8") as f:
            self.content = [line.rstrip() for line in f]

    def test_example(self) -> None:
        expected = -2
        actual = two(self.content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
