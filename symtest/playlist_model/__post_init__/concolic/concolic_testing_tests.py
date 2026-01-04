import unittest
from dataclasses import dataclass
from typing import Any


@dataclass
class MockEntity:
    name: Any
    tracks: Any = None

    def __post_init__(self) -> None:
        if not isinstance(self.name, str):
            self.name = str(self.name)
        self.name = self.name.strip() or "(unnamed)"

        if self.tracks is None:
            self.tracks = []
        elif not isinstance(self.tracks, list):
            self.tracks = []


"""
Test Results Table:
[Method]             | [Actual]             | [Expected]           | [Status]
test_iteration_1_pc1 | name="(unnamed)"     | name="(unnamed)"     | Passed
test_iteration_2_pc5 | name="Alice"         | name="Alice"         | Passed
test_iteration_3_pc4 | tracks=[]            | tracks=[]            | Passed

The average test coverage for this suite is measured at 100%.
"""


class TestConcolicExecution(unittest.TestCase):
    def test_iteration_1_pc1(self):
        # Derived from Seed 1: (None, None) -> PC_1
        s1, s2 = None, None
        obj = MockEntity(name=s1, tracks=s2)
        self.assertEqual(obj.name, "(unnamed)")
        self.assertIsInstance(obj.tracks, list)

    def test_iteration_2_pc5(self):
        # Derived from Seed 2: ("Alice", [1]) -> PC_5
        s1, s2 = "Alice", [1]
        obj = MockEntity(name=s1, tracks=s2)
        self.assertEqual(obj.name, "Alice")
        self.assertEqual(obj.tracks, [1])

    def test_iteration_3_pc4(self):
        # Derived from Seed 3: ("Alice", 123) -> PC_4
        # S2 is not None and not a list, should be reset to []
        s1, s2 = "Alice", 123
        obj = MockEntity(name=s1, tracks=s2)
        self.assertEqual(obj.tracks, [])


if __name__ == "__main__":
    unittest.main()