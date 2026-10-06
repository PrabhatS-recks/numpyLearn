"""Face-box geometry tests (no camera or MediaPipe required)."""

import unittest

from src.geometry import FaceBox


class FaceBoxTests(unittest.TestCase):
    def test_identical_boxes_have_full_iou(self):
        box = FaceBox(10, 10, 40, 40, 1.0)
        self.assertEqual(box.iou(box), 1.0)

    def test_separated_boxes_have_zero_iou(self):
        a = FaceBox(0, 0, 10, 10, 1.0)
        b = FaceBox(50, 50, 10, 10, 1.0)
        self.assertEqual(a.iou(b), 0.0)


if __name__ == "__main__":
    unittest.main()
