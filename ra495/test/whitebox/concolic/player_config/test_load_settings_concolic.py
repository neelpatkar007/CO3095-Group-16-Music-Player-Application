import unittest
from unittest.mock import MagicMock, patch, mock_open
import json
from music_player.player_config import load_settings

class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock()
        self.state.volume = 0
        self.state.shuffle_active = False
        self.state.loop_mode = "off"
        self.state.playback_speed = 1.0
        self.state.song_tags = {}
        self.state.total_play_time = 0.0
        self.state.audio_engine = MagicMock()

    def run_concolic_iteration(self, input_seed):
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('builtins.open', new_callable=mock_open, read_data=json.dumps(input_seed)) as mock_file, \
                patch('json.load', return_value=input_seed):
            mock_exists.return_value = True
            load_settings(self.state)

    def test_iter1_base_seed(self):
        seed = {
            "volume": 50, "shuffle": True, "loop": "one",
            "speed": 1.0, "tags": {}, "total_time": 10.0
        }
        self.run_concolic_iteration(seed)
        self.assertEqual(self.state.volume, 50)
        self.assertEqual(self.state.loop_mode, "one")

    def test_iter2_flip_vol_type(self):
        seed = {"volume": "invalid", "shuffle": True}
        self.run_concolic_iteration(seed)
        self.assertEqual(self.state.volume, 100)

    def test_iter3_flip_vol_range(self):
        seed = {"volume": 150, "shuffle": True}
        self.run_concolic_iteration(seed)
        self.assertEqual(self.state.volume, 100)

    def test_iter4_flip_shuff_type(self):
        seed = {"shuffle": 1}
        self.run_concolic_iteration(seed)
        self.assertEqual(self.state.shuffle_active, False)

    def test_iter5_flip_loop_type(self):
        seed = {"loop": False}
        self.run_concolic_iteration(seed)
        self.assertEqual(self.state.loop_mode, "off")

    def test_iter6_flip_loop_val(self):
        seed = {"loop": "unknown"}
        self.run_concolic_iteration(seed)
        self.assertEqual(self.state.loop_mode, "all")

    def test_iter7_flip_speed_type(self):
        seed = {"speed": "fast"}
        self.run_concolic_iteration(seed)
        self.assertEqual(self.state.playback_speed, 1.0)

    def test_iter8_flip_speed_range(self):
        seed = {"speed": 3.0}
        self.run_concolic_iteration(seed)
        self.assertEqual(self.state.playback_speed, 1.0)

    def test_iter9_flip_tags_type(self):
        seed = {"tags": []}
        self.run_concolic_iteration(seed)
        self.assertEqual(self.state.song_tags, {})

    def test_iter10_flip_time_type(self):
        seed = {"total_time": "long"}
        self.run_concolic_iteration(seed)
        self.assertEqual(self.state.total_play_time, 0.0)

    def test_iter11_flip_time_neg(self):
        seed = {"total_time": -5.0}
        self.run_concolic_iteration(seed)
        self.assertEqual(self.state.total_play_time, 0.0)


if __name__ == '__main__':
    unittest.main()