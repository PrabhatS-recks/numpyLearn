"""Procedural futuristic visual effects aligned to facial landmarks."""

from __future__ import annotations

import math

import cv2
import numpy as np

from config import SCAN_LINE_SPEED
from src.character_generator import Character
from src.face_landmarks import (
    CHIN,
    FOREHEAD,
    LEFT_EYE,
    LEFT_IRIS,
    MOUTH,
    NOSE_TIP,
    RIGHT_EYE,
    RIGHT_IRIS,
    FaceLandmarks,
)
from src.image_processor import (
    add_glow_layer,
    blend_overlay,
    face_mask,
    tint_region,
)


def apply_character_effects(
    frame: np.ndarray,
    landmarks: FaceLandmarks,
    character: Character,
    frame_index: int = 0,
) -> np.ndarray:
    out = frame.copy()
    mask = face_mask(out.shape[:2], landmarks.points)

    out = tint_region(out, mask, character.color, alpha=0.28)
    out = _apply_texture(out, mask, character)
    out = _apply_energy_pattern(out, landmarks, character, frame_index)
    out = apply_neon_eyes(out, landmarks, character)
    out = apply_energy_glow(out, landmarks, character, frame_index)
    out = _draw_scan_hud(out, landmarks, character, frame_index)
    return out


def apply_neon_eyes(
    frame: np.ndarray,
    landmarks: FaceLandmarks,
    character: Character,
) -> np.ndarray:
    glow = np.zeros_like(frame)
    style = character.eye_effect

    for iris_idx, eye_idx in ((LEFT_IRIS, LEFT_EYE), (RIGHT_IRIS, RIGHT_EYE)):
        iris = landmarks.subset(iris_idx)
        eye = landmarks.subset(eye_idx)
        if len(eye) == 0:
            continue
        if len(iris) > 0:
            cx, cy = iris.mean(axis=0)
        else:
            cx, cy = eye.mean(axis=0)
        width = max(6.0, (eye[:, 0].max() - eye[:, 0].min()) * 0.55)
        height = max(4.0, (eye[:, 1].max() - eye[:, 1].min()) * 0.85)
        center = (int(cx), int(cy))

        if style == "neon":
            cv2.ellipse(glow, center, (int(width), int(height)), 0, 0, 360, character.accent, -1)
            cv2.circle(glow, center, max(2, int(width * 0.25)), (255, 255, 255), -1)
        elif style == "plasma":
            cv2.ellipse(glow, center, (int(width * 1.2), int(height * 1.1)), 0, 0, 360, character.color, -1)
            cv2.ellipse(glow, center, (int(width * 0.5), int(height * 0.4)), 0, 0, 360, (255, 255, 255), -1)
        elif style == "void":
            cv2.ellipse(glow, center, (int(width), int(height)), 0, 0, 360, (10, 10, 10), -1)
            cv2.ellipse(glow, center, (int(width * 1.15), int(height * 1.15)), 0, 0, 360, character.accent, 2)
        else:  # scan
            cv2.ellipse(glow, center, (int(width), int(height)), 0, 0, 360, character.color, 2)
            cv2.line(
                glow,
                (int(cx - width), int(cy)),
                (int(cx + width), int(cy)),
                character.accent,
                2,
            )

    return add_glow_layer(frame, glow, 0.85)


def apply_circuit_pattern(
    frame: np.ndarray,
    landmarks: FaceLandmarks,
    character: Character,
) -> np.ndarray:
    overlay = np.zeros_like(frame)
    pts = landmarks.points
    step = 12 + (character.variation % 5)
    for i in range(0, min(len(pts), 300), step):
        a = pts[i]
        b = pts[(i + step * 3) % min(len(pts), 300)]
        p1 = (int(a[0]), int(a[1]))
        p2 = (int(b[0]), int(b[1]))
        cv2.line(overlay, p1, p2, character.color, 1, cv2.LINE_AA)
        cv2.circle(overlay, p1, 2, character.accent, -1)

    forehead = landmarks.get(FOREHEAD)
    nose = landmarks.get(NOSE_TIP)
    cv2.line(overlay, forehead, nose, character.accent, 2, cv2.LINE_AA)
    return add_glow_layer(frame, overlay, 0.55)


