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
    # 1. Determine Source (Main Library vs Active Queue)
    source_tracks: List[Track] = []
    if hasattr(state, "library_tracks") and state.library_tracks:
        source_tracks = state.library_tracks
    elif state.tracks:
        source_tracks = state.tracks
    else:
        return

    # 2. Get Target
    info = _get_playlist(state, playlist_selector)
    if info is None: return
    _, pl = info

    # 3. Add
    try:
        lib_idx = int(library_index_str) - 1
        if 0 <= lib_idx < len(source_tracks):
            track = source_tracks[lib_idx]
            pl.tracks.append(track)
    except ValueError: pass