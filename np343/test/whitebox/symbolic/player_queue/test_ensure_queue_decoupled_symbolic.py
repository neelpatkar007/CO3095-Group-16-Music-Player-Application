import unittest
from types import SimpleNamespace
from music_player.player_queue import _ensure_queue_decoupled


class TestSymbolicExecution(unittest.TestCase):

    def test_pc1_missing_attrs(self):
        state_a = SimpleNamespace(library_tracks=[1, 2])
        _ensure_queue_decoupled(state_a)
        self.assertFalse(hasattr(state_a, "tracks"))

        state_b = SimpleNamespace(tracks=[1, 2])
        _ensure_queue_decoupled(state_b)
        self.assertEqual(state_b.tracks, [1, 2])

    def test_pc2_lib_copy(self):
        lib = [1, 2, 3]
        state = SimpleNamespace(tracks=lib, library_tracks=lib)

        self.assertIs(state.tracks, state.library_tracks)

        _ensure_queue_decoupled(state)

        self.assertEqual(state.tracks, [1, 2, 3])
        self.assertIsNot(state.tracks, state.library_tracks)
        self.assertIsNot(state.tracks, lib)

    def test_pc3_lib_invalid_type(self):
        invalid_lib = 12345
        state = SimpleNamespace(tracks=invalid_lib, library_tracks=invalid_lib)

        _ensure_queue_decoupled(state)

        self.assertEqual(state.tracks, [])

    def test_pc4_no_playlists_or_no_match(self):
        current_queue = [10, 20]
        lib = [1, 2]

        state = SimpleNamespace(tracks=current_queue, library_tracks=lib)
        _ensure_queue_decoupled(state)
        self.assertIs(state.tracks, current_queue)

        pl1 = SimpleNamespace(tracks=[99, 99])
        state_with_pl = SimpleNamespace(
            tracks=current_queue,
            library_tracks=lib,
            playlists=[pl1]
        )
        _ensure_queue_decoupled(state_with_pl)
        self.assertIs(state_with_pl.tracks, current_queue)

    def test_pc5_playlist_match(self):
        pl_tracks = [5, 5, 5]
        pl1 = SimpleNamespace(tracks=pl_tracks)
        lib = [1, 2]

        state = SimpleNamespace(
            tracks=pl_tracks,
            library_tracks=lib,
            playlists=[pl1]
        )

        self.assertIs(state.tracks, pl1.tracks)

        _ensure_queue_decoupled(state)

        self.assertEqual(state.tracks, [5, 5, 5])
        self.assertIsNot(state.tracks, pl1.tracks)


if __name__ == '__main__':
    unittest.main()