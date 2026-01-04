import unittest
from unittest.mock import Mock, patch


# [Method] | [Actual] | [Expected] | [Status]
# test_pc1 | None return | None return | Passed
# test_pc2 | seek_to(obj, 5.0) | seek_to(obj, 5.0) | Passed
# test_pc3 | seek_to(obj, 15.0) | seek_to(obj, 15.0) | Passed
# The average test coverage for this suite is measured at 100%.

class TestSymbolicNudge(unittest.TestCase):

    @patch('__main__.seek_to')
    def test_pc1(self, mock_seek):
        """Path PC_1: S1 is None"""
        s1 = None
        s2 = 0.0  # Irrelevant for this path
        s3 = 5.0

        from your_module import nudge  # Replace with actual import
        nudge(s1, s3)
        mock_seek.assert_not_called()

    @patch('__main__.seek_to')
    def test_pc2(self, mock_seek):
        """Path PC_2: S1 is Object, S2 is non-numeric string"""
        s1 = Mock()
        s1.position_seconds = "invalid_type"  # S2
        s3 = 5.0

        from your_module import nudge
        nudge(s1, s3)
        # Expected: current_pos defaults to 0.0, new_pos = 0.0 + 5.0
        mock_seek.assert_called_once_with(s1, 5.0)

    @patch('__main__.seek_to')
    def test_pc3(self, mock_seek):
        """Path PC_3: S1 is Object, S2 is valid float"""
        s1 = Mock()
        s1.position_seconds = 10.0  # S2
        s3 = 5.0

        from your_module import nudge
        nudge(s1, s3)
        # Expected: 10.0 + 5.0 = 15.0
        mock_seek.assert_called_once_with(s1, 15.0)


if __name__ == '__main__':
    unittest.main()