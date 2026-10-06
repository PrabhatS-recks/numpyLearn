"""
Digital Entity Scanner
Multi-face detection and unique futuristic character transformation.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import CAMERA_INDEX, ENABLE_TRACKING, OUTPUT_DIR, WINDOW_NAME
from generate_assets import generate_all
from src.character_generator import CharacterGenerator
from src.effects import apply_character_effects
from src.face_detector import FaceDetector
from src.geometry import FaceBox
from src.face_landmarks import FaceLandmarks, LandmarkDetector
from src.face_tracker import FaceTracker
from src.image_processor import load_image, save_image


def _match_landmarks(box: FaceBox, meshes: list[FaceLandmarks]) -> FaceLandmarks | None:
    best: FaceLandmarks | None = None
    best_score = 0.05
    for mesh in meshes:
        score = box.iou(mesh.box)
        if score > best_score:
            best = mesh
            best_score = score
    return best


def _draw_global_hud(frame: np.ndarray, status: str, entity_count: int) -> np.ndarray:
    overlay = frame.copy()
    h, w = frame.shape[:2]
    cv2.rectangle(overlay, (0, 0), (w, 70), (10, 8, 20), -1)
    cv2.putText(
        overlay,
        "DIGITAL ENTITY SCANNER",
        (16, 28),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (80, 255, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        overlay,
        f"{status}    |    ENTITIES LOCKED: {entity_count}",
        (16, 54),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (180, 220, 255),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        overlay,
        "Q quit   S save   R reassign",
        (16, h - 16),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (160, 160, 180),
        1,
        cv2.LINE_AA,
    )
    return cv2.addWeighted(overlay, 0.72, frame, 0.28, 0)


def process_frame(
    frame: np.ndarray,
    detector: FaceDetector,
    landmarks: LandmarkDetector,
    tracker: FaceTracker,
    characters: CharacterGenerator,
    frame_index: int,
    persist: bool,
) -> np.ndarray:
    detections = detector.detect(frame)
    meshes = landmarks.detect(frame, detections)

    if persist and ENABLE_TRACKING:
        tracked = tracker.update(detections)
    else:
        tracked = [(i + 1, box) for i, box in enumerate(detections)]

    rendered = frame.copy()
    for track_id, box in tracked:
        mesh = _match_landmarks(box, meshes)
        character = characters.assign(track_id)
        if mesh is None:
            cv2.rectangle(rendered, (box.x, box.y), (box.x + box.w, box.y + box.h), character.color, 2)
            cv2.putText(
                rendered,
                character.label(),
                (box.x, max(20, box.y - 8)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                character.color,
                1,
                cv2.LINE_AA,
            )
            continue
        rendered = apply_character_effects(rendered, mesh, character, frame_index)

    status = "SCANNING..." if tracked else "AWAITING SUBJECTS"
    if tracked:
        status = f"{len(tracked)} ENTITY SIGNAL(S) DETECTED"
    return _draw_global_hud(rendered, status, len(tracked))


def run_image(image_path: str, save: bool) -> None:
    generate_all()
    image = load_image(image_path)
    detector = FaceDetector()
    landmarks = LandmarkDetector()
    landmarks.set_static_image_mode(True)
    tracker = FaceTracker()
    characters = CharacterGenerator()

    print("INITIALIZING DIGITAL ENTITY SCANNER...")
    print("SCANNING...")
    output = process_frame(image, detector, landmarks, tracker, characters, 24, persist=False)

    for character in characters.all_assigned():
        print(f"{character.label()}  ->  {character.theme}")

    detector.close()
    landmarks.close()

    if save:
        out_path = Path(OUTPUT_DIR) / f"scan_{Path(image_path).stem}.png"
        save_image(out_path, output)
        print(f"Saved {out_path}")

    cv2.imshow(WINDOW_NAME, output)
    print("Press any key in the window to close.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def run_webcam(camera_index: int, save_dir: Path) -> None:
    generate_all()
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open webcam index {camera_index}")

    detector = FaceDetector()
    landmarks = LandmarkDetector()
    tracker = FaceTracker()
    characters = CharacterGenerator()

    print("INITIALIZING DIGITAL ENTITY SCANNER...")
    frame_index = 0
    save_dir.mkdir(parents=True, exist_ok=True)

    while True:
        ok, frame = cap.read()
        if not ok:
            print("Webcam frame not available.")
            break
        frame = cv2.flip(frame, 1)
        output = process_frame(
            frame, detector, landmarks, tracker, characters, frame_index, persist=True
        )
        cv2.imshow(WINDOW_NAME, output)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27):
            break
        if key == ord("s"):
            path = save_dir / f"webcam_{int(time.time())}.png"
            save_image(path, output)
            print(f"Saved {path}")
        if key == ord("r"):
            tracker.reset()
            characters = CharacterGenerator(seed=int(time.time()))
            print("Character profiles reassigned.")
        frame_index += 1

    cap.release()
    detector.close()
    landmarks.close()
    cv2.destroyAllWindows()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect multiple faces and assign unique futuristic digital-entity looks."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--image", type=str, help="Path to an input image")
    mode.add_argument("--webcam", action="store_true", help="Use the live webcam feed")
    parser.add_argument("--camera", type=int, default=CAMERA_INDEX, help="Webcam device index")
    parser.add_argument("--save", action="store_true", help="Save the processed image")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.image:
        run_image(args.image, save=args.save)
        return
    if args.webcam or not args.image:
        if not args.webcam and not args.image:
            print("No mode given. Starting webcam. Use --image path.jpg for a photo.")
        run_webcam(args.camera, Path(OUTPUT_DIR))


if __name__ == "__main__":
    main()
