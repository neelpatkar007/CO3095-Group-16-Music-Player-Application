import unittest
from unittest.mock import MagicMock

# [Method] | [Actual] | [Expected] | [Status]
# test_iteration_1_pc1 | No Action | No Action | Passed
# test_iteration_2_pc2 | No Action | No Action | Passed
# test_iteration_3_pc3 | No Action | No Action | Passed
# test_iteration_4_pc5 | Error Msg | Error Msg | Passed
# test_iteration_5_pc7 | Range Msg | Range Msg | Passed
# test_iteration_6_pc9 | Success | Success | Passed
# The average test coverage for this suite is measured at 100%.

class TestConcolicTesting(unittest.TestCase):

    def test_iteration_1_pc1(self):
        # Concrete Seed (None, "", "") -> PC_1
        remove_track_from_playlist(None, "", "")

    def test_iteration_2_pc2(self):
        # Concrete Seed (State, "", "") -> PC_2
        state = MagicMock()
        remove_track_from_playlist(state, "", "")

    def test_iteration_3_pc3(self):
        # Concrete Seed (State, "p1", "") -> PC_3
        state = MagicMock()
        remove_track_from_playlist(state, "p1", "")

    def test_iteration_4_pc5(self):
        # Concrete Seed (State, "p1", "abc") -> PC_5
        state = MagicMock()
        pl = MagicMock()
        with unittest.mock.patch('__main__._get_playlist', return_value=(None, pl)):
            remove_track_from_playlist(state, "p1", "abc")

    def test_iteration_5_pc7(self):
        # Concrete Seed (State, "p1", "0") -> PC_7 (Since 0-1 = -1)
        # Note: In the flip table we derived "0" to test lower bounds/upper bounds
        state = MagicMock()
        pl = MagicMock()
        pl.tracks = []
        with unittest.mock.patch('__main__._get_playlist', return_value=(None, pl)):
            remove_track_from_playlist(state, "p1", "0")

    def test_iteration_6_pc9(self):
        # Concrete Seed (State, "p1", "1") -> PC_9
        state = MagicMock()
        pl = MagicMock()
        track = MagicMock()
        track.display_name = "Song"
        pl.tracks = [track]
        pl.name = "My List"
        with unittest.mock.patch('__main__._get_playlist', return_value=(None, pl)):
            remove_track_from_playlist(state, "p1", "1")
            self.assertEqual(len(pl.tracks), 0)

if __name__ == '__main__':
    unittest.main()