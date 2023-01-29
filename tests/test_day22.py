import unittest
from unittest.mock import patch

from src.day22 import one, two, parse_instructions

with open("../examples/day22.txt", encoding="utf-8") as f:
    content = f.read()


class TestOne(unittest.TestCase):
    def test_example(self):

        expected = 6032
        actual = one(content)
        self.assertEqual(expected, actual)

    def test_parse_instructions(self):
        expected = [10, "R", 5, "L", 5, "R", 10, "L", 4, "L", 1]
        actual = parse_instructions("10R5L5R10L4L1")
        self.assertEqual(expected, actual)

    def test_one(self):
        with patch("src.day22.simulate") as mock_simulate:
            mock_simulate.return_value = (1, 2), "U"
            actual = one(content)
            expected = (1000 * 2) + (4 * 3) + 3
            self.assertEqual(expected, actual)

    # def test_make_col(self):
    #     expected = []
    #     actual = make_col()
    #     self.assertListEqual(expected, actual)


class TestTwo(unittest.TestCase):
    def test_example(self):

        expected = -1
        actual = two(content)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
