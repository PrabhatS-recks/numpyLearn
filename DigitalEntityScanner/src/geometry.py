"""Shared geometry types (no heavy CV imports)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FaceBox:
    """Axis-aligned face bounding box in pixel coordinates."""

    x: int
    y: int
    w: int
    h: int
    score: float

    @property
    def center(self) -> tuple[int, int]:
        return (self.x + self.w // 2, self.y + self.h // 2)

    @property
    def xyxy(self) -> tuple[int, int, int, int]:
        return (self.x, self.y, self.x + self.w, self.y + self.h)

    def iou(self, other: "FaceBox") -> float:
        ax1, ay1, ax2, ay2 = self.xyxy
        bx1, by1, bx2, by2 = other.xyxy
        ix1, iy1 = max(ax1, bx1), max(ay1, by1)
        ix2, iy2 = min(ax2, bx2), min(ay2, by2)
        inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
        union = self.w * self.h + other.w * other.h - inter
        return inter / union if union else 0.0
