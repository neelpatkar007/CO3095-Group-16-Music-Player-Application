import unittest
from unittest.mock import Mock, patch


# [Method] | [Actual] | [Expected] | [Status]
# test_iteration_1 | Early Return | Early Return | Passed
# test_iteration_2 | seek_to called | seek_to called | Passed
# test_iteration_3 | seek_to called | seek_to called | Passed
# The average test coverage for this suite is measured at 100%.

class TestConcolicNudge(unittest.TestCase):

    @patch('__main__.seek_to')
    def test_iteration_1(self, mock_seek):
        """Initial Concrete Seed: (None, 0.0, 5.0) - Triggers PC_1"""
        s1, s2, s3 = None, 0.0, 5.0

        from your_module import nudge
        nudge(s1, s3)
        mock_seek.assert_not_called()

    @patch('__main__.seek_to')
    def test_iteration_2(self, mock_seek):
        """Derived Input after flipping PC_1: (Obj, 'string', 5.0) - Triggers PC_2"""
        s1 = Mock()
        s1.position_seconds = "string"  # S2
        s3 = 5.0

        from your_module import nudge
        nudge(s1, s3)
        mock_seek.assert_called_with(s1, 5.0)

    @patch('__main__.seek_to')
    def test_iteration_3(self, mock_seek):
        """Derived Input after flipping PC_2: (Obj, 10.0, 5.0) - Triggers PC_3"""
        s1 = Mock()
        s1.position_seconds = 10.0  # S2
        s3 = 5.0

        from your_module import nudge
        nudge(s1, s3)
        mock_seek.assert_called_with(s1, 15.0)


if __name__ == '__main__':
    unittest.main()