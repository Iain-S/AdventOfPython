"""Tests for the day's solutions."""
import unittest
from aopy.b.day13 import one, two, get_patterns, find_reflections


class TestBOne(unittest.TestCase):
    def setUp(self) -> None:
        with open("./examples/b/day13.txt", encoding="utf-8") as f:
            self.content = [line.rstrip() for line in f]

        self.patterns = get_patterns(self.content)

    def test_example(self) -> None:
        expected = 405
        actual = one(self.content)
        self.assertEqual(expected, actual)

    def test_find_reflection(self) -> None:
        expected = ("v", 5)
        actual = find_reflections(self.patterns[0])[0]
        self.assertTupleEqual(expected, actual)

        expected = ("h", 4)
        actual = find_reflections(self.patterns[1])[0]
        self.assertTupleEqual(expected, actual)

    def test_get_patterns(self) -> None:
        expected = (["abc", "def"], ["ghi", "jkl"])
        actual = get_patterns(["abc", "def", "", "ghi", "jkl"])
        self.assertTupleEqual(expected, actual)


class TestBTwo(unittest.TestCase):
    def setUp(self) -> None:
        with open("./examples/b/day13.txt", encoding="utf-8") as f:
            self.content = [line.rstrip() for line in f]

    def test_example(self) -> None:
        expected = 400
        actual = two(self.content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
