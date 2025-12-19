"""
Module: config
Central configuration for the Music Player app.

Sprint 1:
 - Defines the songs folder used as the music library source.
"""

from pathlib import Path

# Folder (root directory) that contains all songs for the player to read from.
# Expects a 'songs' folder in the current working directory.

MUSIC_DIR: Path = Path("songs")

# Whitelists all audio file formats.
SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".ogg", ".flac", ".m4a"}
