from __future__ import annotations
from pathlib import Path

try:
    import pygame
    pygame.mixer.init()
    HAS_PYGAME = True
except Exception:
    pygame = None  # type: ignore
    HAS_PYGAME = False
    print("[audio] pygame not available – using simulated audio backend.")


class AudioEngine:
    def __init__(self) -> None:
        self.current_path: Path | None = None
        self.playing: bool = False
        self.paused: bool = False
        self.volume: int = 100
        self.muted: bool = False

    def play(self, path: Path, start_pos: float = 0.0) -> None:
        self.current_path = path
        self.playing = True
        self.paused = False

        if HAS_PYGAME:
            self._play_real(path, start_pos)
        else:
            self._play_simulated(path, start_pos)

    def pause(self) -> None:
        if not self.playing or self.paused:
            return
        self.playing = False
        self.paused = True

        if HAS_PYGAME:
            self._pause_real()
        else:
            print("[audio] PAUSE (simulated)")

    def resume(self) -> None:
        if not self.paused:
            return
        self.paused = False
        self.playing = True

        if HAS_PYGAME:
            self._resume_real()
        else:
            print("[audio] RESUME (simulated)")

    def stop(self) -> None:
        if not self.playing and not self.paused:
            return

        self.playing = False
        self.paused = False

        if HAS_PYGAME:
            self._stop_real()
        else:
            print("[audio] STOP (simulated)")

    def is_busy(self) -> bool:
        if HAS_PYGAME:
            assert pygame is not None
            return pygame.mixer.music.get_busy()
        return self.playing and not self.paused

    def set_volume(self, value: int) -> None:
        self.volume = value
        if HAS_PYGAME:
            vol_float = max(0.0, min(1.0, value / 100.0))
            if pygame and pygame.mixer and pygame.mixer.music:
                pygame.mixer.music.set_volume(vol_float)

    def set_muted(self, muted: bool) -> None:
        self.muted = muted
        if muted:
            if HAS_PYGAME:
                pygame.mixer.music.set_volume(0.0)

    def _play_real(self, path: Path, start_pos: float) -> None:
        assert pygame is not None
        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.play(loops=0, start=start_pos)

            if self.muted:
                pygame.mixer.music.set_volume(0.0)
            else:
                self.set_volume(self.volume)

            print(f"[audio] PLAY (real) {path.name} from {start_pos:.1f}s")
        except Exception as e:
            print(f"[audio] ERROR playing {path}: {e}")

    def _pause_real(self) -> None:
        assert pygame is not None
        pygame.mixer.music.pause()

    def _resume_real(self) -> None:
        assert pygame is not None
        pygame.mixer.music.unpause()

    def _stop_real(self) -> None:
        assert pygame is not None
        pygame.mixer.music.stop()

    def _play_simulated(self, path: Path, start_pos: float) -> None:
        print(f"[audio] PLAY (simulated) {path.name} from {start_pos:.1f}s")

    # Seek implementation functions
    def seek(self, seconds: float) -> None:
        # Jump to a new position in the currently loaded file.
        if not self.current_path:
            return
        self.playing = True
        self.paused = False
        if HAS_PYGAME:
            self._seek_real(seconds)
        else:
            self._seek_simulated(seconds)

    def _seek_real(self, seconds: float) -> None:
        assert pygame is not None
        try:
            # Reload the current track and start from the new position.
            pygame.mixer.music.load(str(self.current_path))
            pygame.mixer.music.play(loops=0, start=seconds)
            
            # Apply correct volume (or silence) on seek
            if self.muted:
                pygame.mixer.music.set_volume(0.0)
            else:
                self.set_volume(self.volume)
            
            print(f"[audio] SEEK (real) -> {seconds:.1f}s")
        except Exception as e:
            print(f"[audio] ERROR seeking: {e}")

    def _seek_simulated(self, seconds: float) -> None:
        print(f"[audio] SEEK (simulated) -> {seconds:.1f}s")