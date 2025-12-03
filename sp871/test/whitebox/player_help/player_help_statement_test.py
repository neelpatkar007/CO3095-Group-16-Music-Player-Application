import pytest

from music_player.player_help import print_help

@pytest.mark.parametrize(
    "cmd, expected_snippet",
    [
        ("/seek", "[Help] /seek"),
        ("rw", "[Help] /rw"),
        ("/ff", "[Help] /ff"),
        ("list", "[Help] /list"),
        ("/info", "[Help] /info"),
        ("progress", "[Help] /progress"),
        ("/bar", "[Help] /bar"),
        ("volume", "[Help] /volume"),
        ("/mute", "[Help] /mute"),
        ("unmute", "[Help] /unmute"),
        ("/quit", "[Help] /quit"),
    ],
)
def test_help_known_topics(cmd, expected_snippet, capsys):
    print_help(cmd)
    out = capsys.readouterr().out
    assert expected_snippet in out


def test_help_unknown_topic_else_branch(capsys):
    # Hits the final "else" branch: unknown command
    print_help("/definitely_not_a_command")
    out = capsys.readouterr().out
    assert "not recognised" in out
    assert "see the full list" in out

def test_stmt_help_no_command_prints_general_help(capsys):
    """
    Statement test:
    - Executes the branch where no command is provided.
    - Covers printing the general help header and list.
    """
    print_help()
    out = capsys.readouterr().out
    assert "Available Commands" in out
    assert "/play" in out
    assert "Shortcuts" in out


def test_stmt_help_specific_command_with_slash(capsys):
    """
    Statement test:
    - Executes the branch for a specific command that already
      starts with '/', such as '/play'.
    """
    print_help("/play")
    out = capsys.readouterr().out
    assert "[Help] /play" in out
    assert "Starts playback" in out


def test_stmt_help_specific_command_without_slash(capsys):
    """
    Statement test:
    - Executes the branch where a command is provided without '/'
      and must be normalized internally to '/pause'.
    """
    print_help("pause")
    out = capsys.readouterr().out
    assert "[Help] /pause" in out
    assert "Pauses the current song" in out


def test_stmt_help_unknown_command(capsys):
    """
    Statement test:
    - Executes the fallback branch for unknown commands.
    """
    print_help("madeup")
    out = capsys.readouterr().out

    assert "not recognised" in out
    assert "see the full list" in out