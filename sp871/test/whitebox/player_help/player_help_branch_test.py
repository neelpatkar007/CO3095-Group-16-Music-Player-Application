import pytest

from music_player.player_help import print_help

# Test: checking if the general command list is shown when no specific help is requested
def test_branch_help_none_shows_general_help(capsys):
    print_help()
    out = capsys.readouterr().out
    assert "Available Commands" in out


# Test: verifying that the system automatically adds a slash to the command if the user leaves it out
def test_branch_help_normalizes_command_without_slash(capsys):
    print_help("play")
    out = capsys.readouterr().out
    assert "[Help] /play" in out


# Test: confirming that the system correctly finds and displays help text for a valid command
def test_branch_help_known_command(capsys):
    print_help("/pause")
    out = capsys.readouterr().out
    assert "Pauses the current song" in out


# Test: ensuring the system handles unrecognised commands by showing a clear error message
def test_branch_help_unknown_command(capsys):
    print_help("xyz123")
    out = capsys.readouterr().out
    assert "not recognised" in out