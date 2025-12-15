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
    # Ensure playlist structures exist before operating
    _ensure_playlists(state)

    # Check 1: Validate target selector input
    if not target_selector or not target_selector.strip():
        print("[pl] Target selector cannot be empty.")
        return

    # Check 2: Validate source selector input
    if not source_selector or not source_selector.strip():
        print("[pl] Source selector cannot be empty.")
        return

    # Resolve target and source playlists
    target = _get_playlist(state, target_selector)
    if target is None:
        return

    # Resolve source playlist
    source = _get_playlist(state, source_selector)
    if source is None:
        return

    # Prevent the merging of a playlist into itself
    if target is source:
        print("[pl] Cannot merge a playlist into itself.")
        return

    # Empty Source Check
    # Check 3: Warn if source is empty (prevents useless looping)
    if not source.tracks:
        print(f"[pl] Source playlist '{source.name}' is empty.")
        return

    added = 0
    skipped_corrupt = 0

    for track in source.tracks:
        # Data Integrity Check
        # Check 4: Skip tracks that might be corrupted (or missing title)
        if not track.title:
            skipped_corrupt += 1
            continue

        # Skip adding tracks that already exist when deduplication is enabled
        if dedupe and track in target.tracks:
            continue
        # Append the track. And track how many were added.
        target.tracks.append(track)
        added += 1

    # Build human-readable deduplication status
    dedupe_text = "with duplicates removed" if dedupe else "including duplicates"

    # Final confirmation message of merge summary
    print(
        f"[pl] Merged {added} tracks from '{source.name}' into "
        f"'{target.name}' ({dedupe_text})."
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
    _ensure_playlists(state)
    new_name = (new_name or "").strip()
    # Validation for new_name
    if not new_name:
        print("[pl] Usage: /pl.copy <source> <new-name>")
        return

    # Look up source playlist to copy from
    source = _get_playlist(state, source_selector)
    if source is None:
        # _get_playlist already prints error
        return

    # Check for name conflict
    for pl in state.playlists:
        if pl.name.lower() == new_name.lower():
            print(f"[pl] A playlist named '{new_name}' already exists.")
            return

    cloned = Playlist(name=new_name, tracks=list(source.tracks))
    state.playlists.append(cloned)
    print(f"[pl] Copied playlist '{source.name}' -> '{new_name}'.")

