import unittest
from aopy.b.day1 import one, two


class TestOne(unittest.TestCase):
    def test_example(self) -> None:
        with open("./examples/b/day1.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = -1
        actual = one(content)
        self.assertEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def test_example(self) -> None:
        with open("./examples/b/day1.txt", encoding="utf-8") as f:
            content = [line.rstrip() for line in f]

        expected = -2
        actual = two(content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
