"""Persistent face IDs across webcam frames (centroid + IoU matching)."""

from __future__ import annotations

from dataclasses import dataclass

from config import TRACKING_IOU_THRESHOLD, TRACKING_MAX_MISSING_FRAMES
from src.geometry import FaceBox


@dataclass
class TrackedFace:
    track_id: int
    box: FaceBox
    missing: int = 0


class FaceTracker:
    def __init__(self) -> None:
        self._tracks: dict[int, TrackedFace] = {}
        self._next_id = 1

    def update(self, detections: list[FaceBox]) -> list[tuple[int, FaceBox]]:
        if not detections:
            self._age_unmatched(set())
            return []

        unmatched_tracks = set(self._tracks.keys())
        unmatched_dets = set(range(len(detections)))
        assignments: dict[int, int] = {}

        pairs: list[tuple[float, int, int]] = []
        for tid, track in self._tracks.items():
            for di, det in enumerate(detections):
                score = track.box.iou(det)
                if score >= TRACKING_IOU_THRESHOLD:
                    pairs.append((score, tid, di))
        pairs.sort(reverse=True)

        used_tracks: set[int] = set()
        used_dets: set[int] = set()
        for _, tid, di in pairs:
            if tid in used_tracks or di in used_dets:
                continue
            assignments[tid] = di
            used_tracks.add(tid)
            used_dets.add(di)

        unmatched_tracks -= used_tracks
        unmatched_dets -= used_dets

        for tid, di in assignments.items():
            self._tracks[tid].box = detections[di]
            self._tracks[tid].missing = 0

        for di in unmatched_dets:
            tid = self._next_id
            self._next_id += 1
            self._tracks[tid] = TrackedFace(track_id=tid, box=detections[di])
            assignments[tid] = di

        self._age_unmatched(unmatched_tracks)

        return [(tid, detections[di]) for tid, di in assignments.items()]

    def _age_unmatched(self, unmatched: set[int]) -> None:
        dead: list[int] = []
        for tid in unmatched:
            track = self._tracks.get(tid)
            if not track:
                continue
            track.missing += 1
            if track.missing > TRACKING_MAX_MISSING_FRAMES:
                dead.append(tid)
        for tid in dead:
            self._tracks.pop(tid, None)

    def reset(self) -> None:
        self._tracks.clear()
        self._next_id = 1
