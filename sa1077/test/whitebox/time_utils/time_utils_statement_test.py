import pytest
from music_player.time_utils import format_mm_ss, parse_timecode


class TestFormatMmSsStatement:
    """
        Statement Testing suite for time formatting.
        Ensures 100% line coverage (C0) by executing all logic paths within format_mm_ss.
        """
    def test_stmt_none_early_return(self):
        """
                Statement Test: Null Input Guard.
                Executes the early-return path when the input is None, verifying
                placeholder display logic.
                """
        assert format_mm_ss(None) == "??:??"

    def test_stmt_normal_value(self):
        """
                Statement Test: Standard Formatting Path.
                Covers the main execution logic for valid durations, ensuring
                accurate mm:ss calculation and string conversion.
                """
        assert format_mm_ss(90.0) == "01:30"

class TestParseTimecodeStatement:
    """
        Statement Testing suite for timecode parsing.
        Validates that every line of the parser—from standard floats to colon
        splitting—is executed.
        """
    def test_stmt_plain_seconds(self):
        """
                Statement Test: Direct Numeric Path.
                Executes the logic path for plain numeric strings, verifying
                direct float conversion.
                """
        assert parse_timecode("42") == pytest.approx(42.0)

    def test_stmt_mm_ss_path(self):
        """
                Statement Test: Colon-Based Parsing.
                Exercises the specific code path responsible for splitting 'mm:ss'
                strings and calculating total seconds.
                """
        assert parse_timecode("01:30") == pytest.approx(90.0)

    def test_stmt_empty_string(self):
        """
                Statement Test: Empty String Sanitisation.
                Covers the guard statements that prevent errors when
                encountering empty input strings.
                """
        assert parse_timecode("") == pytest.approx(0.0)

    def test_stmt_invalid_string(self):
        """
                Statement Test: Error Handling Fallback.
                Forces execution of the try-except (ValueError) logic path to
                ensure system resilience against malformed text.
                """
        assert parse_timecode("abc") == pytest.approx(0.0)
