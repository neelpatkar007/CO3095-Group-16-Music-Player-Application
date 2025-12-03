import pytest

from music_player.player_state import PlayerState
from music_player.audio_backend import AudioEngine
from music_player.library import Track
from music_player.player_seek import get_progress, seek_to, nudge
from music_player.time_utils import format_mm_ss


def make_state_with_track(duration: float = 180.0) -> PlayerState:
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
        """S1: Execute normal path with valid track and duration."""
        state = make_state_with_track(200.0)
        state.position_seconds = 42.0

        pos, total = get_progress(state)

        assert pos == 42.0
        assert total == 200.0


class TestSeekToStatement:
    def test_stmt_seek_to_seconds_in_range(self, capsys):
        """S2: Execute seek_to with numeric seconds inside duration."""
        state = make_state_with_track(100.0)

        seek_to(state, 30.0)
        out = capsys.readouterr().out

        assert "Jumped to" in out
        assert format_mm_ss(state.position_seconds) == "00:30"

    def test_stmt_seek_to_mmss_string(self):
        """S3: Execute seek_to via parse_timecode('mm:ss')."""
        state = make_state_with_track(200.0)

        seek_to(state, "01:30")  # 90 seconds

        assert state.position_seconds == pytest.approx(90.0)


class TestNudgeStatement:
    def test_stmt_nudge_changes_position(self):
        """S4: Execute nudge forward once."""
        state = make_state_with_track(60.0)
        state.position_seconds = 10.0

        nudge(state, 5.0)

        assert state.position_seconds == pytest.approx(15.0)
