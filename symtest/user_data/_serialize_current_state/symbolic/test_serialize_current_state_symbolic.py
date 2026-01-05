import unittest
from dataclasses import dataclass
from typing import List, Any
from music_player.user_data import _serialize_current_state

@dataclass
class Track:
    path: str


@dataclass
class Playlist:
    name: str
    tracks: List[Track]


@dataclass
class PlayerState:
    playlists: List[Playlist]
    liked_tracks: List[str]
    song_ratings: dict

class TestSymbolicExecution(unittest.TestCase):

    def test_PC_1_null_state(self):
        result = _serialize_current_state(None)
        self.assertEqual(result, {})

    def test_PC_2_empty_playlists(self):
        s1 = PlayerState(playlists=[], liked_tracks=[], song_ratings={})
        result = _serialize_current_state(s1)
        self.assertEqual(result["playlists"], [])

    def test_PC_5_full_serialization(self):
        t1 = Track(path="/vol/music/01.mp3")
        pl1 = Playlist(name="Favourites", tracks=[t1])
        s1 = PlayerState(playlists=[pl1], liked_tracks=["Track 1"], song_ratings={"Track 1": 4})

        result = _serialize_current_state(s1)

        self.assertEqual(result["playlists"][0]["name"], "Favourites")
        self.assertEqual(result["playlists"][0]["tracks"], ["/vol/music/01.mp3"])
        self.assertEqual(result["liked"], ["Track 1"])


if __name__ == "__main__":
    unittest.main()