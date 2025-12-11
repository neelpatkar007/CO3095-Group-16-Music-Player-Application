"""
Backbone: Sprint 2 – playlists_basic

Stories:
- S2-01: Create, rename, delete playlists
- S2-05: List playlists and choose one
- S2-06: Open playlist and view contents
- S2-10: Show number of songs and total play time

This module handles the basic playlist lifecycle and listing.
"""

from __future__ import annotations
from typing import Optional

from music_player import player_core
from music_player.player_state import PlayerState
from music_player.playlist_model import Playlist
from music_player.time_utils import format_mm_ss


def _ensure_playlists(state: PlayerState) -> None:
    """Internal helper to ensure state.playlists exists."""
    if state.playlists is None:
        state.playlists = []


def _resolve_playlist(state: PlayerState, selector: str) -> Optional[Playlist]:
    """
    Internal helper: find a playlist by number (1-based) or by name (case-insensitive).
    Used by multiple S2 stories.
    """
    _ensure_playlists(state)
    selector = (selector or "").strip()
    if not selector:
        print("[pl] Missing playlist name or number.")
        return None

    # Try numeric index first
    try:
        idx = int(selector) - 1
    except ValueError:
        idx = None

    if idx is not None:
        if 0 <= idx < len(state.playlists):
            return state.playlists[idx]
        print("[pl] Playlist index out of range.")
        return None

    # Name match
    lowered = selector.lower()
    for pl in state.playlists:
        if pl.name.lower() == lowered:
            return pl

    print(f"[pl] Playlist '{selector}' not found.")
    return None


def _set_active_by_playlist(state: PlayerState, playlist: Playlist) -> None:
    """
    Internal helper: set active_playlist_index based on playlist instance.
    Used when opening / selecting playlists.
    """
    _ensure_playlists(state)
    try:
        idx = state.playlists.index(playlist)
    except ValueError:
        return
    state.active_playlist_index = idx

def _activate_playlist_queue(
    state: PlayerState,
    playlist: Playlist,
    auto_play: bool = True,
) -> None:
    """
    Make the given playlist the current playback queue.
    Sets state.tracks to the playlist's tracks.
    Resets current_index and position.
    Keeps a reference to the original library in state.library_tracks.
    """
    _ensure_playlists(state)

    # Ensure library_tracks is initialised
    if not hasattr(state, "library_tracks"):
        state.library_tracks = state.tracks

    _set_active_by_playlist(state, playlist)

    # Queue is now the playlist tracks
    state.tracks = playlist.tracks
    state.current_index = 0
    state.position_seconds = 0.0

    if auto_play:
        player_core.play(state)


# S2-01: create, rename, delete playlists


def create_playlist(state: PlayerState, name: str) -> None:
    """
    S2-01: Create new playlist.

    Behaviours:
      - Validate name is non-empty and unique.
      - Append new Playlist to state.playlists.
      - Optionally set active_playlist_index if none is active.
      - Print confirmation.
    """
    _ensure_playlists(state)
    name = (name or "").strip()
    if not name:
        print("[pl] Usage: /pl.new <name>")
        return

    for pl in state.playlists:
        if pl.name.lower() == name.lower():
            print(f"[pl] A playlist named '{name}' already exists.")
            return

    new_pl = Playlist(name=name)
    state.playlists.append(new_pl)
    if state.active_playlist_index is None:
        state.active_playlist_index = 0
    print(f"[pl] Created playlist '{name}'.")


def rename_playlist(state: PlayerState, selector: str, new_name: str) -> None:
    """
    S2-01: Rename an existing playlist.

    Behaviours:
      - Resolve playlist by selector (index or name).
      - Validate new_name is non-empty and not already taken.
      - Update playlist.name and print confirmation.
    """
    _ensure_playlists(state)
    new_name = (new_name or "").strip()
    if not new_name:
        print("[pl] Usage: /pl.rename <old> <new>")
        return

    pl = _resolve_playlist(state, selector)
    if pl is None:
        return

    for other in state.playlists:
        if other is not pl and other.name.lower() == new_name.lower():
            print(f"[pl] Another playlist already has the name '{new_name}'.")
            return

    old_name = pl.name
    pl.name = new_name
    print(f"[pl] Renamed playlist '{old_name}' -> '{new_name}'.")


