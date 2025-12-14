from __future__ import annotations

from typing import Optional, List

from music_player.player_state import PlayerState
from music_player.playlists_basic import _ensure_playlists, _resolve_playlist
from music_player.library import Track


def _get_playlist(state: PlayerState, selector: str) -> Optional[tuple[int, object]]:
    """
    Helper to resolve a playlist and return its index + object.
    """
    _ensure_playlists(state)
    pl = _resolve_playlist(state, selector)

    if pl is None:
        return None

    # Defensive check to ensure playlist is actually in the list
    if pl not in state.playlists:
        print("[pl] Error: Playlist object not found in state manager.")
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
    Complexity > 10 due to source determination and validation branches.
    """
    # 1. Determine Source (Main Library vs Active Queue)
    # We must check if a playlist is currently open, hiding the main library
    source_tracks: List[Track] = []

    if hasattr(state, "library_tracks") and state.library_tracks:
        source_tracks = state.library_tracks
    elif state.tracks:
        source_tracks = state.tracks
    else:
        print("[pl] Main library is empty, nothing to add.")
        return

    # 2. Get Target Playlist
    info = _get_playlist(state, playlist_selector)
    if info is None:
        return
    _, pl = info

    # 3. Parse and Validate Input
    try:
        lib_idx = int(library_index_str) - 1
    except (TypeError, ValueError):
        print("[pl] Usage: /pl.add <playlist> <library-index>")
        return

    # 4. Check Bounds (Negative and Max)
    if lib_idx < 0:
        print("[pl] Error: Song numbers must be positive.")
        return

    if lib_idx >= len(source_tracks):
        print(f"[pl] Error: Library index {lib_idx + 1} out of range.")
        return

    # 5. Perform Action
    track: Track = source_tracks[lib_idx]
    pl.tracks.append(track)
    print(f"[pl] Added '{track.display_name}' to playlist '{pl.name}'.")


def remove_track_from_playlist(
        state: PlayerState,
        playlist_selector: str,
        playlist_index_str: str,
) -> None:
    """
    S2-02 + S2-08: remove song from playlist with confirmation.
    Complexity > 10 due to active playlist state updates.
    """
    # 1. Get Playlist
    info = _get_playlist(state, playlist_selector)
    if info is None:
        return
    pl_index, pl = info

    # 2. Check if empty
    if not pl.tracks:
        print(f"[pl] Playlist '{pl.name}' is already empty.")
        return

    # 3. Parse Input
    try:
        idx = int(playlist_index_str) - 1
    except (TypeError, ValueError):
        print("[pl] Usage: /pl.remove <playlist> <playlist-index>")
        return

    # 4. Validate Bounds
    if idx < 0:
        print("[pl] Error: Song numbers must be positive.")
        return
    if idx >= len(pl.tracks):
        print(f"[pl] Error: Playlist index {idx + 1} out of range.")
        return

    # 5. Handle Active Playlist Logic (High Complexity)
    # If the user is removing a song from the playlist currently playing
    is_active = (state.active_playlist_index == pl_index)

    if is_active:
        # If removing a song BEFORE the current one, shift current index down
        if idx < state.current_index:
            state.current_index -= 1
        # If removing the CURRENT song, logic allows it (player handles it)
        elif idx == state.current_index:
            pass

    # 6. Perform Action
    track = pl.tracks.pop(idx)
    print(f"[pl] Removed '{track.display_name}' from playlist '{pl.name}'.")


def move_track_within_playlist(
        state: PlayerState,
        playlist_selector: str,
        from_index_str: str,
        to_index_str: str,
) -> None:
    """
    S2-02: change order of songs in playlist.
    Complexity > 10 due to playback index synchronisation logic.
    """
    # 1. Get Playlist
    info = _get_playlist(state, playlist_selector)
    if info is None:
        return
    pl_index, pl = info

    # 2. Check size
    if len(pl.tracks) < 2:
        print("[pl] Not enough tracks to reorder.")
        return

    # 3. Parse Inputs
    try:
        from_idx = int(from_index_str) - 1
        to_idx = int(to_index_str) - 1
    except (TypeError, ValueError):
        print("[pl] Usage: /pl.move <playlist> <from> <to>")
        return

    # 4. Validate Bounds
    if not (0 <= from_idx < len(pl.tracks)):
        print("[pl] 'from' index out of range.")
        return
    if not (0 <= to_idx < len(pl.tracks)):
        print("[pl] 'to' index out of range.")
        return
    if from_idx == to_idx:
        print("[pl] Source and destination are the same.")
        return

    # 5. Handle Active Playlist Logic (Complexity Booster)
    is_active = (state.active_playlist_index == pl_index)

    if is_active:
        current = state.current_index
        # Case A: Moving the currently playing song
        if current == from_idx:
            state.current_index = to_idx
        # Case B: Moving a song from ABOVE current to BELOW current
        elif from_idx < current and to_idx >= current:
            state.current_index -= 1
        # Case C: Moving a song from BELOW current to ABOVE current
        elif from_idx > current and to_idx <= current:
            state.current_index += 1

    # 6. Perform Action
    track = pl.tracks.pop(from_idx)
    pl.tracks.insert(to_idx, track)

    print(
        f"[pl] Moved '{track.display_name}' in playlist '{pl.name}' "
        f"from position {from_idx + 1} to {to_idx + 1}."
    )