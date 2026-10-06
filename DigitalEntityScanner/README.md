# Digital Entity Scanner

Multi-face detection and unique futuristic character transformation.

Version 1 detects several faces in a photo or webcam feed, assigns each person a distinct digital-entity profile, and overlays procedural neon / circuit / metallic effects using MediaPipe landmarks.

## Setup

Prefer **Python 3.9–3.12** so MediaPipe Face Mesh can install. On Python 3.13+ (including 3.14), MediaPipe may be unavailable; the app then falls back to OpenCV Haar detection and estimated landmarks so you can still demo image and webcam modes.

```bash
cd DigitalEntityScanner
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python generate_assets.py
```

## Run

Image mode:

```bash
python main.py --image path\to\photo.jpg --save
```

Webcam mode (default if you pass no arguments):

```bash
python main.py --webcam
```

Keys in the preview window:

- `Q` or `Esc` — quit
- `S` — save the current frame to `output/results`
- `R` — reassign character themes (webcam)

## What Version 1 includes

- Multi-face detection (MediaPipe Face Detection)
- Face mesh landmarks (eyes, nose, mouth, contour)
- Unique character IDs and themes (Alpha–Kappa)
- Procedural effects: neon eyes, circuits, hologram grid, metallic tint, scan HUD
- Webcam tracking so the same person keeps the same entity look

Not in Version 1: generative AI face replacement (PyTorch / Diffusers). That is Version 2.

## Project layout

```
DigitalEntityScanner/
  main.py
  config.py
  src/face_detector.py
  src/face_landmarks.py
  src/face_tracker.py
  src/character_generator.py
  src/effects.py
  src/image_processor.py
```
