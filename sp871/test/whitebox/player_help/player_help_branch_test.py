import pytest

from music_player.player_help import print_help


def test_branch_help_none_shows_general_help(capsys):
    """
    Branch test:
    - Forces branch where command is None.
    - This is the True branch of: if command is None.
    """
    print_help()
    out = capsys.readouterr().out
    assert "Available Commands" in out


def test_branch_help_normalizes_command_without_slash(capsys):
    """
    Branch test:
    - Forces the branch where the command does NOT start with '/',
      hitting: if not command.startswith("/"): command = "/" + command
    """
    print_help("play")
    out = capsys.readouterr().out
    assert "[Help] /play" in out


def test_branch_help_known_command(capsys):
    """
    Branch test:
    - Forces the True branch of: if cmd in HELP_DATA.
    """
    print_help("/pause")
    out = capsys.readouterr().out
    assert "Pauses the current song" in out


def test_branch_help_unknown_command(capsys):
    """
    Branch test:
    - Forces the False branch of: if cmd in HELP_DATA,
      hitting the 'unknown command' message.
    """
    print_help("xyz123")
    out = capsys.readouterr().out
    assert "not recognised" in out