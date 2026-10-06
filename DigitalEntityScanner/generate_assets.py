"""Create simple transparent overlay PNGs used by the effect engine."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ASSETS = Path(__file__).resolve().parent / "assets" / "overlays"


def _save_rgba(name: str, array: np.ndarray) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    Image.fromarray(array, mode="RGBA").save(ASSETS / name)


def generate_neon_eyes() -> None:
    size = 256
    img = np.zeros((size, size, 4), dtype=np.uint8)
    yy, xx = np.ogrid[:size, :size]
    cx = cy = size / 2
    r = np.sqrt((xx - cx) ** 2 + ((yy - cy) * 1.6) ** 2)
    glow = np.clip(255 * np.exp(-((r - 40) ** 2) / 400), 0, 255).astype(np.uint8)
    img[:, :, 0] = 80
    img[:, :, 1] = 220
    img[:, :, 2] = 255
    img[:, :, 3] = glow
    _save_rgba("neon_eyes.png", img)


def generate_circuit_pattern() -> None:
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    color = (40, 255, 210, 200)
    for i in range(16, size, 32):
        draw.line((i, 20, i, size - 20), fill=color, width=2)
        draw.line((20, i, size - 20, i), fill=color, width=2)
        draw.ellipse((i - 3, i - 3, i + 3, i + 3), fill=(180, 255, 255, 230))
    ASSETS.mkdir(parents=True, exist_ok=True)
    img.save(ASSETS / "circuit_pattern.png")


def generate_energy_effect() -> None:
    size = 256
    img = np.zeros((size, size, 4), dtype=np.uint8)
    yy, xx = np.ogrid[:size, :size]
    cx = cy = size / 2
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    ring = np.clip(255 * np.exp(-((r - 90) ** 2) / 250), 0, 255).astype(np.uint8)
    img[:, :, 0] = 255
    img[:, :, 1] = 120
    img[:, :, 2] = 40
    img[:, :, 3] = ring
    _save_rgba("energy_effect.png", img)


def generate_all() -> None:
    generate_neon_eyes()
    generate_circuit_pattern()
    generate_energy_effect()


if __name__ == "__main__":
    generate_all()
    print(f"Wrote overlay assets to {ASSETS}")
