"""
Module: config
Central configuration for the Music Player app.
"""

from pathlib import Path

# Folder (called songs) that contains all songs that the player to read from.

MUSIC_DIR: Path = Path("songs")

# only allow audio file formats in the song directory.
SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".ogg", ".flac", ".m4a"}
