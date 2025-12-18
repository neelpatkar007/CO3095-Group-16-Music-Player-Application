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
    """
        Specification Test: Parameterised Command Verification.
        Uses Equivalence Partitioning (EP) to verify that all primary command strings
        retrieve their corresponding documentation snippets correctly.
        """
    print_help(cmd)
    out = capsys.readouterr().out
    assert expected_snippet in out


def test_help_unknown_topic_else_branch(capsys):
    """
        Statement Test: Logic Fallback Path.
        Specifically targets the final 'else' statement to ensure the system
        provides helpful feedback when a command is not recognised.
        """
    print_help("/definitely_not_a_command")
    out = capsys.readouterr().out
    assert "not recognised" in out
    assert "see the full list" in out

def test_stmt_help_no_command_prints_general_help(capsys):
    """
        Statement Test: Default General Path.
        Executes the initial lines of the function responsible for displaying
        the full command library and header.
        """
    print_help()
    out = capsys.readouterr().out
    assert "Available Commands" in out
    assert "/play" in out
    assert "Shortcuts" in out


def test_stmt_help_specific_command_with_slash(capsys):
    """
        Statement Test: Standard Command Lookup.
        Executes the execution path for commands already starting with '/',
        verifying standard dictionary lookup logic.
        """
    print_help("/play")
    out = capsys.readouterr().out
    assert "[Help] /play" in out
    assert "Starts playback" in out


def test_stmt_help_specific_command_without_slash(capsys):
    """
        Statement Test: Input Normalisation logic.
        Executes the code lines that detect a missing '/' prefix and
        automatically format the string for a successful lookup.
        """
    print_help("pause")
    out = capsys.readouterr().out
    assert "[Help] /pause" in out
    assert "Pauses the current song" in out


def test_stmt_help_unknown_command(capsys):
    """
        Statement Test: Robustness Handling.
        Ensures that unrecognised alphanumeric strings are safely processed
        by the error-trapping lines of the function.
        """
    print_help("madeup")
    out = capsys.readouterr().out

    assert "not recognised" in out
    assert "see the full list" in out