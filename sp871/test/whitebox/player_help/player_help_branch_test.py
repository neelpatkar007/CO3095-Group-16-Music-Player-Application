import pytest

from music_player.player_help import print_help


def test_branch_help_none_shows_general_help(capsys):
    """
        Branch Test: Default Null Path.
        Exercises the 'True' branch of the condition 'if command is None',
        verifying that the system defaults to the general command overview.
        """
    print_help()
    out = capsys.readouterr().out
    assert "Available Commands" in out


def test_branch_help_normalizes_command_without_slash(capsys):
    """
        Branch Test: Input Normalisation.
        Exercises the branch where a command string lacks a '/' prefix,
        verifying the logic that auto-prepends the slash for lookup consistency.
        """
    print_help("play")
    out = capsys.readouterr().out
    assert "[Help] /play" in out


def test_branch_help_known_command(capsys):
    """
        Branch Test: Successful Specification Lookup.
        Exercises the 'True' branch for a valid command search, ensuring the
        correct help data is retrieved from the internal dictionary.
        """
    print_help("/pause")
    out = capsys.readouterr().out
    assert "Pauses the current song" in out


def test_branch_help_unknown_command(capsys):
    """
        Branch Test: Error-Handling Path.
        Exercises the 'False' branch of the command lookup, verifying that the
        system provides a 'not recognised' message for invalid input.
        """
    print_help("xyz123")
    out = capsys.readouterr().out
    assert "not recognised" in out