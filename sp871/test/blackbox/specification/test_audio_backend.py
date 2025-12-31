import unittest
from unittest.mock import MagicMock, patch, ANY
from pathlib import Path
from music_player import audio_backend
from music_player.audio_backend import AudioEngine


class TestAudioBackendSpecification(unittest.TestCase):
    """
    Black-Box Specification-based Testing for audio_backend.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Category Partition Method
    """

    def setUp(self):
        self.dummy_path = Path("song.mp3")

    # Simulated Environment (No Pygame)

    @patch("music_player.audio_backend.HAS_PYGAME", False)
    def test_simulated_workflow(self):
        """
        Expected Result:
        - play sets state to playing and prints simulated message.
        - pause sets state to paused and prints simulated message.
        - resume sets state to playing and prints simulated message.
        - stop resets state and prints simulated message.
        Actual Result: PASSED [100%]
        """
        engine = AudioEngine()

        # Play
        with patch("builtins.print") as mock_print:
            engine.play(self.dummy_path)
            self.assertTrue(engine.playing)
            self.assertFalse(engine.paused)
            self.assertEqual(engine.current_path, self.dummy_path)
            # falls back to simulated mode
            mock_print.assert_called_with(f"[audio] PLAY (simulated) {self.dummy_path.name} from 0.0s")

        # Pause
        with patch("builtins.print") as mock_print:
            engine.pause()
            self.assertFalse(engine.playing)
            self.assertTrue(engine.paused)
            mock_print.assert_called_with("[audio] PAUSE (simulated)")

        # Resume
        with patch("builtins.print") as mock_print:
            engine.resume()
            self.assertTrue(engine.playing)
            self.assertFalse(engine.paused)
            mock_print.assert_called_with("[audio] RESUME (simulated)")

        # Stop
        with patch("builtins.print") as mock_print:
            engine.stop()
            self.assertFalse(engine.playing)
            self.assertFalse(engine.paused)
            mock_print.assert_called_with("[audio] STOP (simulated)")

    @patch("music_player.audio_backend.HAS_PYGAME", False)
    def test_simulated_seek(self):
        """
        Expected Result: Seek updates state and prints simulated message.
        Actual Result: PASSED [100%]
        """
        engine = AudioEngine()
        engine.current_path = self.dummy_path

        with patch("builtins.print") as mock_print:
            engine.seek(30.0)
            # Update internal state
            self.assertTrue(engine.playing)
            self.assertFalse(engine.paused)
            mock_print.assert_called_with("[audio] SEEK (simulated) -> 30.0s")

    # Real Environment (Pygame)

    @patch("music_player.audio_backend.HAS_PYGAME", True)
    @patch("music_player.audio_backend.pygame")
    def test_real_playback_calls(self, mock_pygame):
        """
        Expected Result: Methods delegate to pygame.mixer.music functions.
        Actual Result: PASSED [100%][audio] PLAY (real) song.mp3 from 0.0s (Speed: 1.0x)
        """
        engine = AudioEngine()

        # Setup mock
        mock_mixer = mock_pygame.mixer.music

        # Play
        engine.play(self.dummy_path)
        mock_mixer.load.assert_called_with(str(self.dummy_path))
        mock_mixer.play.assert_called_with(loops=0, start=0.0)

        # Set Volume
        engine.set_volume(50)
        mock_mixer.set_volume.assert_called_with(0.5)

        # Pause
        engine.pause()
        mock_mixer.pause.assert_called()

        # Resume
        engine.resume()
        mock_mixer.unpause.assert_called()

        # Stop
        engine.stop()
        mock_mixer.stop.assert_called()

    @patch("music_player.audio_backend.HAS_PYGAME", True)
    @patch("music_player.audio_backend.pygame")
    def test_real_seek(self, mock_pygame):
        """
        Expected Result: Seek reloads file and plays from new timestamp.
        Actual Result: PASSED [100%][audio] SEEK -> 15.0s
        """
        engine = AudioEngine()
        engine.current_path = self.dummy_path

        engine.seek(15.0)

        mock_pygame.mixer.music.load.assert_called_with(str(self.dummy_path))
        mock_pygame.mixer.music.play.assert_called_with(loops=0, start=15.0)

    # Feature Interaction

    @patch("music_player.audio_backend.HAS_PYGAME", True)
    @patch("music_player.audio_backend.pygame")
    def test_mute_logic(self, mock_pygame):
        """
        Expected Result:
        - Mute sets pygame volume to 0.
        - Play while muted keeps volume at 0.
        Actual Result: PASSED [100%][audio] PLAY (real) song.mp3 from 0.0s (Speed: 1.0x)
        """
        engine = AudioEngine()
        mock_mixer = mock_pygame.mixer.music

        # Toggle Mute On
        engine.set_muted(True)
        self.assertTrue(engine.muted)
        mock_mixer.set_volume.assert_called_with(0.0)

        # Play while muted
        engine.play(self.dummy_path)
        # Should set volume to 0 again
        mock_mixer.set_volume.assert_called_with(0.0)

    # Speed Change (Pydub)

    @patch("music_player.audio_backend.HAS_PYGAME", True)
    @patch("music_player.audio_backend.HAS_PYDUB", True)
    @patch("music_player.audio_backend.AudioSegment")
    @patch("music_player.audio_backend.pygame")
    def test_speed_change_processing(self, mock_pygame, mock_segment):
        """
        Expected Result:
        - If speed != 1.0, AudioSegment processes file.
        - Playback uses temporary file.
        - Start position is adjusted.
        Actual Result:
            PASSED [100%][audio] Processing audio for 1.5x speed... (this may take a moment)
            [audio] PLAY (real) temp_speed_audio.mp3 from 10.0s (Speed: 1.5x)
        """
        engine = AudioEngine()

        # Mock AudioSegment chain
        mock_seg_instance = MagicMock()
        mock_segment.from_file.return_value = mock_seg_instance
        mock_seg_instance.frame_rate = 44100
        # _spawn return
        mock_processed = MagicMock()
        mock_seg_instance._spawn.return_value = mock_processed
        # set_frame_rate return
        mock_final = MagicMock()
        mock_processed.set_frame_rate.return_value = mock_final

        # Test 1.5x speed
        start_time = 15.0
        speed = 1.5
        engine.play(self.dummy_path, start_pos=start_time, speed=speed)

        # Verify Pydub usage
        mock_segment.from_file.assert_called_with(self.dummy_path)
        mock_final.export.assert_called()  # Should export to temp file

        # Verify Pygame loads temp file
        expected_load_path = str(Path("temp_speed_audio.mp3"))
        mock_pygame.mixer.music.load.assert_called_with(expected_load_path)

        # Verify Start Position Adjusted
        mock_pygame.mixer.music.play.assert_called_with(loops=0, start=10.0)

    @patch("music_player.audio_backend.HAS_PYGAME", True)
    @patch("music_player.audio_backend.HAS_PYDUB", False)  # Pydub missing
    @patch("music_player.audio_backend.pygame")
    def test_speed_change_fallback(self, mock_pygame):
        """
        Expected Result: If Pydub missing, falls back to normal playback.
        Actual Result: PASSED [100%][audio] PLAY (real) song.mp3 from 10.0s (Speed: 1.5x)
        """
        engine = AudioEngine()

        engine.play(self.dummy_path, start_pos=10.0, speed=1.5)

        # Should load the original file, not the temp file
        mock_pygame.mixer.music.load.assert_called_with(str(self.dummy_path))
        # Should play from original start time
        mock_pygame.mixer.music.play.assert_called_with(loops=0, start=10.0)

    # Edge Cases

    def test_init_state(self):
        """
        Expected Result: Default values are correct.
        Actual Result: PASSED [100%]
        """
        engine = AudioEngine()
        self.assertFalse(engine.playing)
        self.assertFalse(engine.paused)
        self.assertEqual(engine.volume, 100)
        self.assertIsNone(engine.current_path)

    @patch("music_player.audio_backend.HAS_PYGAME", False)
    def test_transitions_safety(self):
        """
        Expected Result: Pause/Resume/Stop do nothing if state is invalid.
        Actual Result: PASSED [100%]
        """
        engine = AudioEngine()

        # Pause when stopped
        engine.pause()
        self.assertFalse(engine.paused)

        # Resume when playing
        engine.playing = True
        engine.resume()  # Already playing
        # No change
        self.assertTrue(engine.playing)

        # Stop when already stopped
        engine.playing = False
        engine.stop()
        self.assertFalse(engine.playing)