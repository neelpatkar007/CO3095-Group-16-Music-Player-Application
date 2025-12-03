import pytest
from music_player.time_utils import format_mm_ss, parse_timecode


class TestFormatMmSsStatement:
    def test_stmt_none_early_return(self):
        """Covers early return path when seconds is None."""
        assert format_mm_ss(None) == "??:??"

    def test_stmt_normal_value(self):
        """Covers main execution path with valid seconds."""
        assert format_mm_ss(90.0) == "01:30"

class TestParseTimecodeStatement:
    def test_stmt_plain_seconds(self):
        """Covers float(text) path."""
        assert parse_timecode("42") == pytest.approx(42.0)

    def test_stmt_mm_ss_path(self):
        """Covers ':' path with mm:ss."""
        assert parse_timecode("01:30") == pytest.approx(90.0)

    def test_stmt_empty_string(self):
        """Covers empty input path."""
        assert parse_timecode("") == pytest.approx(0.0)

    def test_stmt_invalid_string(self):
        """Covers ValueError-handling fallback."""
        assert parse_timecode("abc") == pytest.approx(0.0)
