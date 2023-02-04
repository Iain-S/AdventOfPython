import unittest
from src.day24 import one, two, simulate, string_to_valley, valley_to_string, in_bounds

with open("../examples/day24.txt", encoding="utf-8") as f:
    content = f.read()


class TestOne(unittest.TestCase):
    def test_example(self):
        expected = -1
        actual = one(content)
        self.assertEqual(expected, actual)

    def test_simulate(self):
        valley = string_to_valley(
            "#.#####\n"
            "#.....#\n"
            "#>....#\n"
            "#.....#\n"
            "#...v.#\n"
            "#.....#\n"
            "#####.#"
        )

        out = simulate(valley, 1)
        actual = valley_to_string(out)
        expected = (
            "#.#####\n"
            "#.....#\n"
            "#.>...#\n"
            "#.....#\n"
            "#.....#\n"
            "#...v.#\n"
            "#####.#"
        )
        self.assertEqual(expected, actual)

        out = simulate(valley, 5)
        actual = valley_to_string(out)
        expected = (
            "#.#####\n"
            "#.....#\n"
            "#>....#\n"
            "#.....#\n"
            "#...v.#\n"
            "#.....#\n"
            "#####.#"
        )
        self.assertEqual(expected, actual)

    def test_string_to_valley(self):
        example = (
            "#.#####\n"
            "#.....#\n"
            "#....>#\n"
            "#...v.#\n"
            "#.....#\n"
            "#.....#\n"
            "#####.#"
        )
        expected = [
            [
                ".",
                ".",
                ".",
                ".",
                ".",
            ],
            [
                ".",
                ".",
                ".",
                ".",
                [">"],
            ],
            [
                ".",
                ".",
                ".",
                ["v"],
                ".",
            ],
            [
                ".",
                ".",
                ".",
                ".",
                ".",
            ],
            [
                ".",
                ".",
                ".",
                ".",
                ".",
            ],
        ]
        actual = string_to_valley(example)
        self.assertListEqual(expected, actual)

        expected = example
        actual = valley_to_string(actual)
        self.assertEqual(expected, actual)

        valley = [[["<",">"]]]
        expected = (
            "#.#\n"
            "#2#\n"
            "#.#"
        )
        actual = valley_to_string(valley)
        self.assertEqual(expected, actual)

    def test_in_bounds(self):
        valley = string_to_valley(content)

        self.assertTrue(in_bounds(valley, 0,0))
        self.assertTrue(in_bounds(valley, 3,0))
        self.assertTrue(in_bounds(valley, 0,0))
        self.assertTrue(in_bounds(valley, 0,5))

        self.assertFalse(in_bounds(valley, -1,0))
        self.assertFalse(in_bounds(valley, 4,0))
        self.assertFalse(in_bounds(valley, 0,-1))
        self.assertFalse(in_bounds(valley, 0,6))

class TestTwo(unittest.TestCase):
    def test_example(self):
        with open("../examples/day24.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = -1
        actual = two(content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
