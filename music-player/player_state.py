"""
Module: player_state
Holds the current state of the music player.

Used in Sprint 1:
 - S1-01: play/pause/stop
 - S1-02: next/previous
 - S1-03: now playing display
 - S1-04: volume
 - S1-05, S1-06, S1-08: progress & seek
 - S1-09: mute
 - S1-10: indicator
 - S1-12: non-blocking playback while using CLI
"""
from __future__ import annotations
from typing import List, Optional

from library import Track
from audio_backend import AudioEngine


class PlayerState:
    """Represents the current player state."""

    def __init__(self, tracks: List[Track], audio_engine: AudioEngine) -> None:
        self.tracks: List[Track] = tracks
        self.current_index: int = 0

        # Playback position & status
        self.position_seconds: float = 0.0
        self.is_playing: bool = False
        self.is_paused: bool = False

        # Audio settings (S1-04, S1-09)
        self.volume: int = 100
        self.is_muted: bool = False

        # Backend engine
        self.audio_engine: AudioEngine = audio_engine

    @property
    def current_track(self) -> Optional[Track]:
        """Return the currently selected track or None if unavailable."""
        if not self.tracks:
            return None
        if not (0 <= self.current_index < len(self.tracks)):
            return None
        return self.tracks[self.current_index]
