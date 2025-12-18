import pytest

from music_player.player_state import PlayerState
from music_player.audio_backend import AudioEngine
from music_player.library import Track
from music_player.player_seek import get_progress, seek_to, nudge
from music_player.time_utils import format_mm_ss


def make_state_with_track(duration: float = 180.0) -> PlayerState:
    """Utility factory to initialise a consistent PlayerState with a fixed track duration."""
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

class TestGetProgressBranch:
    def test_branch_get_progress_with_track(self):
        """Branch B1: Valid Track Case. Exercises the logic path where a track is actively loaded."""
        state = make_state_with_track(200.0)
        state.position_seconds = 42.0

        pos, total = get_progress(state)

        assert pos == 42.0
        assert total == 200.0

    def test_branch_get_progress_without_valid_track(self):
        """Branch B2: Null Track Case. Exercises the 'else' logic when the current track is missing."""
        engine = AudioEngine()
        state = PlayerState(tracks=[], audio_engine=engine)

        pos, total = get_progress(state)

        # Logic verification: ensures current position is returned while total remains None
        assert pos == state.position_seconds
        assert total is None


class TestSeekToBranch:
    def test_branch_seek_to_seconds_normal_in_range(self, capsys):
        """Branch B3: Numeric In-Range Seek. Standard success path for numeric input within duration bounds."""
        state = make_state_with_track(100.0)

        seek_to(state, 30.0)
        out = capsys.readouterr().out

        assert "Jumped to" in out
        assert format_mm_ss(state.position_seconds) == "00:30"

    def test_branch_seek_to_clamps_below_zero(self):
        """Branch B4: Lower Bound Decision. Forces the branch that clamps negative seek times to 0.0."""
        state = make_state_with_track(60.0)

        seek_to(state, -10.0)

        assert state.position_seconds == pytest.approx(0.0)

    def test_branch_seek_to_clamps_above_duration(self):
        """Branch B5: Upper Bound Decision. Forces the branch that clamps excessive seek times to the track end."""
        state = make_state_with_track(60.0)

        seek_to(state, 100.0)

        assert state.position_seconds == pytest.approx(60.0)

    def test_branch_seek_to_with_mmss_string(self):
        """Branch B6: Timecode String Path. Exercises the branch that parses and processes 'mm:ss' formatted inputs."""
        state = make_state_with_track(200.0)

        seek_to(state, "01:30")  # 90 seconds

        assert state.position_seconds == pytest.approx(90.0)

    def test_branch_seek_to_when_no_track_loaded_prints_warning(self, capsys):
        """Branch B7: Empty Library Guard. Triggers the error-handling branch when seeking without a loaded track."""
        engine = AudioEngine()
        state = PlayerState(tracks=[], audio_engine=engine)

        seek_to(state, 10.0)
        out = capsys.readouterr().out

        assert "No track loaded" in out


class TestNudgeBranch:
    def test_branch_nudge_forward_with_clamp(self):
        """Branch B8: Forward Nudge Boundary. Verifies the decision logic for forward nudges exceeding track duration."""
        state = make_state_with_track(60.0)
        state.position_seconds = 58.0

        nudge(state, 5.0)  # 58 + 5 -> 63 -> clamp to 60

        assert state.position_seconds == pytest.approx(60.0)

    def test_branch_nudge_backward_with_clamp(self):
        """Branch B9: Backward Nudge Boundary. Verifies the decision logic for backward nudges dropping below 0.0."""
        state = make_state_with_track(60.0)
        state.position_seconds = 2.0

        nudge(state, -5.0)  # 2 - 5 -> -3 -> clamp to 0

        assert state.position_seconds == pytest.approx(0.0)
