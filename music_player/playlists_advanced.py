"""
Backbone: Sprint 2 – playlists_advanced

Stories:
- S2-10: Playlist stats already exposed by Playlist model
- S2-11: Merge two playlists, optionally deduplicating
- S2-12: Copy a playlist
"""

from __future__ import annotations
from typing import Optional

from music_player.player_state import PlayerState
from music_player.playlist_model import Playlist
from music_player.playlists_basic import _ensure_playlists, _resolve_playlist


def _get_playlist(state: PlayerState, selector: str) -> Optional[Playlist]:
    """
    Helper: resolve Playlist for advanced operations (merge/copy).
    """
    # TODO: implement
    raise NotImplementedError


def merge_playlists(
    state: PlayerState,
    target_selector: str,
    source_selector: str,
    dedupe: bool = True,
) -> None:
    """
    S2-11:
      - Resolve target and source playlists.
      - If same playlist, print error and abort.
      - Append tracks from source into target.
      - If dedupe=True, skip tracks already present in target.
      - Print summary (how many added, whether deduped).
    """
    _ensure_playlists(state)

    target = _get_playlist(state, target_selector)
    if target is None:
        return
    source = _get_playlist(state, source_selector)
    if source is None:
        return

    if target is source:
        print("[pl] Cannot merge a playlist into itself.")
        return


    )


def copy_playlist(
    state: PlayerState,
    source_selector: str,
    new_name: str,
) -> None:
    """
    S2-12:
      - Resolve source playlist.
      - Validate new_name non-empty and not already used.
      - Create new Playlist with the new name and a copy of the tracks.
      - Append to state.playlists.
      - Print confirmation.
    """
    # TODO: implement
    raise NotImplementedError
