import unittest
from unittest.mock import MagicMock, patch
from music_player import player_seek
from music_player.player_state import PlayerState
from music_player.library import Track