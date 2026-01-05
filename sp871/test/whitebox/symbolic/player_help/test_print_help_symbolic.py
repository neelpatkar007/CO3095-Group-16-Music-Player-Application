import unittest
import io
import sys
from music_player.player_help import print_help

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.held_output = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = self.original_stdout

    def assertOutputContains(self, substring):
        output = self.held_output.getvalue()
        self.assertIn(substring, output)

    def test_PC_1_none(self):
        print_help(None)
        self.assertOutputContains("--- Music Player: Help Menu ---")

    def test_PC_1_empty_string(self):
        print_help("")
        self.assertOutputContains("--- Music Player: Help Menu ---")

    def test_PC_2_play(self):
        print_help("play")
        self.assertOutputContains("[Help] /play")

    def test_PC_3_pause(self):
        print_help("pause")
        self.assertOutputContains("[Help] /pause")

    def test_PC_4_stop(self):
        print_help("stop")
        self.assertOutputContains("[Help] /stop")

    def test_PC_5_next(self):
        print_help("next")
        self.assertOutputContains("[Help] /next")

    def test_PC_6_prev(self):
        print_help("prev")
        self.assertOutputContains("[Help] /prev")

    def test_PC_7_seek(self):
        print_help("seek")
        self.assertOutputContains("[Help] /seek")

    def test_PC_8_rw(self):
        print_help("rw")
        self.assertOutputContains("[Help] /rw")

    def test_PC_9_ff(self):
        print_help("ff")
        self.assertOutputContains("[Help] /ff")

    def test_PC_10_volume(self):
        print_help("volume")
        self.assertOutputContains("[Help] /volume")

    def test_PC_10_vol_alias(self):
        print_help("vol")
        self.assertOutputContains("[Help] /volume")

    def test_PC_11_mute(self):
        print_help("mute")
        self.assertOutputContains("[Help] /mute")

    def test_PC_12_unmute(self):
        print_help("unmute")
        self.assertOutputContains("[Help] /unmute")

    def test_PC_13_shuffle(self):
        print_help("shuffle")
        self.assertOutputContains("[Help] /shuffle")

    def test_PC_14_loop(self):
        print_help("loop")
        self.assertOutputContains("[Help] /loop")

    def test_PC_15_queue(self):
        print_help("queue")
        self.assertOutputContains("[Help] /queue")

    # Tests for Remaining Branches
    def test_sprint4_search(self):
        print_help("search")
        self.assertOutputContains("[Help] /search")

    def test_playlist_pl_new(self):
        print_help("pl.new")
        self.assertOutputContains("[Help] /pl.new")

    def test_system_quit(self):
        print_help("quit")
        self.assertOutputContains("[Help] /quit")

    def test_PC_ELSE_unknown(self):
        print_help("unknown_command")
        self.assertOutputContains("I couldn't find a command named '/unknown_command'")

if __name__ == '__main__':
    unittest.main()
