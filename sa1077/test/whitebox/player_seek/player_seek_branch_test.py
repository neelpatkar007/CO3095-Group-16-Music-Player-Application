import pytest

from music_player.player_state import PlayerState
from music_player.audio_backend import AudioEngine
from music_player.library import Track
from music_player.player_seek import get_progress, seek_to, nudge
from music_player.time_utils import format_mm_ss


# Test: Helper function to create a player state with a track of a set length
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
    # Test: checking that progress is recorded correctly when a track is playing
    def test_branch_get_progress_with_track(self):
        state = make_state_with_track(200.0)
        state.position_seconds = 42.0

        pos, total = get_progress(state)

        assert pos == 42.0
        assert total == 200.0

    # Test: checking that the system handles progress correctly when no track is currently loaded
    def test_branch_get_progress_without_valid_track(self):
        engine = AudioEngine()
        state = PlayerState(tracks=[], audio_engine=engine)

        pos, total = get_progress(state)

        assert pos == state.position_seconds
        assert total is None


class TestSeekToBranch:
    # Test: verifying that seeking to a normal time within the song works correctly
    def test_branch_seek_to_seconds_normal_in_range(self, capsys):
        state = make_state_with_track(100.0)

        seek_to(state, 30.0)
        out = capsys.readouterr().out

        assert "Jumped to" in out
        assert format_mm_ss(state.position_seconds) == "00:30"

    # Test: ensuring that seeking to a negative time resets the position to the start (zero)
    def test_branch_seek_to_clamps_below_zero(self):
        state = make_state_with_track(60.0)

        seek_to(state, -10.0)

        assert state.position_seconds == pytest.approx(0.0)

    # Test: ensuring that seeking past the end of a song stops exactly at the finish time
    def test_branch_seek_to_clamps_above_duration(self):
        state = make_state_with_track(60.0)

        seek_to(state, 100.0)

        assert state.position_seconds == pytest.approx(60.0)

    # Test: checking that time strings like 'mm:ss' are correctly converted into seconds
    def test_branch_seek_to_with_mmss_string(self):
        state = make_state_with_track(200.0)

        seek_to(state, "01:30")  # 90 seconds

        assert state.position_seconds == pytest.approx(90.0)

    # Test: ensuring a warning is shown if the user tries to seek when no track is loaded
    def test_branch_seek_to_when_no_track_loaded_prints_warning(self, capsys):
        engine = AudioEngine()
        state = PlayerState(tracks=[], audio_engine=engine)

        seek_to(state, 10.0)
        out = capsys.readouterr().out

        assert "No track loaded" in out


class TestNudgeBranch:
    # Test: verifying that skipping forward near the end of a track does not go past the finish
    def test_branch_nudge_forward_with_clamp(self):
        state = make_state_with_track(60.0)
        state.position_seconds = 58.0

        nudge(state, 5.0)  # 58 + 5 -> 63 -> clamp to 60

        assert state.position_seconds == pytest.approx(60.0)

    # Test: verifying that skipping backward near the start of a track does not go below zero
    def test_branch_nudge_backward_with_clamp(self):
        state = make_state_with_track(60.0)
        state.position_seconds = 2.0

        nudge(state, -5.0)  # 2 - 5 -> -3 -> clamp to 0

        assert state.position_seconds == pytest.approx(0.0)