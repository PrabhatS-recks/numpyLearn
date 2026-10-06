"""Facial landmarks via MediaPipe Face Mesh, with a geometric fallback."""

from __future__ import annotations

from dataclasses import dataclass, field

import cv2
import numpy as np

from config import (
    MAX_FACES,
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE,
    REFINE_LANDMARKS,
)
from src.geometry import FaceBox

try:
    import mediapipe as mp

    HAS_MEDIAPIPE = True
except ImportError:
    mp = None
    HAS_MEDIAPIPE = False


LEFT_IRIS = [468, 469, 470, 471, 472]
RIGHT_IRIS = [473, 474, 475, 476, 477]
LEFT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
RIGHT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
NOSE_TIP = 1
FOREHEAD = 10
CHIN = 152
MOUTH = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]


@dataclass
class FaceLandmarks:
    """Pixel-space landmarks for one face."""

    points: np.ndarray
    box: FaceBox
    connections: list[tuple[int, int]] = field(default_factory=list)

    def get(self, index: int) -> tuple[int, int]:
        if index >= len(self.points):
            return self.box.center
        x, y = self.points[index]
        return int(x), int(y)

    def subset(self, indices: list[int]) -> np.ndarray:
        valid = [i for i in indices if i < len(self.points)]
        return self.points[valid]

    def mean_point(self, indices: list[int]) -> tuple[int, int]:
        pts = self.subset(indices)
        if len(pts) == 0:
            return self.box.center
        mean = pts.mean(axis=0)
        return int(mean[0]), int(mean[1])


def approximate_landmarks(box: FaceBox) -> FaceLandmarks:
    """Estimate key facial points from a bounding box when Face Mesh is unavailable."""
    x, y, w, h = box.x, box.y, box.w, box.h
    points = np.zeros((478, 2), dtype=np.float32)
    for i in range(478):
        points[i] = (x + w / 2, y + h / 2)
    points[FOREHEAD] = (x + w * 0.50, y + h * 0.12)
    points[NOSE_TIP] = (x + w * 0.50, y + h * 0.52)
    points[CHIN] = (x + w * 0.50, y + h * 0.95)
    for i, t in enumerate(np.linspace(0.15, 0.85, len(LEFT_EYE))):
        points[LEFT_EYE[i]] = (x + w * (0.22 + 0.12 * (t - 0.15) / 0.7), y + h * 0.38)
    for i, t in enumerate(np.linspace(0.15, 0.85, len(RIGHT_EYE))):
        points[RIGHT_EYE[i]] = (x + w * (0.62 + 0.12 * (t - 0.15) / 0.7), y + h * 0.38)
    for i in LEFT_IRIS:
        points[i] = (x + w * 0.32, y + h * 0.38)
    for i in RIGHT_IRIS:
        points[i] = (x + w * 0.68, y + h * 0.38)
    for i, t in enumerate(np.linspace(0.30, 0.70, len(MOUTH))):
        points[MOUTH[i]] = (x + w * t, y + h * 0.74)
    oval = []
    for i, ang in enumerate(np.linspace(0, 2 * np.pi, 36, endpoint=False)):
        px = x + w * 0.5 + (w * 0.48) * np.cos(ang)
        py = y + h * 0.5 + (h * 0.52) * np.sin(ang)
        idx = min(i, 35)
        points[idx] = (px, py)
        oval.append((int(px), int(py)))
    return FaceLandmarks(points=points, box=box)


class LandmarkDetector:
    def __init__(self) -> None:
        self._mesh = None
        self._connections: list[tuple[int, int]] = []
        self._static = False
        if HAS_MEDIAPIPE:
            self._build_mesh(static_image_mode=False)
        else:
            print("MediaPipe is not installed. Using approximate facial landmarks.")

    def _build_mesh(self, static_image_mode: bool) -> None:
        self._mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=static_image_mode,
            max_num_faces=MAX_FACES,
            refine_landmarks=REFINE_LANDMARKS,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
        )
        self._connections = list(mp.solutions.face_mesh.FACEMESH_TESSELATION)

    def set_static_image_mode(self, enabled: bool) -> None:
        self._static = enabled
        if self._mesh is None:
            return
        self._mesh.close()
        self._build_mesh(static_image_mode=enabled)

    def detect(self, frame_bgr: np.ndarray, boxes: list[FaceBox] | None = None) -> list[FaceLandmarks]:
        if self._mesh is None:
            return [approximate_landmarks(box) for box in (boxes or [])]

        h, w = frame_bgr.shape[:2]
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        result = self._mesh.process(rgb)
        if not result.multi_face_landmarks:
            return [approximate_landmarks(box) for box in (boxes or [])]

        faces: list[FaceLandmarks] = []
        for mesh in result.multi_face_landmarks:
            pts = np.array(
                [(lm.x * w, lm.y * h) for lm in mesh.landmark],
                dtype=np.float32,
            )
            xs, ys = pts[:, 0], pts[:, 1]
            x1, y1 = int(max(0, xs.min())), int(max(0, ys.min()))
            x2, y2 = int(min(w, xs.max())), int(min(h, ys.max()))
            box = FaceBox(x=x1, y=y1, w=max(1, x2 - x1), h=max(1, y2 - y1), score=1.0)
            faces.append(FaceLandmarks(points=pts, box=box, connections=self._connections))
        return faces

    def close(self) -> None:
        if self._mesh is not None:
            self._mesh.close()
