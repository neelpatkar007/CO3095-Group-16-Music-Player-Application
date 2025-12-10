from __future__ import annotations
from typing import List, Optional

from music_player.library import Track
from music_player.audio_backend import AudioEngine


class PlayerState:
    '''
    Central state container for the music player application.
    Holds the current playlist, track index, playback position and audio settings.
    All modules (core, queue, seek, audio) read from and write to this single object.
    '''
    def __init__(self, tracks: List[Track], audio_engine: AudioEngine) -> None:
        # Playlist / queue of tracks to play
        self.tracks: List[Track] = tracks # List of all discovered tracks
        self.current_index: int = 0 # Index of the currently playing/selected track

        # Playback state
        self.position_seconds: float = 0.0 # Current position in seconds within the track
        self.is_playing: bool = False # Whether playback is currently active
        self.is_paused: bool = False # Whether playback is currently paused

        # Audio settings
        self.volume: int = 100 # Volume level from 0 to 100
        self.saved_volume: int = 100 # Saved volume level before muting
        self.is_muted: bool = False # True if audio is muted

        # Backend audio engine
        self.audio_engine: AudioEngine = audio_engine # Reference to the audio engine output handler

    @property
    def current_track(self) -> Optional[Track]:
        '''
        Retrieves the currently selected track, or none if it is out of bounds.
        '''
        # Check if the playlist is empty
        if not self.tracks:
            return None

        # Check if the index is within the valid range
        if not (0 <= self.current_index < len(self.tracks)):
            return None
        return self.tracks[self.current_index]