"""
Backbone: Sprint 2 – playlists_edit

Stories:
- S2-02: Add, remove, change the order of songs in a playlist
- S2-07: Add song from main library to playlist using command
- S2-08: Confirmation message when adding/removing songs
"""

from __future__ import annotations
from typing import Optional

from music_player.player_state import PlayerState
from music_player.playlists_basic import _ensure_playlists, _resolve_playlist
from music_player.library import Track


def _get_playlist(state: PlayerState, selector: str) -> Optional[tuple[int, object]]:
    """
    Internal helper: resolve playlist and also return its index in state.playlists.
    Used by add/remove/move operations.
    """
    # TODO: implement
    raise NotImplementedError


def add_track_from_library(
    state: PlayerState,
    playlist_selector: str,
    library_index_str: str,
) -> None:
    """
    S2-02, S2-07, S2-08:
      - Interpret library_index_str as 1-based index into state.tracks.
      - Validate playlist exists and index in range.
      - Append that Track to playlist.tracks.
      - Print confirmation message.
    """
    # TODO: implement
    raise NotImplementedError


def remove_track_from_playlist(
    state: PlayerState,
    playlist_selector: str,
    playlist_index_str: str,
) -> None:
    """
    S2-02, S2-08:
      - Interpret playlist_index_str as 1-based index into playlist.tracks.
      - Validate and remove that entry.
      - Print confirmation message.
    """
    # TODO: implement
    raise NotImplementedError


def move_track_within_playlist(
    state: PlayerState,
    playlist_selector: str,
    from_index_str: str,
    to_index_str: str,
) -> None:
    """
    S2-02:
      - Interpret from/to as 1-based indices.
      - Validate bounds.
      - Pop track at from and insert at to.
      - Print confirmation message including old and new positions.
    """
    # TODO: implement
    raise NotImplementedError
