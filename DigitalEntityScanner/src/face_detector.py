"""Multi-face detection: MediaPipe when available, OpenCV Haar fallback."""

from __future__ import annotations

import cv2
import numpy as np

from config import MAX_FACES, MIN_DETECTION_CONFIDENCE
from src.geometry import FaceBox

try:
    import mediapipe as mp

    HAS_MEDIAPIPE = True
except ImportError:
    mp = None
    HAS_MEDIAPIPE = False


class FaceDetector:
    def __init__(self) -> None:
        self._mp_detector = None
        self._haar = None
        if HAS_MEDIAPIPE:
            self._mp_detector = mp.solutions.face_detection.FaceDetection(
                model_selection=1,
                min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            )
        else:
            cascade = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            self._haar = cv2.CascadeClassifier(cascade)
            if self._haar.empty():
                raise RuntimeError("Face detector could not load Haar cascade.")
            print("MediaPipe is not installed. Using OpenCV Haar face detection.")

    def detect(self, frame_bgr: np.ndarray) -> list[FaceBox]:
        if self._mp_detector is not None:
            return self._detect_mediapipe(frame_bgr)
        return self._detect_haar(frame_bgr)

    def _detect_mediapipe(self, frame_bgr: np.ndarray) -> list[FaceBox]:
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        result = self._mp_detector.process(rgb)
        if not result.detections:
            return []

        h, w = frame_bgr.shape[:2]
        boxes: list[FaceBox] = []
        for det in result.detections[:MAX_FACES]:
            loc = det.location_data.relative_bounding_box
            x = max(0, int(loc.xmin * w))
            y = max(0, int(loc.ymin * h))
            bw = min(w - x, int(loc.width * w))
            bh = min(h - y, int(loc.height * h))
            if bw < 8 or bh < 8:
                continue
            score = float(det.score[0]) if det.score else 0.0
            boxes.append(FaceBox(x=x, y=y, w=bw, h=bh, score=score))
        return boxes

    def _detect_haar(self, frame_bgr: np.ndarray) -> list[FaceBox]:
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        raw = self._haar.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=5, minSize=(40, 40))
        boxes = []
        for (x, y, w, h) in list(raw)[:MAX_FACES]:
            boxes.append(FaceBox(x=int(x), y=y, w=int(w), h=int(h), score=1.0))
        return boxes

    def close(self) -> None:
        if self._mp_detector is not None:
            self._mp_detector.close()
