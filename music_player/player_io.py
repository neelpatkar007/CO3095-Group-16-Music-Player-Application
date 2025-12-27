"""
Sprint 4 Module: File I/O
Stories:
 - S4-04: Import Songs
 - S4-10: Export Playlist
 - S4-11: Update Metadata
"""
import shutil
from pathlib import Path
from music_player.player_state import PlayerState
from music_player.config import MUSIC_DIR, SUPPORTED_EXTENSIONS
from music_player import library


# S4-04: Import Songs

def import_song(state: PlayerState, source_path_str: str) -> None:
    """
    Copies a valid audio file from an external source to the local 'songs/' directory.
    Triggers a library rescan upon success.
    """
    if not source_path_str:
        return

    src = Path(source_path_str)
    if not src.exists():
        print("[import] Error: File not found.")
        return

    if not src.is_file():
        print("[import] Error: Source is not a file.")
        return

    if src.stat().st_size == 0:
        print("[import] Error: File is empty.")
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

        if not state.tracks:
            state.tracks = new_tracks
    except PermissionError:
        print("[import] Error: Permission denied.")

    except Exception as e:
        print(f"[import] Copy failed: {e}")

# S4-10: Export Playlist

def export_playlist(state: PlayerState, name_or_file: str, filename_arg: str = "") -> None:
    """
    Exports a playlist to a .m3u file.
    name_or_file: Name of the playlist to export.
    filename_arg: Optional specific filename for the output.
    """
    def export_playlist(state: PlayerState, name_or_file: str, filename_arg: str = "") -> None:
        target_tracks = []
        output_filename = ""

        # Logic: Check if - 'name_or_file' matches a playlist name
        found_playlist = None
        for pl in state.playlists:
            if pl.name == name_or_file:
                found_playlist = pl
                break

        if found_playlist:
            # The user is exporting a specific playlist
            target_tracks = found_playlist.tracks
            # If they provided a second arg, we use that as the filename. Otherwise we will use the playlist name
            if filename_arg:
                output_filename = filename_arg
            else:
                output_filename = f"{found_playlist.name}.m3u"
            print(f"[export] Exporting playlist '{found_playlist.name}'...")
        else:
            # The user is exporting the current queue - and name_or_file is the filename.
            target_tracks = state.tracks
            output_filename = name_or_file
            print(f"[export] Exporting current library/queue...")

        if not target_tracks:
            print("[export] Nothing to export.")
            return

        if not output_filename.endswith(".m3u") and not output_filename.endswith(".txt"):
            output_filename += ".m3u"

        try:
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                for t in target_tracks:
                    dur = int(t.duration_seconds) if t.duration_seconds else -1
                    f.write(f"#EXTINF:{dur},{t.display_name}\n")
                    f.write(f"{t.path.resolve()}\n")

            print(f"[export] Saved {len(target_tracks)} songs to {output_filename}.")
        except Exception as e:
            print(f"[export] Error writing file: {e}")


# S4-11: Update Metadata

def update_metadata(state: PlayerState, index_str: str, field: str, value: str) -> None:
    """
    Updates the metadata (Title or Artist) of a song.
    Will write changes persistently to the file using mutagen if installed.
    """
    try:
        idx = int(index_str) - 1
        if not (0 <= idx < len(state.library_tracks)): raise ValueError
    except ValueError:
        print("[edit] Invalid song number.")
        return

    track = state.library_tracks[idx]

    if field == "title":
        track.title = value
    elif field == "artist":
        track.artist = value
    else:
        print("[edit] Can only edit 'title' or 'artist'.")
        return

    print(f"[edit] Updated {field} to '{value}'.")

    try:
        from mutagen.easyid3 import EasyID3
        from mutagen.id3 import ID3NoHeaderError

        try:
            audio = EasyID3(track.path)
        except ID3NoHeaderError:
            audio = EasyID3()
            audio.filename = track.path
            audio.save()  # Creating a header
            audio = EasyID3(track.path)

        audio[field] = value
        audio.save()
        print("[edit] File tags updated successfully (Persistent).")

    except ImportError:
        print("[edit] WARNING: 'mutagen' not installed. Changes will NOT persist after restart.")
    except Exception as e:
        print(f"[edit] Warning: Could not write to file: {e}")