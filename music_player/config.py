"""
Module: config
Central configuration for the Music Player app.

Sprint 1:
 - Defines the songs folder used as the music library source.
"""

from pathlib import Path

# Folder that contains all songs for the player to read from.
MUSIC_DIR: Path = Path("songs")

# Supported audio file extensions.
SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".ogg", ".flac", ".m4a"}
