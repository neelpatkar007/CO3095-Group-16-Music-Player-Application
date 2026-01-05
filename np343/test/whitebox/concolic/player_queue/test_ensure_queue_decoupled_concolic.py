import unittest
from types import SimpleNamespace
from music_player.player_queue import _ensure_queue_decoupled



class TestConcolicGenerative(unittest.TestCase):

    def test_iteration_1_early_return(self):

        state = SimpleNamespace(library_tracks=[])

        _ensure_queue_decoupled(state)

        self.assertFalse(hasattr(state, "tracks"))

    def test_iteration_2_no_match_fallthrough(self):
        unique_queue = [100]
        pl_tracks = [200]
        playlist = SimpleNamespace(tracks=pl_tracks)

        state = SimpleNamespace(
            tracks=unique_queue,
            library_tracks=[],
            playlists=[playlist]
        )

        _ensure_queue_decoupled(state)

        self.assertIs(state.tracks, unique_queue)

    def test_iteration_3_playlist_match(self):
        shared_tracks = [300]
        playlist = SimpleNamespace(tracks=shared_tracks)

        state = SimpleNamespace(
            tracks=shared_tracks,
            library_tracks=[],
            playlists=[playlist]
        )

        _ensure_queue_decoupled(state)

        self.assertIsNot(state.tracks, playlist.tracks)
        self.assertEqual(state.tracks, [300])

    def test_iteration_4_library_standard(self):

        shared_lib = [400, 500]
        state = SimpleNamespace(
            tracks=shared_lib,
            library_tracks=shared_lib
        )

        _ensure_queue_decoupled(state)

        self.assertIsNot(state.tracks, state.library_tracks)
        self.assertEqual(state.tracks, [400, 500])

    def test_iteration_5_library_edge_case(self):
        sentinel = object()
        state = SimpleNamespace(
            tracks=sentinel,
            library_tracks=sentinel
        )

        _ensure_queue_decoupled(state)

        self.assertEqual(state.tracks, [])


if __name__ == '__main__':
    unittest.main()