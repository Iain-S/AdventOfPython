from aopy.b.day0 import something
from unittest import TestCase


class TestModule(TestCase):
    def test_something(self) -> None:
        result = something()
        self.assertEqual("1.0.0", result)
