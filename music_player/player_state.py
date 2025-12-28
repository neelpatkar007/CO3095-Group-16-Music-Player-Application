from __future__ import annotations
from typing import List, Optional, Set, Dict, Any

from music_player.library import Track
from music_player.audio_backend import AudioEngine
from music_player.playlist_model import Playlist


class PlayerState:
    '''
    Central state container for the music player application.
    Holds the current playlist, track index, playback position and audio settings.
    All modules (core, queue, seek, audio) read from and write to this single object.
    '''
    def __init__(self, tracks: List[Track], audio_engine: AudioEngine) -> None:
        # Main library – never lost. Used when not in playlist mode
        self.library_tracks: List[Track] = tracks

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

        # Sprint 2: playlists
        self.playlists: List[Playlist] = []
        self.active_playlist_index: int | None = None

        # S3-01 & S3-02: Shuffle and Loop
        self.shuffle_active: bool = False
        self.loop_mode: str = "all"  # Options: "off", "one", "all"

        # S3-03: History
        self.history: List[Track] = []

        # S3-07: Playback Speed
        self.playback_speed: float = 1.0

        # S3-12: Sleep Timer
        self.sleep_deadline: float | None = None  # Timestamp to stop

        # S3-08, S3-09 S3-11: Liked and Top songs
        self.play_counts: Dict[str, int] = {}
        self.liked_tracks: Set[str] = set()

        # User Data
        self.active_profile: str = "default"
        self.profiles: Dict[str, Any] = {}  # Stores data for other profiles
        self.song_ratings: Dict[str, int] = {}  # Path -> Rating (1-5)

        # Config & Tags
        self.song_tags: Dict[str, List[str]] = {}
        self.total_play_time: float = 0.0

        # Time & State
        self.scheduled_alarms: List[str] = []  # List of "HH:MM" strings
        self.resume_active: bool = False  # Flag to trigger resume logic on boot

    @property
    def current_track(self) -> Optional[Track]:
        '''
        Retrieves the currently selected track, or it's none if it is out of bounds.
        '''
        # Check if the playlist is empty
        if not self.tracks:
            return None

        # Check if the index is within the valid range
        if not (0 <= self.current_index < len(self.tracks)):
            return None
        return self.tracks[self.current_index]