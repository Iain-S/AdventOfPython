"""Tests for the day's solutions."""
import unittest
from aopy.b.day18 import (
    one,
    two,
    dig_interior,
    dig_loop,
    walk_loop,
    get_area,
    intersects,
    point_in_rect,
    split_rect,
    split_range,
    calc_bounding_rect,
)


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

        self.two_loop = [
            ((0, 0), (2, 0)),
            ((2, 0), (2, 2)),
            ((2, 2), (0, 2)),
            ((0, 2), (0, 0)),
        ]

    def test_example(self) -> None:
        expected = 952_408_144_115
        actual = two(self.content)
        self.assertEqual(expected, actual)

    def test_walk_loop(self) -> None:
        actual = walk_loop(
            [
                ("R", 2),
                ("D", 2),
                ("L", 2),
                ("U", 2),
            ]
        )
        expected = self.two_loop
        self.assertListEqual(expected, actual)

        actual = walk_loop(
            [
                ("U", 50),
                ("U", 50),
                ("L", 100),
                ("D", 100),
                ("R", 100),
            ]
        )
        expected = [
            ((0, 0), (0, -50)),
            ((0, -50), (0, -100)),
            ((0, -100), (-100, -100)),
            ((-100, -100), (-100, 0)),
            ((-100, 0), (0, 0)),
        ]
        self.assertListEqual(expected, actual)

    def test_get_area(self):
        expected = 0
        actual = get_area([], tuple())
        self.assertEqual(expected, actual)

        loop = self.two_loop
        rect = ((0, 0), (1, 1))
        expected = 1
        actual = get_area(loop, rect)
        self.assertEqual(expected, actual)

    def test_intersects(self):
        # rect is inside the loop
        actual = intersects(self.two_loop, ((1, 1), (1, 1)))
        self.assertFalse(actual)

        # rect and loop overlap
        actual = intersects(self.two_loop, ((1, 1), (3, 3)))
        self.assertTrue(actual)

        # section of loop passes through horizontally
        actual = intersects([((0, 2), (8, 2))], ((1, 1), (3, 3)))
        self.assertTrue(actual)

        # section of loop passes through vertically
        actual = intersects([((2, -10), (2, 5))], ((1, 1), (3, 3)))
        self.assertTrue(actual)

    def test_point_in_rect(self):
        self.assertTrue(point_in_rect((0, 0), ((0, 0), (1, 1))))

        self.assertFalse(point_in_rect((-1, -1), ((0, 0), (1, 1))))

    def test_split_rect(self):
        expected = (
            ((0, 0), (0, 0)),
            ((1, 0), (1, 0)),
            ((1, 1), (1, 1)),
            ((0, 1), (0, 1)),
        )
        actual = split_rect(((0, 0), (1, 1)))
        self.assertTupleEqual(expected, actual)

        expected = (
            ((2, 7), (2, 7)),
            ((3, 7), (4, 7)),
            ((3, 8), (4, 9)),
            ((2, 8), (2, 9)),
        )

        actual = split_rect(((2, 7), (4, 9)))
        self.assertTupleEqual(expected, actual)

        expected = (
            ((1, 8), (1, 8)),
            ((2, 8), (2, 8)),
        )

        actual = split_rect(((1, 8), (2, 8)))
        self.assertTupleEqual(expected, actual)

        expected = (
            ((-27, -126), (-27, -126)),
            ((-27, -125), (-27, -125)),
        )

        actual = split_rect(((-27, -126), (-27, -125)))
        self.assertTupleEqual(expected, actual)

        return
        # todo unit rectangle
        with self.assertRaises(RuntimeError):
            split_rect(((0, 0), (0, 0)))

    def test_split_range(self) -> None:
        expected = ((0, 1), (2, 3))
        actual = split_range(0, 3)
        self.assertTupleEqual(expected, actual)

        expected = ((2, 3), (4, 6))
        actual = split_range(2, 6)
        self.assertTupleEqual(expected, actual)

        expected = ((-3, -2), (-1, 0))
        actual = split_range(-3, 0)
        self.assertTupleEqual(expected, actual)

    def test_rect_in_loop(self) -> None:
        pass

    def test_bounding_rect(self) -> None:
        expected = ((-1, -1), (3, 3))
        actual = calc_bounding_rect(self.two_loop)
        self.assertTupleEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
