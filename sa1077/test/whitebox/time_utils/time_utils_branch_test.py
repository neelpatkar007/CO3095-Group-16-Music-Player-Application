import pytest

from music_player.time_utils import format_mm_ss, parse_timecode


class TestFormatMmSsBranch:
    """
        Branch Testing suite for the time formatter.
        Aims for 100% decision coverage of the time-to-string conversion logic.
        """
    def test_branch_none_returns_question_marks(self):
        # Branch B1: Verifying the 'if duration is None' early-exit path.
        assert format_mm_ss(None) == "??:??"

    def test_branch_negative_returns_question_marks(self):
        # Branch B2: Decision logic for invalid negative durations (Lower Boundary).
        assert format_mm_ss(-1) == "??:??"

    def test_branch_zero_boundary(self):
        # Branch B3: Critical boundary check for 0.0 seconds (The 'Happy Path' floor).
        assert format_mm_ss(0) == "00:00"

    def test_branch_normal_positive_value(self):
        # Branch B4: Standard execution path for positive floats involving mm:ss calculation.
        assert format_mm_ss(90.7) == "01:30"

class TestParseTimecodeBranch:
    """
        Branch Testing for the timecode parser.
        Ensures all conditional sanitisation and formatting logic is fully traversed.
        """
    def test_branch_empty_string(self):
        # Branch B5: Handling the 'if not string' branch to prevent parsing errors on empty input.
        assert parse_timecode("") == pytest.approx(0.0)

    def test_branch_plain_seconds(self):
        # Branch B6: The numeric-only branch (e.g., '42' string to 42.0 float).
        assert parse_timecode("42") == pytest.approx(42.0)

    def test_branch_mm_ss_valid(self):
        # Branch B7: The standard 'mm:ss' parsing path involving the colon-split logic.
        assert parse_timecode("01:30") == pytest.approx(90.0)

    def test_branch_mm_ss_with_spaces(self):
        # Branch B8: Verifying the branch that handles whitespace trimming during parsing.
        assert parse_timecode("  2:05  ") == pytest.approx(125.0)

    def test_branch_mm_ss_malformed_extra_colon(self):
        # Branch B9: Error-trapping branch for invalid formats (e.g., too many colons).
        assert parse_timecode("1:2:3") == pytest.approx(0.0)

    def test_branch_invalid_random_string(self):
        # Branch B10: Resilience check for the ValueError exception path during float conversion.
        assert parse_timecode("xVSd6\tE") == pytest.approx(0.0)

    def test_branch_negative_number_clamped_to_zero(self):
        # Branch B11: Logical branch ensuring negative timecodes are clamped to 0.0.
        assert parse_timecode("-10") == pytest.approx(0.0)

    def test_branch_bytes_input(self):
        # Branch B12: Robustness branch that catches and rejects non-string (bytes) input.
        assert parse_timecode(b"M") == pytest.approx(0.0)
