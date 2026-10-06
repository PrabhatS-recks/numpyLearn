"""Cropping, resizing, masking, and blending helpers."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def load_image(path: str | Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return image


def save_image(path: str | Path, image: np.ndarray) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), image)


def face_mask(shape_hw: tuple[int, int], points: np.ndarray) -> np.ndarray:
    h, w = shape_hw
    mask = np.zeros((h, w), dtype=np.uint8)
    if len(points) == 0:
        return mask
    hull = cv2.convexHull(points[: min(468, len(points))].astype(np.int32))
    cv2.fillConvexPoly(mask, hull, 255)
    mask = cv2.GaussianBlur(mask, (21, 21), 0)
    return mask


def blend_overlay(
    base: np.ndarray,
    overlay: np.ndarray,
    mask: np.ndarray,
    alpha: float,
) -> np.ndarray:
    mask_f = (mask.astype(np.float32) / 255.0) * alpha
    if mask_f.ndim == 2:
        mask_f = mask_f[:, :, None]
    return (base * (1.0 - mask_f) + overlay * mask_f).astype(np.uint8)


def add_glow_layer(base: np.ndarray, glow: np.ndarray, strength: float = 0.7) -> np.ndarray:
    blurred = cv2.GaussianBlur(glow, (0, 0), 4)
    combined = cv2.addWeighted(glow, 0.65, blurred, 0.85, 0)
    return cv2.addWeighted(base, 1.0, combined, strength, 0)


def tint_region(
    frame: np.ndarray,
    mask: np.ndarray,
    color_bgr: tuple[int, int, int],
    alpha: float,
) -> np.ndarray:
    tint = np.zeros_like(frame)
    tint[:] = color_bgr
    return blend_overlay(frame, tint, mask, alpha)


def overlay_png(
    frame: np.ndarray,
    png_path: str | Path,
    center: tuple[int, int],
    size: tuple[int, int],
    alpha_scale: float = 1.0,
) -> np.ndarray:
    """Blend a transparent PNG onto the frame around a center point."""
    path = Path(png_path)
    if not path.exists():
        return frame
    rgba = np.array(Image.open(path).convert("RGBA"))
    resized = cv2.resize(rgba, size, interpolation=cv2.INTER_AREA)
    bh, bw = resized.shape[:2]
    cx, cy = center
    x1, y1 = cx - bw // 2, cy - bh // 2
    x2, y2 = x1 + bw, y1 + bh
    fh, fw = frame.shape[:2]
    fx1, fy1 = max(0, x1), max(0, y1)
    fx2, fy2 = min(fw, x2), min(fh, y2)
    if fx1 >= fx2 or fy1 >= fy2:
        return frame
    ox1, oy1 = fx1 - x1, fy1 - y1
    ox2, oy2 = ox1 + (fx2 - fx1), oy1 + (fy2 - fy1)
    roi = frame[fy1:fy2, fx1:fx2]
    patch = resized[oy1:oy2, ox1:ox2]
    alpha = (patch[:, :, 3:4].astype(np.float32) / 255.0) * alpha_scale
    rgb = cv2.cvtColor(patch[:, :, :3], cv2.COLOR_RGB2BGR)
    blended = roi.astype(np.float32) * (1 - alpha) + rgb.astype(np.float32) * alpha
    frame[fy1:fy2, fx1:fx2] = blended.astype(np.uint8)
    return frame
