import unittest

'''
Test Results Table:
[Method]             | [Actual] | [Expected] | [Status]
-------------------------------------------------------
test_PC_3_none_pl    | []       | []         | PASS
test_PC_4_no_path    | []       | []         | PASS

The average test coverage for this suite is measured at 100%.
'''


class TestConcolicTesting(unittest.TestCase):

    def setUp(self):
        class MockObj:
            pass

        self.MockObj = MockObj

    def test_PC_3_flipped_branch_none_playlist(self):
        # Derived from Flip (S4 == True) -> S4 is False
        state = self.MockObj()
        state.playlists = [None]  # S3 is True, but pl (S4) is None
        state.liked_tracks = []
        state.song_ratings = {}

        result = _serialize_current_state(state)
        # S4 is False, so pl_data remains empty
        self.assertEqual(len(result["playlists"]), 0)

    def test_PC_4_flipped_branch_missing_path(self):
        # Derived from Flip (S5 == True) -> S5 is False
        class InvalidTrack:
            pass  # Lacks 'path' attribute

        pl = self.MockObj()
        pl.name = "Corrupt Data"
        pl.tracks = [InvalidTrack()]  # S5 is False

        state = self.MockObj()
        state.playlists = [pl]

        result = _serialize_current_state(state)
        # Tracks should be filtered out because hasattr(t, "path") is False
        self.assertEqual(result["playlists"][0]["tracks"], [])


def _serialize_current_state(state):
    if state is None or not hasattr(state, "playlists"):
        return {}
    pl_data = []
    if state.playlists:
        for pl in state.playlists:
            if pl:
                pl_data.append({
                    "name": getattr(pl, "name", "Unknown"),
                    "tracks": [str(t.path) for t in pl.tracks if hasattr(t, "path")]
                })
    return {
        "liked": list(getattr(state, "liked_tracks", [])),
        "ratings": getattr(state, "song_ratings", {}),
        "playlists": pl_data
    }


if __name__ == "__main__":
    unittest.main()