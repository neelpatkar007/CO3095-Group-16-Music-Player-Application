import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from music_player import library


class TestLibraryBranch(unittest.TestCase):
    """
    White-Box Branch Testing for library.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Branch Testing (White-Box)
    """

