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
    """
    Parse 'mm:ss' or plain seconds into a float number of seconds.

    Used by seek_to / nudge (S1-06, S1-08).
    """
    text = text.strip()
    try:
        if ":" in text:
            minutes, seconds = map(float,text.split(":"))
            total = float(minutes * 60 + seconds)
        else:
            total = float(text)
        if total < 0:
            raise ValueError("Negative seconds are not supported")

        return total

    except ValueError:
        raise ValueError("Invalid timecode")

