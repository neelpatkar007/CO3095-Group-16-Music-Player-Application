"""
Sprint 4 Module: File I/O
Stories:
 - S4-04: Import Songs
 - S4-10: Export Playlist
 - S4-11: Update Metadata
"""
from music_player.player_state import PlayerState


# S4-04: Import Songs

def import_song(state: PlayerState, source_path_str: str) -> None:
    """
    Copies a valid audio file from an external source to the local 'songs/' directory.
    Triggers a library rescan upon success.
    """
    src = Path(source_path_str)
    if not src.exists():
        print("[import] Error: File not found.")
        return

    if src.suffix.lower() not in SUPPORTED_EXTENSIONS:
        print("[import] Error: Unsupported file type.")
        return

    if not MUSIC_DIR.exists():
        MUSIC_DIR.mkdir()

    dest = MUSIC_DIR / src.name
    if dest.exists():
        print(f"[import] Error: File '{src.name}' already exists in library.")
        return

    try:
        shutil.copy2(src, dest)
        print(f"[import] Successfully imported '{src.name}'.")

        new_tracks = library.discover_tracks()
        state.library_tracks = new_tracks

# S4-10: Export Playlist

def export_playlist(state: PlayerState, name_or_file: str, filename_arg: str = "") -> None:
    """
    Exports a playlist to a .m3u file.
    name_or_file: Name of the playlist to export.
    filename_arg: Optional specific filename for the output.
    """
    pass


# S4-11: Update Metadata

def update_metadata(state: PlayerState, index_str: str, field: str, value: str) -> None:
    """
    Updates the metadata (Title or Artist) of a song.
    Will write changes persistently to the file using mutagen if installed.
    """
    pass