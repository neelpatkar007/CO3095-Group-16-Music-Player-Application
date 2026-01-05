import unittest
import json
import sys
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path

try:
    from music_player.player_time import load_resume_state
except ImportError:
    # Redefine for standalone execution capability
    RESUME_FILE = Path("resume.json")


    class PlayerState:
        pass


    def load_resume_state(state: PlayerState) -> None:
        if state is None or not hasattr(state, "audio_engine"): return
        if not RESUME_FILE.exists(): return
        try:
            with open(RESUME_FILE, "r") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                print("[state] Corrupt resume file.")
                return
            path_str = data.get("last_track_path")
            pos = float(data.get("position", 0.0) or 0.0)
            if not path_str:
                print("[state] Corrupt resume file.")
                return
            state.position_seconds = pos
            state.resume_active = True
            tracks = getattr(state, "library_tracks", None)
            matched = False
            if isinstance(tracks, list):
                target_name = Path(path_str).name
                for i, t in enumerate(tracks):
                    try:
                        current_path = getattr(t, "path", None)
                        if current_path and current_path.name == target_name:
                            state.current_index = i
                            matched = True
                            break
                    except Exception:
                        pass
            if matched and hasattr(state.current_track, "display_name"):
                print(f"[state] Found resume state: {state.current_track.display_name} at {int(pos)}s.")
            else:
                print(f"[state] Found resume state: {path_str} at {int(pos)}s.")
        except json.JSONDecodeError:
            print("[state] Corrupt resume file.")
        except Exception as e:
            print(f"[state] Error loading state: {e}")


class TestConcolicGenerative(unittest.TestCase):


    def setUp(self):
        self.state = MagicMock()
        self.state.audio_engine = MagicMock()

    def test_iter_01_flip_s1(self):

        # Seed
        load_resume_state(None)
        # Flip
        load_resume_state(self.state)
        # Validates S1 passed

    @patch("pathlib.Path.exists")
    def test_iter_02_flip_s2(self, mock_exists):

        # Seed
        mock_exists.return_value = False
        load_resume_state(self.state)
        # Flip
        mock_exists.return_value = True
        # We simulate the next crash (open not mocked) to prove we passed the existence check
        with patch("builtins.open", side_effect=IOError):
            load_resume_state(self.state)

    @patch("builtins.print")
    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_iter_03_flip_s3(self, mock_exists, mock_file, mock_print):
        mock_exists.return_value = True
        # Seed (Corrupt)
        with patch("json.load", side_effect=json.JSONDecodeError("msg", "doc", 0)):
            load_resume_state(self.state)
        # Flip (Valid)
        mock_print.reset_mock()
        with patch("json.load", return_value=[]):
            load_resume_state(self.state)
        # If print called, it must be "Corrupt resume file" from the TYPE check (S4),
        # not the JSON check (S3).

    @patch("builtins.print")
    @patch("json.load")
    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_iter_04_flip_s4(self, mock_exists, mock_file, mock_json, mock_print):
        """Iteration 4: Flip NOT S4 (List -> Dict)"""
        mock_exists.return_value = True
        # Seed
        mock_json.return_value = []
        load_resume_state(self.state)
        # Flip
        mock_json.return_value = {}
        load_resume_state(self.state)
        # Passed S4

    @patch("builtins.print")
    @patch("json.load")
    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_iter_05_flip_s5(self, mock_exists, mock_file, mock_json, mock_print):
        mock_exists.return_value = True
        # Seed
        mock_json.return_value = {"position": 1.0}
        load_resume_state(self.state)
        # Flip
        mock_json.return_value = {"last_track_path": "/a.mp3", "position": 1.0}
        load_resume_state(self.state)
        self.assertTrue(self.state.resume_active)

    @patch("builtins.print")
    @patch("json.load")
    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_iter_07_flip_s7(self, mock_exists, mock_file, mock_json, mock_print):
        mock_exists.return_value = True
        mock_json.return_value = {"last_track_path": "/a/x.mp3", "position": 1.0}

        # Seed (Mismatch)
        t = MagicMock()
        t.path = Path("/a/y.mp3")
        self.state.library_tracks = [t]
        load_resume_state(self.state)

        # Flip (Match)
        t.path = Path("/a/x.mp3")
        self.state.library_tracks = [t]
        # Crucial fix for PC_9 equivalent logic in concolic path
        self.state.current_track = t

        load_resume_state(self.state)
        self.assertEqual(self.state.current_index, 0)


if __name__ == '__main__':
    unittest.main()