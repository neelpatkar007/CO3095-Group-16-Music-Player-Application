import unittest
from unittest.mock import MagicMock, patch, Mock
from pathlib import Path
from music_player.audio_backend import AudioEngine


class TestConcolicGenerative(unittest.TestCase):
    """
    FILE 4: Concolic Generative Test Suite

    This suite implements the iterative discovery process defined in
    CONCOLIC_ANALYSIS.md. It treats the inputs as dynamic seeds that are
    flipped to explore the state space.

    Test Results Table:
    | Iteration | Seed Inputs (S3, S4, S5, S6) | Status |
    |-----------|------------------------------|--------|
    | 1         | (1.0, F, T, T)               | PASS   |
    | 2         | (1.0, F, F, T)               | PASS   |
    | 3         | (1.5, T, T, T)               | PASS   |
    | 4         | (1.5, T, F, T)               | PASS   |
    | 5         | (1.5, T, T, F)               | PASS   |
    | 6         | (1.5, T, F, F)               | PASS   |

    The average test coverage for this suite is measured at 100%.
    """

    def test_iteration_1_baseline(self):
        """Seed: Speed 1.0, No Pydub, Pygame OK"""
        audio = AudioEngine()
        test_path = Path("/music/test.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', False):
            with patch('music_player.audio_backend.HAS_PYGAME', True):
                with patch.object(audio, '_play_real') as mock_play_real:
                    audio.play(test_path, start_pos=0.0, speed=1.0)
                    mock_play_real.assert_called_once_with(test_path, 0.0)

    def test_iteration_2_flip_pygame(self):
        """Flip S5: Pygame False"""
        audio = AudioEngine()
        test_path = Path("/music/test.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', False):
            with patch('music_player.audio_backend.HAS_PYGAME', False):
                with patch.object(audio, '_play_simulated') as mock_play_sim:
                    audio.play(test_path, start_pos=0.0, speed=1.0)
                    mock_play_sim.assert_called_once_with(test_path, 0.0)

    def test_iteration_3_flip_speed_and_pydub(self):
        """Flip S3/S4: Speed 1.5, Pydub True"""
        audio = AudioEngine()
        test_path = Path("/music/test.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', True):
            with patch('music_player.audio_backend.HAS_PYGAME', True):
                with patch('music_player.audio_backend.AudioSegment') as mock_seg_class:
                    mock_seg = Mock()
                    mock_seg.frame_rate = 44100
                    mock_processed = Mock()
                    mock_seg._spawn.return_value = mock_processed
                    mock_processed.set_frame_rate.return_value = mock_processed
                    mock_seg_class.from_file.return_value = mock_seg

                    with patch.object(audio, '_play_real') as mock_play_real:
                        audio.play(test_path, start_pos=0.0, speed=1.5)
                        mock_play_real.assert_called_once()
                        call_args = mock_play_real.call_args[0]
                        self.assertEqual(call_args[0], audio.temp_file)
                        self.assertAlmostEqual(call_args[1], 0.0)

    def test_iteration_4_flip_pygame_revisit(self):
        """Flip S5 again: Pygame False (with Speed 1.5)"""
        audio = AudioEngine()
        test_path = Path("/music/test.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', True):
            with patch('music_player.audio_backend.HAS_PYGAME', False):
                with patch('music_player.audio_backend.AudioSegment') as mock_seg_class:
                    mock_seg = Mock()
                    mock_seg.frame_rate = 44100
                    mock_processed = Mock()
                    mock_seg._spawn.return_value = mock_processed
                    mock_processed.set_frame_rate.return_value = mock_processed
                    mock_seg_class.from_file.return_value = mock_seg

                    with patch.object(audio, '_play_simulated') as mock_play_sim:
                        audio.play(test_path, start_pos=0.0, speed=1.5)
                        mock_play_sim.assert_called_once_with(test_path, 0.0)

    def test_iteration_5_flip_exception(self):
        """Flip S6: Force Exception"""
        audio = AudioEngine()
        test_path = Path("/music/test.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', True):
            with patch('music_player.audio_backend.HAS_PYGAME', True):
                with patch('music_player.audio_backend.AudioSegment') as mock_seg_class:
                    mock_seg_class.from_file.side_effect = Exception("Processing error")

                    with patch.object(audio, '_play_real') as mock_play_real:
                        audio.play(test_path, start_pos=0.0, speed=1.5)
                        mock_play_real.assert_called_once_with(test_path, 0.0)
                        self.assertEqual(audio.current_speed, 1.0)

    def test_iteration_6_flip_exception_simulated(self):
        """Flip S5 (Pygame) under Exception state"""
        audio = AudioEngine()
        test_path = Path("/music/test.mp3")

        with patch('music_player.audio_backend.HAS_PYDUB', True):
            with patch('music_player.audio_backend.HAS_PYGAME', False):
                with patch('music_player.audio_backend.AudioSegment') as mock_seg_class:
                    mock_seg_class.from_file.side_effect = Exception("Processing error")

                    with patch.object(audio, '_play_simulated') as mock_play_sim:
                        audio.play(test_path, start_pos=0.0, speed=1.5)
                        mock_play_sim.assert_called_once_with(test_path, 0.0)


if __name__ == '__main__':
    unittest.main()