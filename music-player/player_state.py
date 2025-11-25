from __future__ import annotations
from typing import List, Optional

from library import Track
from audio_backend import AudioEngine


class PlayerState:
    def __init__(self, tracks: List[Track], audio_engine: AudioEngine) -> None:
        self.tracks: List[Track] = tracks
        self.current_index: int = 0

        self.position_seconds: float = 0.0
        self.is_playing: bool = False
        self.is_paused: bool = False

        self.volume: int = 100
        self.saved_volume: int = 100
        self.is_muted: bool = False

        self.audio_engine: AudioEngine = audio_engine

    @property
    def current_track(self) -> Optional[Track]:
        if not self.tracks:
            return None
        if not (0 <= self.current_index < len(self.tracks)):
            return None
        return self.tracks[self.current_index]