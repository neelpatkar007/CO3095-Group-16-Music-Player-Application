"""
Module: time_utils
Helper functions for formatting and parsing time strings.
"""
from __future__ import annotations

from typing import Any


def format_mm_ss(seconds: float | None) -> str:
    """
    Convert floating point number of seconds to a 'mm:ss' formatted string.

    Returns "??:??" for negative values or None values.
    """
    # Handle invalid input or missing values
    if seconds is None or seconds < 0:
        return "??:??"

    total_seconds = int(seconds)

    # Calculate minutes and seconds
    minutes = total_seconds // 60
    secs = total_seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def parse_timecode(text: Any) -> float:
    """
    Parse time string into total number of seconds (float)
    Supports 2 formats -
        1 - Plain seconds
        2 - Minutes and seconds
    """
    # Normalise input to string
    if isinstance(text, bytes):
        text = text.decode(errors="ignore")
    else:
        text = str(text)

    text = text.strip()
    if not text:
        # Empty string: treat as 0.0 seconds
        return 0.0

    try:
        if ":" in text:
            # Minutes and seconds format
            parts = text.split(":")
            if len(parts) != 2:
                # Reject formats like "1:2:3", and are invalidated
                return 0.0

            minutes_str, seconds_str = parts
            minutes = float(minutes_str)
            seconds = float(seconds_str)
            total = minutes * 60.0 + seconds
        else:
            # Plain seconds format
            total = float(text)

        if total < 0:
            # Negative time is invalid
            return 0.0

        return float(total)

    except (TypeError, ValueError):
        # Catch errors if conversion to float fails
        return 0.0