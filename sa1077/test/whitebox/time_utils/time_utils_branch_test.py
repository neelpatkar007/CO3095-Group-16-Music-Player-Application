import pytest

from music_player.time_utils import format_mm_ss, parse_timecode


class TestFormatMmSsBranch:
    def test_branch_none_returns_question_marks(self):
        assert format_mm_ss(None) == "??:??"

    def test_branch_negative_returns_question_marks(self):
        assert format_mm_ss(-1) == "??:??"

    def test_branch_zero_boundary(self):
        assert format_mm_ss(0) == "00:00"

    def test_branch_normal_positive_value(self):
        assert format_mm_ss(90.7) == "01:30"

class TestParseTimecodeBranch:
    def test_branch_empty_string(self):
        assert parse_timecode("") == pytest.approx(0.0)

    def test_branch_plain_seconds(self):
        assert parse_timecode("42") == pytest.approx(42.0)

    def test_branch_mm_ss_valid(self):
        assert parse_timecode("01:30") == pytest.approx(90.0)

    def test_branch_mm_ss_with_spaces(self):
        assert parse_timecode("  2:05  ") == pytest.approx(125.0)

    def test_branch_mm_ss_malformed_extra_colon(self):
        assert parse_timecode("1:2:3") == pytest.approx(0.0)

    def test_branch_invalid_random_string(self):
        assert parse_timecode("xVSd6\tE") == pytest.approx(0.0)

    def test_branch_negative_number_clamped_to_zero(self):
        assert parse_timecode("-10") == pytest.approx(0.0)

    def test_branch_bytes_input(self):
        assert parse_timecode(b"M") == pytest.approx(0.0)
