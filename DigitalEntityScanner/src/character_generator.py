"""Unique futuristic character profile assignment."""

from __future__ import annotations

from dataclasses import dataclass
import itertools
import random


THEMES = [
    {
        "name": "Entity Alpha",
        "theme": "Blue Digital Energy",
        "color": (255, 180, 40),  # BGR
        "accent": (255, 255, 120),
        "energy_pattern": "circuit",
        "eye_effect": "neon",
        "texture": "energy",
    },
    {
        "name": "Entity Beta",
        "theme": "Red Cybernetic",
        "color": (40, 40, 255),
        "accent": (80, 160, 255),
        "energy_pattern": "mask",
        "eye_effect": "plasma",
        "texture": "metallic",
    },
    {
        "name": "Entity Gamma",
        "theme": "Purple Neon",
        "color": (255, 40, 220),
        "accent": (255, 160, 255),
        "energy_pattern": "hologram",
        "eye_effect": "void",
        "texture": "neon",
    },
    {
        "name": "Entity Delta",
        "theme": "Green Metallic",
        "color": (80, 255, 80),
        "accent": (180, 255, 180),
        "energy_pattern": "circuit",
        "eye_effect": "scan",
        "texture": "metallic",
    },
    {
        "name": "Entity Epsilon",
        "theme": "Cyan Hologram",
        "color": (255, 255, 40),
        "accent": (255, 255, 200),
        "energy_pattern": "hologram",
        "eye_effect": "neon",
        "texture": "hologram",
    },
    {
        "name": "Entity Zeta",
        "theme": "Orange Plasma",
        "color": (20, 140, 255),
        "accent": (80, 220, 255),
        "energy_pattern": "energy",
        "eye_effect": "plasma",
        "texture": "energy",
    },
    {
        "name": "Entity Eta",
        "theme": "Magenta Circuit",
        "color": (180, 40, 255),
        "accent": (220, 140, 255),
        "energy_pattern": "circuit",
        "eye_effect": "void",
        "texture": "neon",
    },
    {
        "name": "Entity Theta",
        "theme": "Gold Chrome",
        "color": (40, 200, 255),
        "accent": (180, 240, 255),
        "energy_pattern": "mask",
        "eye_effect": "scan",
        "texture": "metallic",
    },
    {
        "name": "Entity Iota",
        "theme": "White Ice Digital",
        "color": (245, 245, 245),
        "accent": (255, 255, 255),
        "energy_pattern": "hologram",
        "eye_effect": "neon",
        "texture": "ice",
    },
    {
        "name": "Entity Kappa",
        "theme": "Teal Quantum",
        "color": (210, 200, 40),
        "accent": (255, 240, 120),
        "energy_pattern": "energy",
        "eye_effect": "scan",
        "texture": "energy",
    },
]


@dataclass
class Character:
    character_id: int
    name: str
    theme: str
    color: tuple[int, int, int]
    accent: tuple[int, int, int]
    energy_pattern: str
    eye_effect: str
    texture: str
    variation: int

    def label(self) -> str:
        return f"ENTITY #{self.character_id:03d}  {self.name}"


class CharacterGenerator:
    """Assigns a unique visual profile to each persistent face ID."""

    def __init__(self, seed: int | None = 7) -> None:
        self._rng = random.Random(seed)
        self._pool = list(range(len(THEMES)))
        self._rng.shuffle(self._pool)
        self._cycle = itertools.cycle(self._pool)
        self._assigned: dict[int, Character] = {}
        self._used_keys: set[tuple] = set()

    def assign(self, track_id: int) -> Character:
        if track_id in self._assigned:
            return self._assigned[track_id]

        theme = THEMES[next(self._cycle)].copy()
        variation = self._unique_variation(theme["name"])
        character = Character(
            character_id=track_id,
            name=theme["name"],
            theme=theme["theme"],
            color=theme["color"],
            accent=theme["accent"],
            energy_pattern=theme["energy_pattern"],
            eye_effect=theme["eye_effect"],
            texture=theme["texture"],
            variation=variation,
        )
        self._assigned[track_id] = character
        return character

    def _unique_variation(self, name: str) -> int:
        for _ in range(16):
            variation = self._rng.randint(1, 8)
            key = (name, variation)
            if key not in self._used_keys:
                self._used_keys.add(key)
                return variation
        return self._rng.randint(1, 8)

    def forget(self, track_id: int) -> None:
        self._assigned.pop(track_id, None)

    def all_assigned(self) -> list[Character]:
        return list(self._assigned.values())
