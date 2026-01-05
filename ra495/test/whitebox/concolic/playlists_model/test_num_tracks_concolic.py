import unittest



class TestNumTracksConcolic(unittest.TestCase):

    class SystemUnderTest:

        @property
        def num_tracks(self) -> int:
            return len(self.tracks)

    def test_iter1_concrete_empty(self):

        sut = self.SystemUnderTest()
        sut.tracks = []  # S1 Concrete Seed 1

        result = sut.num_tracks

        self.assertEqual(result, 0, "Concolic Iteration 1 failed: Expected length 0 for empty S1.")

    def test_iter2_concrete_pop(self):
        sut = self.SystemUnderTest()
        sut.tracks = ["Song A", "Song B"]  # S1 Concrete Seed 2

        result = sut.num_tracks

        self.assertEqual(result, 2, "Concolic Iteration 2 failed: Expected length 2 for populated S1.")


if __name__ == '__main__':
    unittest.main()