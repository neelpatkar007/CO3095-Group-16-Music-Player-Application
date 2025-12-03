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

class TestGetProgressBranch:
    def test_branch_get_progress_with_track(self):
        """B1: Branch where current_track is a valid Track."""
        state = make_state_with_track(200.0)
        state.position_seconds = 42.0

        pos, total = get_progress(state)

        assert pos == 42.0
        assert total == 200.0

    def test_branch_get_progress_without_valid_track(self):
        """B2: Branch where there is no valid current_track."""
        engine = AudioEngine()
        state = PlayerState(tracks=[], audio_engine=engine)

        pos, total = get_progress(state)

        # hardened logic: position returned, total is None
        assert pos == state.position_seconds
        assert total is None


class TestSeekToBranch:
    def test_branch_seek_to_seconds_normal_in_range(self, capsys):
        """B3: numeric seconds, within range."""
        state = make_state_with_track(100.0)

        seek_to(state, 30.0)
        out = capsys.readouterr().out

        assert "Jumped to" in out
        assert format_mm_ss(state.position_seconds) == "00:30"

    def test_branch_seek_to_clamps_below_zero(self):
        """B4: numeric seconds below 0 -> clamped to 0."""
        state = make_state_with_track(60.0)

        seek_to(state, -10.0)

        assert state.position_seconds == pytest.approx(0.0)

    def test_branch_seek_to_clamps_above_duration(self):
        """B5: numeric seconds above duration -> clamped to duration."""
        state = make_state_with_track(60.0)

        seek_to(state, 100.0)

        assert state.position_seconds == pytest.approx(60.0)

    def test_branch_seek_to_with_mmss_string(self):
        """B6: string 'mm:ss' path via parse_timecode."""
        state = make_state_with_track(200.0)

        seek_to(state, "01:30")  # 90 seconds

        assert state.position_seconds == pytest.approx(90.0)

    def test_branch_seek_to_when_no_track_loaded_prints_warning(self, capsys):
        """B7: branch where current_track is None -> 'No track loaded.'"""
        engine = AudioEngine()
        state = PlayerState(tracks=[], audio_engine=engine)

        seek_to(state, 10.0)
        out = capsys.readouterr().out

        assert "No track loaded" in out


class TestNudgeBranch:
    def test_branch_nudge_forward_with_clamp(self):
        """B8: nudge forward to beyond duration -> clamp at duration."""
        state = make_state_with_track(60.0)
        state.position_seconds = 58.0

        nudge(state, 5.0)  # 58 + 5 -> 63 -> clamp to 60

        assert state.position_seconds == pytest.approx(60.0)

    def test_branch_nudge_backward_with_clamp(self):
        """B9: nudge backward below 0 -> clamp at 0."""
        state = make_state_with_track(60.0)
        state.position_seconds = 2.0

        nudge(state, -5.0)  # 2 - 5 -> -3 -> clamp to 0

        assert state.position_seconds == pytest.approx(0.0)
