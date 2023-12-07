"""Tests for the day's solutions."""
import unittest
from aopy.b.day7 import one, two, parse, rank, rank_two, comparator_two


class TestOne(unittest.TestCase):
    def setUp(self) -> None:
        with open("./examples/b/day7.txt", encoding="utf-8") as f:
            self.content = [line.rstrip() for line in f]

    def test_example(self) -> None:
        expected = 6440
        actual = one(self.content)
        self.assertEqual(expected, actual)

    def test_parse(self) -> None:
        actual = parse(self.content)
        self.assertEqual(5, len(actual[0]))
        self.assertEqual(5, len(actual[1]))
        self.assertEqual(483, actual[1][4])
        self.assertEqual("QQQJA", actual[0][4])

    def test_rank(self) -> None:
        expected = [
            "32T3K",
            "KTJJT",
            "KK677",
            "T55J5",
            "QQQJA",
        ]
        actual = rank(
            [
                "32T3K",
                "T55J5",
                "KK677",
                "KTJJT",
                "QQQJA",
            ]
        )
        self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def setUp(self) -> None:
        with open("./examples/b/day7.txt", encoding="utf-8") as f:
            self.content = [line.rstrip() for line in f]

    def test_example(self) -> None:
        expected = 5905
        actual = two(self.content)
        self.assertEqual(expected, actual)

    def test_rank_two(self) -> None:
        expected = [
            "32T3K",
            "KK677",
            "T55J5",
            "QQQJA",
            "KTJJT",
        ]
        actual = rank_two(
            [
                "32T3K",
                "T55J5",
                "KK677",
                "KTJJT",
                "QQQJA",
            ]
        )
        self.assertEqual(expected, actual)

        expected = ["JKKK2", "QQQQ2"]
        actual = rank_two(["QQQQ2", "JKKK2"])
        self.assertEqual(expected, actual)

    def test_comparitor_two(self) -> None:
        expected = -1
        actual = comparator_two("JKKK2", "QQQQ2")
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
