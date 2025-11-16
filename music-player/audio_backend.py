"""
Module: audio_backend
Abstracts the low-level audio playback engine.

Sprint 1 backbone:
 - Define the interface used by player_core for S1-01 and S1-12.
 - Real implementation (pygame) to be added.
"""

from pathlib import Path


class AudioEngine:
    """Placeholder audio engine to be implemented."""

    def play(self, path: Path, start_pos: float = 0.0) -> None:
        """Start playing the given file from start_pos seconds."""
        pass

    def pause(self) -> None:
        """Pause playback."""
        pass

    def resume(self) -> None:
        """Resume playback."""
        pass

    def stop(self) -> None:
        """Stop playback."""
        pass

    def is_busy(self) -> bool:
        """
        Return True if audio is currently playing.

        Implementation will be added later.
        """
        return False
