from pathlib import Path
from types import SimpleNamespace

from music_player.player_core import play, pause, stop, update_playback
from music_player.player_state import PlayerState


class DummyEngine:
    def __init__(self):
        self.play_calls = []
        self.paused = False
        self.stopped = False
        self.resumed = False

    def play(self, path, start_pos=0.0):
        self.play_calls.append((path, start_pos))

    def pause(self):
        self.paused = True

    def stop(self):
        self.stopped = True

    def resume(self):
        self.resumed = True


def make_state_with_track(duration=120.0):
    engine = DummyEngine()
    # SimpleNamespace is enough – only .path, .display_name and duration_seconds are used.
    track = SimpleNamespace(
        path=Path("song.mp3"),
        display_name="Song",
        duration_seconds=duration,
    )
    state = PlayerState(tracks=[track], audio_engine=engine)
    state.current_index = 0
    return state, track, engine


def test_play_already_playing_branch(capsys):
    state, _, _ = make_state_with_track()
    state.is_playing = True
    state.is_paused = False

    play(state)
    out = capsys.readouterr().out
    assert "Already playing" in out


def test_play_resumes_from_pause(capsys):
    state, track, engine = make_state_with_track()
    state.is_playing = False
    state.is_paused = True

    play(state)
    out = capsys.readouterr().out

    assert engine.resumed is True
    assert state.is_playing is True
    assert state.is_paused is False
    assert f"Resumed: {track.display_name}" in out


def test_play_fresh_play_starts_engine(capsys):
    state, track, engine = make_state_with_track()
    # default is not playing and not paused
    state.position_seconds = 5.0

    play(state)
    out = capsys.readouterr().out

    assert engine.play_calls == [(track.path, 5.0)]
    assert state.is_playing is True
    assert state.is_paused is False
    assert f"Playing: {track.display_name}" in out


def test_pause_nothing_to_pause_branch(capsys):
    state, _, _ = make_state_with_track()
    # default: not playing
    pause(state)
    out = capsys.readouterr().out
    assert "Nothing to pause" in out


def test_pause_happy_path(capsys):
    state, _, engine = make_state_with_track()
    state.is_playing = True
    state.is_paused = False

    pause(state)
    out = capsys.readouterr().out

    assert engine.paused is True
    assert state.is_playing is False
    assert state.is_paused is True
    assert "Paused." in out


def test_stop_nothing_is_playing_branch(capsys):
    state, _, _ = make_state_with_track()
    state.is_playing = False
    state.is_paused = False

    stop(state)
    out = capsys.readouterr().out
    assert "Nothing is playing" in out


def test_stop_happy_path(capsys):
    state, _, engine = make_state_with_track()
    state.is_playing = True
    state.is_paused = False
    state.position_seconds = 42.0

    stop(state)
    out = capsys.readouterr().out

    assert engine.stopped is True
    assert state.is_playing is False
    assert state.is_paused is False
    assert state.position_seconds == 0.0
    assert "Stopped." in out


def test_update_playback_ignores_non_positive_delta():
    state, _, _ = make_state_with_track()
    state.is_playing = True
    before = state.position_seconds

    update_playback(state, 0.0)
    assert state.position_seconds == before


def test_update_playback_stops_at_track_end(capsys):
    state, track, engine = make_state_with_track(duration=100.0)
    state.is_playing = True
    state.is_paused = False
    state.position_seconds = 95.0

    # delta pushes beyond duration
    update_playback(state, 10.0)
    out = capsys.readouterr().out

    assert state.position_seconds == track.duration_seconds
    assert state.is_playing is False
    assert engine.stopped is True
    assert "Track finished" in out
