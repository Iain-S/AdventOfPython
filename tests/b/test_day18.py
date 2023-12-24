"""Tests for the day's solutions."""
import unittest
from aopy.b.day18 import one, two, dig_interior, dig_loop


class TestOne(unittest.TestCase):
    def setUp(self) -> None:
        with open("../../examples/b/day18.txt", encoding="utf-8") as f:
            self.content = [line.rstrip() for line in f]

    def test_example(self) -> None:
        expected = 62
        actual = one(self.content)
        self.assertEqual(expected, actual)

    def test_dig_loop(self) -> None:
        expected = [
            "#######",
            "#.....#",
            "###...#",
            "..#...#",
            "..#...#",
            "###.###",
            "#...#..",
            "##..###",
            ".#....#",
            ".######",
        ]
        actual = dig_loop(self.content)
        self.assertEqual(expected, actual)

    def test_dig_interior(self) -> None:
        expected = [
            "#######",
            "#######",
            "#######",
            "..#####",
            "..#####",
            "#######",
            "#####..",
            "#######",
            ".######",
            ".######",
        ]
        actual = dig_interior(dig_loop(self.content))
        self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def setUp(self) -> None:
        with open("../../examples/b/day18.txt", encoding="utf-8") as f:
            self.content = [line.rstrip() for line in f]

    def test_example(self) -> None:
        expected = 952_408_144_115
        actual = two(self.content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
