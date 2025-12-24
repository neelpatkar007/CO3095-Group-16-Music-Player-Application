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
# Test: verifying that the help system correctly finds and shows documentation for all known commands
def test_help_known_topics(cmd, expected_snippet, capsys):
    print_help(cmd)
    out = capsys.readouterr().out
    assert expected_snippet in out


# Test: ensuring that unrecognised commands trigger a helpful error message and a link to the full list
def test_help_unknown_topic_else_branch(capsys):
    print_help("/definitely_not_a_command")
    out = capsys.readouterr().out
    assert "not recognised" in out
    assert "see the full list" in out

# Test: checking that the general list of commands is printed when help is called with no arguments
def test_stmt_help_no_command_prints_general_help(capsys):
    print_help()
    out = capsys.readouterr().out
    assert "Available Commands" in out
    assert "/play" in out
    assert "Shortcuts" in out


# Test: verifying that the help lookup works correctly when a slash is already included in the command
def test_stmt_help_specific_command_with_slash(capsys):
    print_help("/play")
    out = capsys.readouterr().out
    assert "[Help] /play" in out
    assert "Starts playback" in out


# Test: checking that the system automatically adds a slash to the name if the user forgets to type it
def test_stmt_help_specific_command_without_slash(capsys):
    print_help("pause")
    out = capsys.readouterr().out
    assert "[Help] /pause" in out
    assert "Pauses the current song" in out


# Test: ensuring the system stays stable and handles random text inputs by using a safe error path
def test_stmt_help_unknown_command(capsys):
    print_help("madeup")
    out = capsys.readouterr().out

    assert "not recognised" in out
    assert "see the full list" in out