def apply_energy_glow(
    frame: np.ndarray,
    landmarks: FaceLandmarks,
    character: Character,
    frame_index: int,
) -> np.ndarray:
    overlay = np.zeros_like(frame)
    contour = landmarks.points[:468:4].astype(np.int32)
    if len(contour) >= 3:
        hull = cv2.convexHull(contour)
        pulse = 2 + (frame_index // 4 + character.variation) % 3
        cv2.polylines(overlay, [hull], True, character.color, pulse, cv2.LINE_AA)
        cv2.polylines(overlay, [hull], True, character.accent, 1, cv2.LINE_AA)
    return add_glow_layer(frame, overlay, 0.65)


def apply_metallic_effect(frame: np.ndarray, mask: np.ndarray, character: Character) -> np.ndarray:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    metal = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    metal = cv2.convertScaleAbs(metal, alpha=1.35, beta=18)
    tinted = tint_region(metal, mask, character.color, alpha=0.35)
    return blend_overlay(frame, tinted, mask, 0.42)


def _apply_texture(frame: np.ndarray, mask: np.ndarray, character: Character) -> np.ndarray:
    if character.texture == "metallic":
        return apply_metallic_effect(frame, mask, character)
    if character.texture == "ice":
        cooled = cv2.convertScaleAbs(frame, alpha=1.1, beta=12)
        return blend_overlay(frame, cooled, mask, 0.35)
    if character.texture in ("neon", "hologram"):
        boosted = cv2.convertScaleAbs(frame, alpha=1.15, beta=8)
        return blend_overlay(frame, boosted, mask, 0.25)
    return frame


def _apply_energy_pattern(
    frame: np.ndarray,
    landmarks: FaceLandmarks,
    character: Character,
    frame_index: int,
) -> np.ndarray:
    pattern = character.energy_pattern
    if pattern == "circuit":
        return apply_circuit_pattern(frame, landmarks, character)
    if pattern == "mask":
        return _cyber_mask(frame, landmarks, character)
    if pattern == "hologram":
        return _hologram_grid(frame, landmarks, character, frame_index)
    return _energy_streaks(frame, landmarks, character, frame_index)


def _cyber_mask(frame: np.ndarray, landmarks: FaceLandmarks, character: Character) -> np.ndarray:
    overlay = np.zeros_like(frame)
    jaw = landmarks.subset(list(range(0, 17)) + [FOREHEAD, CHIN])
    if len(jaw) >= 3:
        hull = cv2.convexHull(jaw.astype(np.int32))
        cv2.polylines(overlay, [hull], True, character.color, 3, cv2.LINE_AA)
    mouth = landmarks.subset(MOUTH)
    if len(mouth) >= 3:
        cv2.polylines(overlay, [mouth.astype(np.int32)], True, character.accent, 2, cv2.LINE_AA)
    nose = landmarks.get(NOSE_TIP)
    forehead = landmarks.get(FOREHEAD)
    cv2.line(overlay, forehead, nose, character.color, 2, cv2.LINE_AA)
    return add_glow_layer(frame, overlay, 0.6)


def _hologram_grid(
    frame: np.ndarray,
    landmarks: FaceLandmarks,
    character: Character,
    frame_index: int,
) -> np.ndarray:
    overlay = np.zeros_like(frame)
    x, y, w, h = landmarks.box.x, landmarks.box.y, landmarks.box.w, landmarks.box.h
    spacing = 10 + character.variation
    offset = (frame_index * 2) % spacing
    for gx in range(x, x + w, spacing):
        cv2.line(overlay, (gx, y), (gx, y + h), character.color, 1)
    for gy in range(y + offset, y + h, spacing):
        cv2.line(overlay, (x, gy), (x + w, gy), character.accent, 1)
    mask = face_mask(frame.shape[:2], landmarks.points)
    overlay = cv2.bitwise_and(overlay, overlay, mask=mask)
    return add_glow_layer(frame, overlay, 0.4)


def _energy_streaks(
    frame: np.ndarray,
    landmarks: FaceLandmarks,
    character: Character,
    frame_index: int,
) -> np.ndarray:
    overlay = np.zeros_like(frame)
    origin = landmarks.get(NOSE_TIP)
    count = 8 + character.variation
    radius = max(landmarks.box.w, landmarks.box.h) * 0.55
    for i in range(count):
        angle = (2 * math.pi * i / count) + (frame_index * 0.08)
        x2 = int(origin[0] + math.cos(angle) * radius)
        y2 = int(origin[1] + math.sin(angle) * radius)
        cv2.line(overlay, origin, (x2, y2), character.color, 1, cv2.LINE_AA)
    return add_glow_layer(frame, overlay, 0.45)


def _draw_scan_hud(
    frame: np.ndarray,
    landmarks: FaceLandmarks,
    character: Character,
    frame_index: int,
) -> np.ndarray:
    x, y, w, h = landmarks.box.xyxy[0], landmarks.box.y, landmarks.box.w, landmarks.box.h
    x2, y2 = x + w, y + h
    overlay = frame.copy()
    color = character.color
    cv2.rectangle(overlay, (x, y), (x2, y2), color, 1)
    tick = 12
    cv2.line(overlay, (x, y), (x + tick, y), color, 2)
    cv2.line(overlay, (x, y), (x, y + tick), color, 2)
    cv2.line(overlay, (x2, y), (x2 - tick, y), color, 2)
    cv2.line(overlay, (x2, y), (x2, y + tick), color, 2)
    cv2.line(overlay, (x, y2), (x + tick, y2), color, 2)
    cv2.line(overlay, (x, y2), (x, y2 - tick), color, 2)
    cv2.line(overlay, (x2, y2), (x2 - tick, y2), color, 2)
    cv2.line(overlay, (x2, y2), (x2, y2 - tick), color, 2)

    scan_y = y + ((frame_index * SCAN_LINE_SPEED) % max(1, h))
    cv2.line(overlay, (x, scan_y), (x2, scan_y), character.accent, 1)

    label = character.label()
    theme = f"{character.theme}  var-{character.variation}"
    cv2.putText(overlay, label, (x, max(18, y - 22)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
    cv2.putText(overlay, theme, (x, max(36, y - 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, character.accent, 1, cv2.LINE_AA)
    return cv2.addWeighted(overlay, 0.85, frame, 0.15, 0)
