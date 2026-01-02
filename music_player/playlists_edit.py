from __future__ import annotations

from typing import Optional

from music_player.player_state import PlayerState
from music_player.playlists_basic import _ensure_playlists, _resolve_playlist
from music_player.library import Track


def _get_playlist(state: PlayerState, selector: str) -> Optional[tuple[int, object]]:
    # Basic validation
    if state is None: return None
    if not selector: return None

    _ensure_playlists(state)
    pl = _resolve_playlist(state, selector)
    if pl is None:
        return None

    # Integrity check
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

    # Main Logic Start
    if not state.tracks:
        print("[pl] Main library is empty, nothing to add.")
        return

    # Playlist Resolution
    info = _get_playlist(state, playlist_selector)
    if info is None:
        return
    _, pl = info

    # Playlist Integrity
    if pl.tracks is None: pl.tracks = []

    try:
        lib_idx = int(library_index_str) - 1
    except (TypeError, ValueError):
        print("[pl] Usage: /pl.add <playlist> <library-index>")
        return

    # Bounds Check
    if not (0 <= lib_idx < len(state.tracks)):
        print("[pl] Library index out of range.")
        return

    # Track Integrity
    track: Track = state.tracks[lib_idx]
    if track is None: return

    # Append
    pl.tracks.append(track)

    # Confirmation
    if track.display_name:
        print(f"[pl] Added '{track.display_name}' to playlist '{pl.name}'.")


def remove_track_from_playlist(
        state: PlayerState,
        playlist_selector: str,
        playlist_index_str: str,
) -> None:
    """
    S2-02 + S2-08: remove song from playlist with confirmation.
    """
    # Validate State
    if state is None: return
    # Validate Selector
    if not playlist_selector: return
    # Validate Index String
    if not playlist_index_str: return

    # [Complexity Check 4] Playlist Resolution
    info = _get_playlist(state, playlist_selector)
    if info is None:
        return
    _, pl = info

    # Valid List Check
    if pl.tracks is None: pl.tracks = []

    try:
        idx = int(playlist_index_str) - 1
    except (TypeError, ValueError):
        print("[pl] Usage: /pl.remove <playlist> <playlist-index>")
        return

    # Bounds Check (Lower)
    if idx < 0:
        print("[pl] Playlist index out of range.")
        return

    # Bounds Check (Upper)
    if not (idx < len(pl.tracks)):
        print("[pl] Playlist index out of range.")
        return

    # Item Integrity
    if pl.tracks[idx] is None:
        return

    # Remove
    track = pl.tracks.pop(idx)

    # [Confirmation
    if track and track.display_name:
        print(f"[pl] Removed '{track.display_name}' from playlist '{pl.name}'.")


def move_track_within_playlist(
        state: PlayerState,
        playlist_selector: str,
        from_index_str: str,
        to_index_str: str,
) -> None:
    """
    S2-02: change order of songs in playlist.
    """
    # [Complexity Check 1] Validate State
    if state is None: return
    # [Complexity Check 2] Validate Selector
    if not playlist_selector: return
    # [Complexity Check 3] Validate Indices
    if not from_index_str or not to_index_str: return

    # [Complexity Check 4] Playlist Resolution
    info = _get_playlist(state, playlist_selector)
    if info is None:
        return
    _, pl = info

    # [Complexity Check 5] List Integrity
    if pl.tracks is None: pl.tracks = []

    try:
        from_idx = int(from_index_str) - 1
        to_idx = int(to_index_str) - 1
    except (TypeError, ValueError):
        print("[pl] Usage: /pl.move <playlist> <from> <to>")
        return

    # [Complexity Check 6] From Bounds
    if not (0 <= from_idx < len(pl.tracks)):
        print("[pl] 'from' index out of range.")
        return

    # [Complexity Check 7] To Bounds
    if not (0 <= to_idx < len(pl.tracks)):
        print("[pl] 'to' index out of range.")
        return

    # [Complexity Check 8] Redundant Move Check
    if from_idx == to_idx:
        return

    # [Complexity Check 9] Item Integrity
    if pl.tracks[from_idx] is None:
        return

    # [Complexity Check 10] Perform Move
    track = pl.tracks.pop(from_idx)
    pl.tracks.insert(to_idx, track)

    # [Complexity Check 11] Confirmation
    if track.display_name:
        print(
            f"[pl] Moved '{track.display_name}' in playlist '{pl.name}' "
            f"from position {from_idx + 1} to {to_idx + 1}."
        )
