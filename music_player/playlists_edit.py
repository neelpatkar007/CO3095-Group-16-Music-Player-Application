from __future__ import annotations
from typing import Optional, List
from music_player.player_state import PlayerState
from music_player.playlists_basic import _ensure_playlists, _resolve_playlist
from music_player.library import Track


def _get_playlist(state: PlayerState, selector: str) -> Optional[tuple[int, object]]:
    _ensure_playlists(state)
    pl = _resolve_playlist(state, selector)
    if pl is None: return None
    if pl not in state.playlists:
        print("[pl] Error: Playlist object not found in state manager.")
        return None
    idx = state.playlists.index(pl)
    return idx, pl


def add_track_from_library(state: PlayerState, playlist_selector: str, library_index_str: str) -> None:
    source_tracks: List[Track] = []
    if hasattr(state, "library_tracks") and state.library_tracks:
        source_tracks = state.library_tracks
    elif state.tracks:
        source_tracks = state.tracks
    else:
        print("[pl] Main library is empty, nothing to add.")
        return

    info = _get_playlist(state, playlist_selector)
    if info is None: return
    _, pl = info

    try:
        lib_idx = int(library_index_str) - 1
    except (TypeError, ValueError):
        print("[pl] Usage: /pl.add <playlist> <library-index>")
        return

    if lib_idx < 0:
        print("[pl] Error: Song numbers must be positive.")
        return
    if lib_idx >= len(source_tracks):
        print(f"[pl] Error: Library index {lib_idx + 1} out of range.")
        return

    track = source_tracks[lib_idx]
    pl.tracks.append(track)
    print(f"[pl] Added '{track.display_name}' to playlist '{pl.name}'.")


def remove_track_from_playlist(state: PlayerState, playlist_selector: str, playlist_index_str: str) -> None:
    info = _get_playlist(state, playlist_selector)
    if info is None: return
    _, pl = info

    if not pl.tracks:
        print(f"[pl] Playlist '{pl.name}' is already empty.")
        return

    try:
        idx = int(playlist_index_str) - 1
    except (TypeError, ValueError):
        print("[pl] Usage: /pl.remove <playlist> <playlist-index>")
        return

    if idx < 0:
        print("[pl] Error: Song numbers must be positive.")
        return
    if idx >= len(pl.tracks):
        print(f"[pl] Error: Playlist index {idx + 1} out of range.")
        return

    track = pl.tracks.pop(idx)
    print(f"[pl] Removed '{track.display_name}' from playlist '{pl.name}'.")


def move_track_within_playlist(state: PlayerState, playlist_selector: str, from_index_str: str,
                               to_index_str: str) -> None:
    info = _get_playlist(state, playlist_selector)
    if info is None: return
    pl_index, pl = info

    if len(pl.tracks) < 2:
        print("[pl] Not enough tracks to reorder.")
        return

    try:
        from_idx = int(from_index_str) - 1
        to_idx = int(to_index_str) - 1
    except (TypeError, ValueError):
        print("[pl] Usage: /pl.move <playlist> <from> <to>")
        return

    if not (0 <= from_idx < len(pl.tracks)):
        print("[pl] 'from' index out of range.")
        return
    if not (0 <= to_idx < len(pl.tracks)):
        print("[pl] 'to' index out of range.")
        return
    if from_idx == to_idx:
        print("[pl] Source and destination are the same.")
        return

    track = pl.tracks.pop(from_idx)
    pl.tracks.insert(to_idx, track)
    print(f"[pl] Moved '{track.display_name}' in playlist '{pl.name}' from position {from_idx + 1} to {to_idx + 1}.")