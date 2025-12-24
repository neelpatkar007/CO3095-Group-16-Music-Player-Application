import pytest
from music_player.time_utils import format_mm_ss, parse_timecode


# Test: A collection of tests to check that time values are correctly converted to readable text
class TestFormatMmSsStatement:

    # Test: checking that the system returns '??:??' when no time value is provided (None)
    def test_stmt_none_early_return(self):
        assert format_mm_ss(None) == "??:??"

    # Test: verifying that a standard number of seconds is converted correctly into a 'minutes:seconds' format
    def test_stmt_normal_value(self):
        assert format_mm_ss(90.0) == "01:30"


# Test: A collection of tests to check that text-based timecodes are correctly read as numbers
class TestParseTimecodeStatement:

    # Test: checking that a simple number inside a string is correctly read as a numeric value
    def test_stmt_plain_seconds(self):
        assert parse_timecode("42") == pytest.approx(42.0)

    # Test: verifying that the system can split and calculate total seconds from a 'minutes:seconds' format
    def test_stmt_mm_ss_path(self):
        assert parse_timecode("01:30") == pytest.approx(90.0)

    # Test: ensuring that a blank input string is handled safely and treated as zero seconds
    def test_stmt_empty_string(self):
        assert parse_timecode("") == pytest.approx(0.0)

    # Test: checking that the system returns zero and does not crash if the text provided is not a valid time
    def test_stmt_invalid_string(self):
        assert parse_timecode("abc") == pytest.approx(0.0)