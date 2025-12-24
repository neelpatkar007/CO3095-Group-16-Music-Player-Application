from pathlib import Path

from music_player.player_state import PlayerState
from music_player.player_ui import (
    print_now_playing,
    print_progress,
    print_progress_bar,
)
from music_player.library import Track


# Test: A simple fake engine used to test the UI without needing actual audio hardware
class DummyEngine:
    pass


# Test: Helper function to set up a player state with a list of tracks
def make_state_with_tracks(tracks):
    return PlayerState(tracks=tracks, audio_engine=DummyEngine())

# Test: checking that the 'Paused' status appears correctly when a song is not playing but is on pause
def test_branch_now_playing_paused_status(capsys):
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


# Test: checking that the 'Stopped' status appears when the player is neither playing nor paused
def test_branch_now_playing_stopped_status(capsys):
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

# Test: verifying that the UI shows the correct current time and total duration for a song
def test_branch_progress_with_track_and_total(capsys):
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

# Test: ensuring the progress bar stays at 100% and does not break if the song time exceeds the duration
def test_branch_progress_bar_clamps_and_percentage(capsys):
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