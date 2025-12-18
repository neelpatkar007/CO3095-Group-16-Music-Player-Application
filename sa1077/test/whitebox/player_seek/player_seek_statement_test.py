import pytest

from music_player.player_state import PlayerState
from music_player.audio_backend import AudioEngine
from music_player.library import Track
from music_player.player_seek import get_progress, seek_to, nudge
from music_player.time_utils import format_mm_ss


def make_state_with_track(duration: float = 180.0) -> PlayerState:
    """Utility factory to initialise a consistent PlayerState for statement-level coverage analysis."""
    engine = AudioEngine()
    track = Track(
        path=None,  # type: ignore[arg-type]
        title="Test",
        artist="Tester",
        duration_seconds=duration,
    )
    state = PlayerState(tracks=[track], audio_engine=engine)
    state.current_index = 0
    state.position_seconds = 0.0
    return state

class TestGetProgressStatement:
    def test_stmt_get_progress_with_valid_track(self):
        """
                Statement Test S1: Standard Execution Path.
                Executes the main lines of get_progress to ensure successful retrieval
                of current position and total duration from a valid track object.
                """
        state = make_state_with_track(200.0)
        state.position_seconds = 42.0

        pos, total = get_progress(state)

        assert pos == 42.0
        assert total == 200.0


class TestSeekToStatement:
    def test_stmt_seek_to_seconds_in_range(self, capsys):
        """
                Statement Test S2: Numeric Seek Path.
                Covers the execution of the seek_to logic when provided with a float value,
                ensuring the playhead update and console output statements are hit.
                """
        state = make_state_with_track(100.0)

        seek_to(state, 30.0)
        out = capsys.readouterr().out

        assert "Jumped to" in out
        assert format_mm_ss(state.position_seconds) == "00:30"

    def test_stmt_seek_to_mmss_string(self):
        """
                Statement Test S3: String Parsing Path.
                Executes the lines responsible for handling 'mm:ss' formatted string inputs
                via the parse_timecode utility function.
                """
        state = make_state_with_track(200.0)

        seek_to(state, "01:30")  # 90 seconds

        assert state.position_seconds == pytest.approx(90.0)


class TestNudgeStatement:
    def test_stmt_nudge_changes_position(self):
        """
                Statement Test S4: Increment Path.
                Ensures the execution of arithmetic update statements within the nudge function
                to verify that the playhead position changes correctly.
                """
        state = make_state_with_track(60.0)
        state.position_seconds = 10.0

        nudge(state, 5.0)

        assert state.position_seconds == pytest.approx(15.0)
