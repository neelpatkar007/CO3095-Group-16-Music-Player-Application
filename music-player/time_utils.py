"""
Module: time_utils
Helper functions for formatting and parsing time strings.
"""

def format_mm_ss(seconds: float) -> str:
    seconds = int(seconds)
    m = seconds // 60
    s = seconds % 60
    return f"{m:02d}:{s:02d}"

def parse_timecode(text: str) -> float:
    if ":" not in text:
        return float(text)
    parts = text.split(":")
    if len(parts) != 2:
        return 0.0
    m = int(parts[0])
    s = int(parts[1])
    return float(m * 60 + s)