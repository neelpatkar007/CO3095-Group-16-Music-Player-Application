"""
Module: time_utils
Helper functions for formatting and parsing time strings.
"""

def format_mm_ss(seconds: float) -> str:
    if seconds is None or seconds < 0:
        return "??:??"

    timeTotal = int(seconds)
    minutes = timeTotal // 60
    secs = timeTotal % 60
    return f"{minutes:02d}:{secs:02d}"

def parse_timecode(text: str) -> float:
    if ":" not in text:
        return float(text)
    parts = text.split(":")
    if len(parts) != 2:
        return 0.0
    m = int(parts[0])
    s = int(parts[1])
    return float(m * 60 + s)