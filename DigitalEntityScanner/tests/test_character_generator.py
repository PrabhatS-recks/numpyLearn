"""Tests for unique character assignment (no camera required)."""

import unittest

from src.character_generator import CharacterGenerator, THEMES
from src.geometry import FaceBox


class CharacterGeneratorTests(unittest.TestCase):
    def test_each_face_gets_a_distinct_theme_for_first_wave(self):
        gen = CharacterGenerator(seed=1)
        names = [gen.assign(i).name for i in range(1, len(THEMES) + 1)]
        self.assertEqual(len(names), len(set(names)))

    def test_same_track_keeps_same_character(self):
        gen = CharacterGenerator(seed=2)
        first = gen.assign(7)
        again = gen.assign(7)
        self.assertEqual(first, again)

    def test_iou_overlap(self):
        a = FaceBox(0, 0, 100, 100, 1.0)
        b = FaceBox(50, 0, 100, 100, 1.0)
        self.assertGreater(a.iou(b), 0.3)
        self.assertLess(a.iou(b), 0.4)


if __name__ == "__main__":
    unittest.main()
