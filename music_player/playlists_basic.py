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

from music_player.player_state import PlayerState
from music_player.playlist_model import Playlist


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
    # TODO: implement
    raise NotImplementedError


# --- S2-01: create, rename, delete playlists --------------------------------------


def create_playlist(state: PlayerState, name: str) -> None:
    """
    S2-01: Create new playlist.

    Behaviours:
      - Validate name is non-empty and unique.
      - Append new Playlist to state.playlists.
      - Optionally set active_playlist_index if none is active.
      - Print confirmation.
    """
    # TODO: implement
    raise NotImplementedError


def rename_playlist(state: PlayerState, selector: str, new_name: str) -> None:
    """
    S2-01: Rename an existing playlist.

    Behaviours:
      - Resolve playlist by selector (index or name).
      - Validate new_name is non-empty and not already taken.
      - Update playlist.name and print confirmation.
    """
    # TODO: implement
    raise NotImplementedError


def delete_playlist(state: PlayerState, selector: str) -> None:
    """
    S2-01: Delete an existing playlist.

    Behaviours:
      - Resolve playlist.
      - Remove from state.playlists.
      - Adjust active_playlist_index if necessary.
      - Print confirmation.
    """
    # TODO: implement
    raise NotImplementedError


# --- S2-05, S2-06, S2-10: list, open, show contents ------------------------------


def list_playlists(state: PlayerState) -> None:
    """
    S2-05 + S2-10:
      - Print all playlists with index, name, number of tracks and total duration.
      - Mark active playlist with a special marker.
    """
    # TODO: implement
    raise NotImplementedError


def open_playlist(state: PlayerState, selector: str) -> None:
    """
    S2-06:
      - Resolve playlist by selector.
      - Set as active.
      - Print tracks with numbers and durations.
    """
    # TODO: implement
    raise NotImplementedError


def show_current_playlist(state: PlayerState) -> None:
    """
    S2-06:
      - If an active playlist exists, print its contents.
      - Otherwise print guidance.
    """
    # TODO: implement
    raise NotImplementedError
