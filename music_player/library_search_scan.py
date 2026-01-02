from __future__ import annotations
from collections import defaultdict
from typing import List

from music_player.player_state import PlayerState
from music_player.library import Track, discover_tracks
from music_player.time_utils import format_mm_ss


def _print_tracks_table(tracks: List[Track]) -> None:
    '''
    Prints a clean and formatted table of songs to the console.
    And because of no GUI, this ensures the text is aligned properly.
    '''

    if not tracks:
        print("  (no tracks)")
        return

    # Table headers with spacing
    print(f"{'No':>3}  {'Title':<30}  {'Artist':<20}  {'Time':>6}")
    print("-" * 65)

    for idx, t in enumerate(tracks, start=1):
        if t is None: continue
        # Truncate strings so that they do fit in the table nicely
        title = str(getattr(t, "title", "") or "")[:30]
        artist = str(getattr(t, "artist", "") or "")[:20]

        dur = format_mm_ss(getattr(t, "duration_seconds", None))

        # Print row with specific column widths matching the headers
        print(f"{idx:3d}  {title:<30}  {artist:<20}  {dur:>6}")


def search_library(state: PlayerState, query: str) -> None:
    '''
    Filters the library tracks based on a users search term.
    And checks title, artist, and filename.
    '''
    if state is None: return
    query = (query or "").strip().lower()
    if not query:
        print("[lib] Usage: /search <text>")
        return

    source_list = state.library_tracks

    results: List[Track] = []
    for t in source_list:
        if t is None: continue

        # Lowercase everything to make the search case-insensitive
        title = (getattr(t, "title", "") or "").lower()
        artist = (getattr(t, "artist", "") or "").lower()
        filename = ""

        # Check for path existence before accessing the name to avoid any errors
        if getattr(t, "path", None) is not None:
            filename = t.path.name.lower()

        # Check for matches in title, artist or filename
        if query in title or query in artist or query in filename:
            results.append(t)

    if not results:
        print("[lib] No matches found.")
    else:
        print(f"[lib] Search results for '{query}':")
        _print_tracks_table(results)


# Library viewing functions

def view_songs_table(state: PlayerState) -> None:
    '''
    A simple wrapper to dump the whole library on screen.
    '''
    print("[lib] Songs (library):")
    _print_tracks_table(state.library_tracks)


def view_artists_table(state: PlayerState) -> None:
    '''
    Groups the songs by artist so that the user can see their collection and
    this also calculates the total runtime for each artist.
    '''
    by_artist: dict[str, List[Track]] = defaultdict(list)
    for t in state.library_tracks:
        if not t or not getattr(t, "artist", None): continue
        by_artist[t.artist].append(t)

    print(f"{'Artist':<25}  {'Tracks':>6}  {'Time':>8}")
    print("-" * 45)

    # Sorts the artists alphabetically so that the list is predictable
    for artist, tracks in sorted(by_artist.items()):
        # Calculate total duration for this artist
        total = sum((t.duration_seconds or 0) for t in tracks)
        print(f"{artist:<25}  {len(tracks):6d}  {format_mm_ss(total):>8}")


def view_albums_table(state: PlayerState) -> None:
    '''
    Uses the folder names as album names to group the tracks as we are not using a database.
    This is a quick way to organise the music without any complex tagging.
    '''
    by_album: dict[str, List[Track]] = defaultdict(list)
    for t in state.library_tracks:
        # Because we dont have a database, the folders name is the most reliable title
        album = t.path.parent.name or "(no folder)"
        by_album[album].append(t)

    print(f"{'Album (folder)':<25}  {'Tracks':>6}  {'Time':>8}")
    print("-" * 45)
    for album, tracks in sorted(by_album.items()):
        total = sum((t.duration_seconds or 0) for t in tracks)
        print(f"{album:<25}  {len(tracks):6d}  {format_mm_ss(total):>8}")

# System Maintenance Functions

def rescan_for_new_tracks(state: PlayerState) -> None:
    '''
    This syncs the internal library with the actual files on disk.
    It looks for any new files that were not there during the last scan
    '''
    print("[lib] Scanning for new tracks...")

    # Track paths that are already in the library
    current_paths = {t.path for t in state.library_tracks}
    discovered = discover_tracks()

    # Only take the ones that are not already in the library
    new_tracks = [t for t in discovered if t.path not in current_paths]

    if not new_tracks:
        print("[lib] No new tracks found.")
        return

    # Add the new tracks to the library
    state.library_tracks.extend(new_tracks)


    if state.tracks is state.library_tracks:
        pass

    print(f"[lib] Added {len(new_tracks)} new track(s).")