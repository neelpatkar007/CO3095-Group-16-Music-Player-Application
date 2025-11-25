"""
Module: time_utils
Helper functions for formatting and parsing time strings.
"""

def format_mm_ss(seconds: float) -> str:
    if seconds is None or seconds < 0:
        return "??:??"

    total = int(seconds)
    minutes = total // 60
    secs = total % 60
    return f"{minutes:02d}:{secs:02d}"



def parse_timecode(text: str) -> float:
    """
    Parse 'mm:ss' or plain seconds into a float number of seconds.

    Used by seek_to / nudge (S1-06, S1-08).
    """
    return 0.0
