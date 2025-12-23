from __future__ import annotations
from pathlib import Path

# Try to import the pygame for audio playback.
# If pygame is not installed, or it fails, then the code falls back to a simulated mode.
try:
    import pygame
    pygame.mixer.init(frequency=44100)
    HAS_PYGAME = True
except Exception:
    pygame = None
    HAS_PYGAME = False
    print("[audio] pygame not available – using simulated audio backend.")

# Pydub check (Required for real speed change)
try:
    from pydub import AudioSegment

    HAS_PYDUB = True
except ImportError:
    HAS_PYDUB = False
    print("[audio] pydub not found. Speed changes will be simulated.")

class AudioEngine:
    '''
    Handles the audio playback logic using pygame if it is available.
    '''

    def __init__(self) -> None:
        # Track whether the file is currently loaded.
        self.current_path: Path | None = None

        # The internal state flags to track logical playback status.
        self.playing: bool = False
        self.paused: bool = False

        # The volume level is stored as an integer from 0 to 100.
        self.volume: int = 100
        self.muted: bool = False

        # Track the current speed to adjust seek times correctly
        self.current_speed: float = 1.0

        # Temporary file for speed-modified audio
        self.temp_file = Path("temp_speed_audio.mp3")

    def play(self, path: Path, start_pos: float = 0.0, speed: float = 1.0) -> None:
        '''
        Loads and starts to play an audio file from a specific position.
        '''
        self.current_path = path
        self.playing = True
        self.paused = False
        self.current_speed = speed

        # Determine which file to play (Original or Temp)
        playback_path = path
        playback_start = start_pos

        # Logic for Real Speed Change
        if HAS_PYDUB and speed != 1.0:
            try:
                print(f"[audio] Processing audio for {speed}x speed... (this may take a moment)")

                # Load original audio
                seg = AudioSegment.from_file(path)

                # Change Speed
                new_rate = int(seg.frame_rate * speed)
                processed = seg._spawn(seg.raw_data, overrides={'frame_rate': new_rate})
                processed = processed.set_frame_rate(44100)

                # Export to temp file
                processed.export(self.temp_file, format="mp3")

                # Point playback to the temp file
                playback_path = self.temp_file

                # Adjust Start Position
                playback_start = start_pos / speed

            except Exception as e:
                print(f"[audio] Error processing speed: {e}. Falling back to 1.0x.")
                playback_path = path
                playback_start = start_pos
                self.current_speed = 1.0

        # Sent to the appropriate backend (Real or Simulated)
        if HAS_PYGAME:
            self._play_real(path, start_pos)
        else:
            self._play_simulated(path, start_pos)

    def pause(self) -> None:
        '''
        This pauses the audio, if it is currently playing.
        '''
        # Makes sure that cannot pause if it is stopped or already paused.
        if not self.playing or self.paused:
            return
        self.playing = False
        self.paused = True

        if HAS_PYGAME:
            self._pause_real()
        else:
            print("[audio] PAUSE (simulated)")

    def resume(self) -> None:
        '''
        This resumes the audio playback from the paused state.
        '''
        # Makes sure that cannot resume if it is not paused.
        if not self.paused:
            return
        self.paused = False
        self.playing = True

        if HAS_PYGAME:
            self._resume_real()
        else:
            print("[audio] RESUME (simulated)")

    def stop(self) -> None:
        '''
        Stops the audio playback completely and resets the paused state.
        '''
        # Doesn't do anything if already stopped.
        if not self.playing and not self.paused:
            return

        self.playing = False
        self.paused = False

        if HAS_PYGAME:
            self._stop_real()
        else:
            print("[audio] STOP (simulated)")

    def is_busy(self) -> bool:
        '''
        This Returns True if the audio is actively playing.
        '''
        if HAS_PYGAME:
            assert pygame is not None
            # Returns false even if paused.
            return pygame.mixer.music.get_busy()
        return self.playing and not self.paused

    def set_volume(self, value: int) -> None:
        '''This sets the master volume level from 0 to 100.'''
        self.volume = value
        if HAS_PYGAME:
            vol_float = max(0.0, min(1.0, value / 100.0))
            if pygame and pygame.mixer and pygame.mixer.music:
                pygame.mixer.music.set_volume(vol_float)

    def set_muted(self, muted: bool) -> None:
        '''
        This toggles the mute state so if muted, the volume is set to 0.
        '''
        self.muted = muted
        if muted:
            if HAS_PYGAME:
                pygame.mixer.music.set_volume(0.0)
        '''
        If unmuted, can't restore the volume here,
        as the play or set_volume methods handle that.
        '''

    # Private implementation functions for real pygame
    def _play_real(self, path: Path, start_pos: float) -> None:
        assert pygame is not None
        try:
            # Pygame requires to convert the Path to string.
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.play(loops=0, start=start_pos)

            # Apply the current volume or mute state immediately after starting.
            if self.muted:
                pygame.mixer.music.set_volume(0.0)
            else:
                self.set_volume(self.volume)

            print(f"[audio] PLAY (real) {path.name} from {start_pos:.1f}s (Speed: {self.current_speed}x)")
        except Exception as e:
            # If there is an error or file not found, it catches it out.
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

    # Private implementation functions for simulated mode without pygame
    def _play_simulated(self, path: Path, start_pos: float) -> None:
        print(f"[audio] PLAY (simulated) {path.name} from {start_pos:.1f}s")

    # Seek Implementation functions
    def seek(self, seconds: float) -> None:
        '''
        Jump to a new position in the currently loaded file track.
        '''
        # Can't seek if no track has been loaded.
        if not self.current_path:
            return

        # Update internal state
        self.playing = True
        self.paused = False

        if HAS_PYGAME:
            self._seek_real(seconds)
        else:
            self._seek_simulated(seconds)

    def _seek_real(self, seconds: float) -> None:
        assert pygame is not None
        try:
            actual_pos = seconds / self.current_speed

            target_file = self.current_path
            if self.current_speed != 1.0 and self.temp_file.exists():
                target_file = self.temp_file

            pygame.mixer.music.load(str(target_file))
            pygame.mixer.music.play(loops=0, start=actual_pos)

            if self.muted:
                pygame.mixer.music.set_volume(0.0)
            else:
                self.set_volume(self.volume)

            print(f"[audio] SEEK -> {seconds:.1f}s")
        except Exception as e:
            print(f"[audio] ERROR seeking: {e}")

    def _seek_simulated(self, seconds: float) -> None:
        print(f"[audio] SEEK (simulated) -> {seconds:.1f}s")