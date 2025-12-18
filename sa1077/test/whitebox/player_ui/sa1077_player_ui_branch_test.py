from pathlib import Path

from music_player.player_state import PlayerState
from music_player.player_ui import (
    print_now_playing,
    print_progress,
    print_progress_bar,
)
from music_player.library import Track


class DummyEngine:
    """Minimal test double (stub) used to isolate UI rendering logic from audio hardware."""
    pass


def make_state_with_tracks(tracks):
    """Utility helper to initialise a PlayerState with a specific set of track metadata."""
    return PlayerState(tracks=tracks, audio_engine=DummyEngine())

def test_branch_now_playing_paused_status(capsys):
    """
        Branch Test: 'Paused' Logic Fork.
        Exercises the specific decision path in print_now_playing where is_playing is False
        but is_paused is True, ensuring the 'Paused:' prefix is correctly applied.
        """
    track = Track(
        path=Path("a.mp3"),
        title="Song",
        artist="Artist",
        duration_seconds=60,
    )
    state = make_state_with_tracks([track])
    state.current_index = 0
    state.is_playing = False
    state.is_paused = True

    print_now_playing(state)
    out = capsys.readouterr().out
    assert "Paused:" in out


def test_branch_now_playing_stopped_status(capsys):
    """
        Branch Test: 'Stopped' Default Logic.
        Forces the final 'else' branch in the status selection chain by setting both
        playing and paused flags to False.
        """
    track = Track(
        path=Path("a.mp3"),
        title="Song",
        artist="Artist",
        duration_seconds=60,
    )
    state = make_state_with_tracks([track])
    state.current_index = 0
    state.is_playing = False
    state.is_paused = False

    print_now_playing(state)
    out = capsys.readouterr().out
    assert "Stopped:" in out

def test_branch_progress_with_track_and_total(capsys):
    """
        Branch Test: Valid Duration Path.
        Verifies the branch where a track exists and its duration is fully known,
        triggering the formatting of both current position and total time.
        """
    track = Track(
        path=Path("a.mp3"),
        title="Timed",
        artist="Artist",
        duration_seconds=180.0,
    )
    state = make_state_with_tracks([track])
    state.current_index = 0
    state.position_seconds = 30.0  # 00:30

    print_progress(state)
    out = capsys.readouterr().out
    assert "00:30/03:00" in out

def test_branch_progress_bar_clamps_and_percentage(capsys):
    """
        Branch Test: Upper-Boundary Clamping Logic.
        Forces the decision path that handles positions exceeding the track duration.
        The logic must clamp the result to 100% to maintain visual integrity.
        """
    track = Track(
        path=Path("end.mp3"),
        title="End",
        artist="A",
        duration_seconds=60.0,
    )
    state = make_state_with_tracks([track])
    state.current_index = 0
    state.position_seconds = 999.0  # beyond duration -> clamp to 100%

    print_progress_bar(state)
    out = capsys.readouterr().out

    # Just check that it's a full bar / 100%
    assert "[ui]" in out
    assert "100%" in out or "100 %" in out
    # and that some bar characters are present
    assert "█" in out or "░" in out or "#" in out
