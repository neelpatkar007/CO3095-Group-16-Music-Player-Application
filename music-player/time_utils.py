"""
Module: time_utils
Helper functions for formatting and parsing time strings.
"""

def format_mm_ss(seconds: float) -> str:
    """
    Convert seconds to a 'mm:ss' formatted string.

    Used by progress display (S1-05, S1-06).
    """
    return ""


def parse_timecode(text: str) -> float:
    """
    Parse 'mm:ss' or plain seconds into a float number of seconds.

    Used by seek_to / nudge (S1-06, S1-08).
    """
    return 0.0
