import pytest

from music_player.time_utils import format_mm_ss, parse_timecode


# Test: A suite of tests to check the time formatter logic
class TestFormatMmSsBranch:

    # Test: ensuring the system shows '??:??' if the time data is missing (None)
    def test_branch_none_returns_question_marks(self):
        assert format_mm_ss(None) == "??:??"

    # Test: ensuring the system shows '??:??' if the time value provided is a negative number
    def test_branch_negative_returns_question_marks(self):
        assert format_mm_ss(-1) == "??:??"

    # Test: verifying that exactly zero seconds is correctly formatted as '00:00'
    def test_branch_zero_boundary(self):
        assert format_mm_ss(0) == "00:00"

    # Test: checking that a normal number of seconds is converted correctly to minutes and seconds
    def test_branch_normal_positive_value(self):
        assert format_mm_ss(90.7) == "01:30"


# Test: A suite of tests to check the timecode parser logic
class TestParseTimecodeBranch:

    # Test: ensuring that an empty input string defaults back to zero seconds safely
    def test_branch_empty_string(self):
        assert parse_timecode("") == pytest.approx(0.0)

    # Test: verifying that a simple number string is correctly converted into a decimal number
    def test_branch_plain_seconds(self):
        assert parse_timecode("42") == pytest.approx(42.0)

    # Test: checking that the standard 'minutes:seconds' format is parsed into the correct total seconds
    def test_branch_mm_ss_valid(self):
        assert parse_timecode("01:30") == pytest.approx(90.0)

    # Test: ensuring the system can handle and ignore extra spaces typed around the time input
    def test_branch_mm_ss_with_spaces(self):
        assert parse_timecode("  2:05  ") == pytest.approx(125.0)

    # Test: checking that the system resets to zero if the time format is broken (e.g. too many colons)
    def test_branch_mm_ss_malformed_extra_colon(self):
        assert parse_timecode("1:2:3") == pytest.approx(0.0)

    # Test: ensuring the system stays stable and defaults to zero if random text is entered
    def test_branch_invalid_random_string(self):
        assert parse_timecode("xVSd6\tE") == pytest.approx(0.0)

    # Test: verifying that negative time inputs are automatically clamped to zero
    def test_branch_negative_number_clamped_to_zero(self):
        assert parse_timecode("-10") == pytest.approx(0.0)

    # Test: checking that raw data (bytes) is rejected safely and defaults the time to zero
    def test_branch_bytes_input(self):
        assert parse_timecode(b"M") == pytest.approx(0.0)