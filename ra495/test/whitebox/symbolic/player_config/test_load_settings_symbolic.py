import unittest
from unittest.mock import MagicMock, patch, mock_open
from music_player.player_config import load_settings

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock()
        self.state.volume = 0
        self.state.shuffle_active = False
        self.state.loop_mode = "off"
        self.state.playback_speed = 1.0
        self.state.song_tags = {}
        self.state.total_play_time = 0.0
        self.state.audio_engine = MagicMock()

    @patch('pathlib.Path.exists')
    def test_pc1_file_missing(self, mock_exists):
        mock_exists.return_value = False
        load_settings(self.state)
        self.state.audio_engine.set_volume.assert_not_called()

    @patch('builtins.open')
    @patch('pathlib.Path.exists')
    def test_pc2_exception(self, mock_exists, mock_file):
        mock_exists.return_value = True
        mock_file.side_effect = IOError("Disk Error")
        load_settings(self.state)
        self.state.audio_engine.set_volume.assert_not_called()

    @patch('json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.exists')
    def test_pc3_happy_path(self, mock_exists, mock_file, mock_json):
        mock_exists.return_value = True
        mock_json.return_value = {
            "volume": 50,
            "shuffle": True,
            "loop": "one",
            "speed": 1.5,
            "tags": {"genre": "jazz"},
            "total_time": 120.0
        }

        load_settings(self.state)

        self.assertEqual(self.state.volume, 50)
        self.assertEqual(self.state.shuffle_active, True)
        self.assertEqual(self.state.loop_mode, "one")
        self.assertEqual(self.state.playback_speed, 1.5)
        self.assertEqual(self.state.song_tags, {"genre": "jazz"})
        self.assertEqual(self.state.total_play_time, 120.0)

    @patch('json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.exists')
    def test_pc4_type_failures(self, mock_exists, mock_file, mock_json):
        mock_exists.return_value = True
        mock_json.return_value = {
            "volume": "loud",
            "shuffle": 1,
            "loop": 123,
            "speed": "fast",
            "tags": [],
            "total_time": "ten"
        }

        load_settings(self.state)

        self.assertEqual(self.state.volume, 100)
        self.assertEqual(self.state.shuffle_active, False)
        self.assertEqual(self.state.loop_mode, "off")
        self.assertEqual(self.state.playback_speed, 1.0)
        self.assertEqual(self.state.song_tags, {})
        self.assertEqual(self.state.total_play_time, 0.0)

    @patch('json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.exists')
    def test_pc5_range_failures(self, mock_exists, mock_file, mock_json):
        mock_exists.return_value = True
        mock_json.return_value = {
            "volume": 150,
            "shuffle": True,
            "loop": "random",
            "speed": 3.0,
            "tags": {},
            "total_time": -10.0
        }

        load_settings(self.state)

        self.assertEqual(self.state.volume, 100)
        self.assertEqual(self.state.loop_mode, "all")
        self.assertEqual(self.state.playback_speed, 1.0)
        self.assertEqual(self.state.total_play_time, 0.0)


if __name__ == '__main__':
    unittest.main()