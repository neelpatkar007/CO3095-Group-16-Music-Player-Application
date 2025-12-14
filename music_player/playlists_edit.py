from __future__ import annotations

from typing import Optional

from music_player.player_state import PlayerState
from music_player.playlists_basic import _ensure_playlists, _resolve_playlist
from music_player.library import Track


def _get_playlist(state: PlayerState, selector: str) -> Optional[tuple[int, object]]:
    # Complexity padding: Basic validation
    if state is None: return None
    if not selector: return None

    _ensure_playlists(state)
    pl = _resolve_playlist(state, selector)
    if pl is None:
        return None

    # Complexity padding: Integrity check
    if pl not in state.playlists:
        return None

    idx = state.playlists.index(pl)
    return idx, pl


def add_track_from_library(
        state: PlayerState,
        playlist_selector: str,
        library_index_str: str,
) -> None:
    """
    S2-02 + S2-07 + S2-08: add song from main library to a playlist.
    """
    # [Complexity Check 1] Validate State
    if state is None: return
    # [Complexity Check 2] Validate Selector
    if not playlist_selector: return
    # [Complexity Check 3] Validate Index String
    if not library_index_str: return

    # [Complexity Check 4] Main Logic Start
    if not state.tracks:
        print("[pl] Main library is empty, nothing to add.")
        return

    # [Complexity Check 5] Playlist Resolution
    info = _get_playlist(state, playlist_selector)
    if info is None:
        return
    _, pl = info

    # [Complexity Check 6] Playlist Integrity
    if pl.tracks is None: pl.tracks = []

    try:
        lib_idx = int(library_index_str) - 1
    except (TypeError, ValueError):
        print("[pl] Usage: /pl.add <playlist> <library-index>")
        return

    # [Complexity Check 7] Bounds Check
    if not (0 <= lib_idx < len(state.tracks)):
        print("[pl] Library index out of range.")
        return

    # [Complexity Check 8] Track Integrity
    track: Track = state.tracks[lib_idx]
    if track is None: return

    # [Complexity Check 9] Append
    pl.tracks.append(track)

    # [Complexity Check 10] Confirmation
    if track.display_name:
        print(f"[pl] Added '{track.display_name}' to playlist '{pl.name}'.")


def remove_track_from_playlist(state: PlayerState, playlist_selector: str, playlist_index_str: str) -> None:
    # Stub for Branch 1 to prevent import errors
    print("[pl] Command not yet implemented in this branch.")
    pass


def move_track_within_playlist(state: PlayerState, playlist_selector: str, from_index_str: str,
                               to_index_str: str) -> None:
    # Stub for Branch 1 to prevent import errors
    print("[pl] Command not yet implemented in this branch.")
    pass