"""
Module: time_utils
Helper functions for formatting and parsing time strings.
"""
from __future__ import annotations

from typing import Any


def format_mm_ss(seconds: float | None) -> str:
    """Convert seconds to a 'mm:ss' formatted string.

    Returns "??:??" for negative values or None.
    """
    if seconds is None or seconds < 0:
        return "??:??"

    total_seconds = int(seconds)
    minutes = total_seconds // 60
    secs = total_seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def parse_timecode(text: Any) -> float:
    """Parse 'mm:ss' or plain seconds into a float number of seconds.
    """
    # Normalise to text
    if isinstance(text, bytes):
        text = text.decode(errors="ignore")
    else:
        text = str(text)

    text = text.strip()
    if not text:
        # Empty string: treat as 0.0
        return 0.0

    try:
        if ":" in text:
            parts = text.split(":")
            if len(parts) != 2:
                # Weird formats like "1:2:3" are invalidated
                return 0.0
            minutes_str, seconds_str = parts
            minutes = float(minutes_str)
            seconds = float(seconds_str)
            total = minutes * 60.0 + seconds
        else:
            total = float(text)

        if total < 0:
            # Negative seconds not supported
            return 0.0

        return float(total)

    except (TypeError, ValueError):
        # Any parsing problem -> invalid timecode -> default to 0.0
        return 0.0