def delete_playlist(state: PlayerState, selector: str) -> None:
    """
    S2-01: Delete an existing playlist.

    Behaviours:
      - Resolve playlist.
      - Remove from state.playlists.
      - Adjust active_playlist_index if necessary.
      - Print confirmation.
    """
    _ensure_playlists(state)
    pl = _resolve_playlist(state, selector)
    if pl is None:
        return

    idx = state.playlists.index(pl)
    del state.playlists[idx]

    if state.active_playlist_index is not None:
        if idx < state.active_playlist_index:
            state.active_playlist_index -= 1
        elif idx == state.active_playlist_index:
            state.active_playlist_index = None if not state.playlists else 0

    print(f"[pl] Deleted playlist '{pl.name}'.")


# S2-05, S2-06, S2-10: list, open, show contents


def list_playlists(state: PlayerState) -> None:
    """
    S2-05 + S2-10:
      - Print all playlists with index, name, number of tracks and total duration.
      - Mark active playlist with a special marker.
    """
    _ensure_playlists(state)

    if state is None:
        print("[pl] Internal Error: State is missing.")
        return
    if getattr(state, 'playlists', None) is None:
        return
    if not isinstance(state.playlists, list):
        print("[pl] Error: Playlist data is corrupted.")
        return
    if not state.playlists:
        print("[pl] No playlists defined.")
        return

    print("[pl] Playlists:")
    for idx, pl in enumerate(state.playlists, start=1):

        if pl is None:
            print(f"   {idx}. <Error: Invalid Playlist>")
            continue

        is_active = False
        current_index = idx - 1

        if state.active_playlist_index is not None:
            if state.active_playlist_index == current_index:
                is_active = True

        if hasattr(pl, 'summary_line'):
            print(pl.summary_line(index=idx, active=is_active))
        else:
            print(f"   {idx}. {pl.name} {'*' if is_active else ''}")


def open_playlist(state: PlayerState, selector: str) -> None:
    """
    S2-06:
      - Resolve playlist by selector.
      - Set as active.
      - Print tracks with numbers and durations.
    """
    _ensure_playlists(state)
    pl = _resolve_playlist(state, selector)
    if pl is None:
        return

    print(f"[pl] Opened playlist '{pl.name}':")
    _print_playlist_contents(pl)

    # Make it the active queue and start playback
    _activate_playlist_queue(state, pl, auto_play=True)


def show_current_playlist(state: PlayerState) -> None:
    """
    S2-06:
      - If an active playlist exists, print its contents.
      - Otherwise print guidance.
    """
    _ensure_playlists(state)
    if state.active_playlist_index is None or not state.playlists:
        print("[pl] No active playlist. Use /pl.open <name|index>.")
        return

    pl = state.playlists[state.active_playlist_index]
    print(f"[pl] Current playlist '{pl.name}':")
    _print_playlist_contents(pl)

def play_playlist(state: PlayerState, selector: str) -> None:
    """
    Explicit command for playing a specific playlist:
    - resolves the playlist
    - sets it as the active queue
    - starts playback from the first track
    """
    _ensure_playlists(state)
    pl = _resolve_playlist(state, selector)
    if pl is None:
        return
    _activate_playlist_queue(state, pl, auto_play=True)

def play_active_playlist(state: PlayerState) -> None:
    """
    Play whatever playlist is currently marked active.
    Used by /pl.play with no arguments.
    """
    _ensure_playlists(state)
    if state.active_playlist_index is None or not state.playlists:
        print("[pl] No active playlist. Use /pl.open or /pl.play <name>.")
        return

    pl = state.playlists[state.active_playlist_index]
    _activate_playlist_queue(state, pl, auto_play=True)

def close_playlist(state: PlayerState) -> None:
    """
    Return to the main library queue.

    - resets state.tracks back to state.library_tracks
    - clears active_playlist_index
    - stops playback and resets position
    """
    # If there's no library there's nowhere to go back to
    if not hasattr(state, "library_tracks"):
        print("[pl] No main library to return to.")
        return

    if state.tracks is state.library_tracks:
        # Already in main library
        state.active_playlist_index = None
        print("[pl] Already in main library.")
        return

    # Stop current playback and restore the main library as the queue
    player_core.stop(state)
    state.tracks = state.library_tracks
    state.current_index = 0
    state.position_seconds = 0.0
    state.active_playlist_index = None
    print("[pl] Closed playlist; returned to main library queue.")

def _print_playlist_contents(pl: Playlist) -> None:
    """
    This is a helper function that prints the contents of a playlist,
    showing each track's index, title, and duration in mm:ss format.
    If the playlist has no tracks, prints an '(empty)' marker instead.
    """
    if not pl.tracks:
        print("  (empty)")
        return

    for idx, track in enumerate(pl.tracks, start=1):
        dur = format_mm_ss(track.duration_seconds)
        print(f"{idx:02d}. {track.display_name} [{dur}]")