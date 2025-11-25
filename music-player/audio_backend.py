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
        else:
            pass

    def _play_real(self, path: Path, start_pos: float) -> None:
        assert pygame is not None
        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.play(loops=0, start=start_pos)
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