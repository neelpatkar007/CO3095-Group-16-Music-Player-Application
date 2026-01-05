import unittest
import io
import sys
from music_player.player_help import print_help

class TestConcolicExecution(unittest.TestCase):
    def setUp(self):
        self.held_output = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = self.original_stdout

    def test_iter_1_base_fallback(self):
        print_help("random_val")
        output = self.held_output.getvalue()
        self.assertIn("I couldn't find a command named '/random_val'", output)
        self.assertIn("Try '/help' to see the full list", output)

    def test_iter_2_quit(self):
        print_help("quit")
        output = self.held_output.getvalue()
        self.assertIn("[Help] /quit", output)
        self.assertIn("Saves your data and shuts down the app", output)

    def test_iter_3_schedule_cancel(self):
        print_help("schedule.cancel")
        output = self.held_output.getvalue()
        self.assertIn("[Help] /schedule.cancel", output)
        self.assertIn("Turns off any active playback alarms", output)

    def test_iter_4_stop(self):
        print_help("stop")
        output = self.held_output.getvalue()
        self.assertIn("[Help] /stop", output)
        self.assertIn("Stops the audio and winds the song back to the start", output)

    def test_iter_5_pause(self):
        print_help("pause")
        output = self.held_output.getvalue()
        self.assertIn("[Help] /pause", output)
        self.assertIn("Pauses the audio. Use /play to keep going", output)

    def test_iter_6_play(self):
        print_help("play")
        output = self.held_output.getvalue()
        self.assertIn("[Help] /play", output)
        self.assertIn("Starts the music. If a session was saved, it picks up from where you left off", output)

    def test_iter_7_normalization_robustness(self):
        print_help("/Play")
        output = self.held_output.getvalue()
        self.assertIn("[Help] /play", output)
        self.assertIn("Starts the music. If a session was saved, it picks up from where you left off", output)


if __name__ == '__main__':
    unittest.main()
