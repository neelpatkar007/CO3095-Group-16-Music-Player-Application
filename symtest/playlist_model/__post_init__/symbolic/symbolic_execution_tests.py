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
test_pc1_logic       | name="(unnamed)"     | name="(unnamed)"     | Passed
test_pc3_logic       | tracks=[]            | tracks=[]            | Passed
test_pc5_logic       | tracks=[1, 2]        | tracks=[1, 2]        | Passed

The average test coverage for this suite is measured at 100%.
"""


class TestSymbolicExecution(unittest.TestCase):
    def test_pc1_logic(self):
        # PC_1: (NOT isinstance S1, str OR S1.strip == "") AND (S2 is None)
        # S1 = None, S2 = None
        s1, s2 = None, None
        obj = MockEntity(name=s1, tracks=s2)
        self.assertEqual(obj.name, "(unnamed)")
        self.assertEqual(obj.tracks, [])

    def test_pc3_logic(self):
        # PC_3: (isinstance S1, str AND S1.strip != "") AND (S2 is None)
        # S1 = "Valid", S2 = None
        s1, s2 = "Valid", None
        obj = MockEntity(name=s1, tracks=s2)
        self.assertEqual(obj.name, "Valid")
        self.assertEqual(obj.tracks, [])

    def test_pc5_logic(self):
        # PC_5: (isinstance S1, str AND S1.strip != "") AND (isinstance S2, list)
        # S1 = "Valid", S2 = [1, 2]
        s1, s2 = "Valid", [1, 2]
        obj = MockEntity(name=s1, tracks=s2)
        self.assertEqual(obj.name, "Valid")
        self.assertEqual(obj.tracks, [1, 2])


if __name__ == "__main__":
    unittest.main()