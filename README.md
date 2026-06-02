# Smart Tello Follower

An autonomous DJI Tello drone system that tracks and follows a specific person using real-time face recognition, and responds to hand gesture commands. Built with Python, OpenCV, MediaPipe, and the `face_recognition` library.

---

## Features

- **Personalized Face Tracking** — Recognizes a specific person from a reference photo and follows only them, ignoring other faces in frame.
- **Autonomous Following** — The drone continuously adjusts yaw, altitude, and forward/backward distance to keep the target centered and at a consistent distance.
- **Face Search Behavior** — If the target is lost, the drone rotates in place to search for them.
- **Hand Gesture Control** — Eight gesture commands let you control the drone mid-flight without a physical remote.
- **Gesture Confirmation System** — Gestures must be held for 20 consecutive frames before triggering, preventing accidental commands.
- **Live Video Feed** — Annotated camera stream shows detected faces (blue for unknown, magenta for matched) and recognized gestures in real time.

---

## Gesture Commands

| Gesture | Action |
|---|---|
| ✋ Open Palm (5 fingers) | Land the drone |
| ✊ Fist (0 fingers) | Pause tracking (hover in place) |
| 👌 OK Sign | Resume tracking after pause |
| ☝️ One Finger | 360° clockwise spin |
| ✌️ Two Fingers | Forward flip |
| 🤟 Three Fingers | Dance routine |
| 🖖 Four Fingers | Corkscrew maneuver |

---

## Architecture

The project is split into four focused modules plus a central config:

```
smart-tello-follower/
├── main.py                # Entry point; orchestrates the main control loop
├── drone_controller.py    # Tello connection, movement, gesture execution, face following
├── face_recognizer.py     # Face detection, recognition, and frame annotation
├── gesture_recognizer.py  # Hand landmark detection and gesture classification
├── config.py              # All tunable parameters (speeds, thresholds, camera size, etc.)
├── requirements.txt
└── ref_img.jpg            # Reference photo of the person to follow (not committed)
```

### How It Works

1. **Setup** — On launch, `main.py` connects to the Tello over Wi-Fi, starts the video stream, and takes off.
2. **Main Loop** — Every ~30ms, a frame is grabbed, flipped horizontally, and passed through face recognition and gesture recognition in parallel.
3. **Face Following** — `DroneController.follow_matched_face()` computes horizontal error (→ yaw), vertical error (→ up/down), and area error (→ forward/back) relative to the frame center and a target face size. Each axis has an independent deadzone, clamp, and scale factor.
4. **Gesture Execution** — `GestureRecognizer` buffers the last 20 gesture readings; only a fully consistent buffer triggers a confirmed gesture, which is then dispatched to `DroneController.execute_gesture()`.
5. **Cleanup** — On quit (`q`), `KeyboardInterrupt`, or any exception, the drone safely lands and the video window closes.

---

## Prerequisites

### Hardware
- DJI Tello drone
- Computer with Wi-Fi (connect to the Tello's Wi-Fi network before running)
- Uses Python Version 3.11

### System Dependencies

**Ubuntu / Debian:**

```bash
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt upgrade

# install required packages
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-all-dev \
    ffmpeg \
    libopencv-dev
```
**Manjaro/Arch Linux:**
```bash
sudo pacman -Syu
# Install required packages
sudo pacman -S --needed base-devel cmake openblas lapack
# Install python 3.11
yay -S python311
```

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/goodwin-sam/smart-tello-follower.git
cd smart-tello-follower
```

**2. Create and activate a Python 3.11 virtual environment**

```bash
python3.11 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

Please be patient, may take time to build wheel for dlib
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**4. Fix face_recognition_models and the broken __init__.py**

The published package uses a deprecated pkg_resources import
```bash
# Fix face_recognition_models (pkg_resources workaround)
cd ~
git clone https://github.com/ageitgey/face_recognition_models
cd face_recognition_models
pip install .
cd ~/smart-tello-follower

# Patch the broken __init__.py
cat > venv/lib/python3.11/site-packages/face_recognition_models/__init__.py << 'EOF'
from pathlib import Path
_models_dir = Path(__file__).parent / "models"
def pose_predictor_model_location():
    return str(_models_dir / "shape_predictor_68_face_landmarks.dat")
def pose_predictor_five_point_model_location():
    return str(_models_dir / "shape_predictor_5_face_landmarks.dat")
def face_recognition_model_location():
    return str(_models_dir / "dlib_face_recognition_resnet_model_v1.dat")
def cnn_face_detector_model_location():
    return str(_models_dir / "mmod_human_face_detector.dat")
EOF
```

**5. Verify the install**

```bash
python -c "import dlib, face_recognition, cv2, djitellopy, mediapipe; print('All imports OK')"
```

---

## Setup: Reference Image

The drone tracks a specific person. Before running, place a clear, front-facing photo of that person in the project root and name it `ref_img.jpg`.

- The face should be clearly visible, well-lit, and unobstructed.
- Only one face should be present in the reference image.
- The path can be changed in `config.py` via `REF_IMG_PATH`.

---

## Running

1. Power on your Tello drone.
2. Connect your computer to the Tello's Wi-Fi network.
3. Run:

```bash
python main.py
```

The drone will connect, print battery level, take off, and begin tracking. Press `q` in the video window to quit and land safely.

---

## Configuration

All tunable parameters live in `config.py`:

| Parameter | Default | Description |
|---|---|---|
| `WIDTH` / `HEIGHT` | 480 / 320 | Camera frame resolution |
| `TOLERANCE` | 0.6 | Face recognition strictness (lower = stricter) |
| `REF_IMG_PATH` | `"ref_img.jpg"` | Path to the reference face image |
| `HORIZONTAL_DEADZONE` | 50 px | Ignore horizontal error within this range |
| `VERTICAL_DEADZONE` | 50 px | Ignore vertical error within this range |
| `AREA_DEADZONE` | 2000 px² | Ignore distance error within this range |
| `TARGET_FACE_AREA` | 7000 px² | Target face bounding box area (controls follow distance) |
| `VERTICAL_OFFSET` | 100 px | Shifts the vertical tracking center downward |
| `HORIZONTAL_SCALE` | 0.12 | Yaw speed multiplier |
| `VERTICAL_SCALE` | 0.25 | Up/down speed multiplier |
| `AREA_SCALE` | 0.005 | Forward/back speed multiplier |
| `NO_FACE_SEARCH_THRESHOLD` | 60 frames | Frames without a face before search mode activates |
| `SEARCH_YAW_SPEED` | 30 | Yaw speed during face search |

---

## Dependencies

| Package | Purpose |
|---|---|
| `djitellopy` | DJI Tello SDK — drone connection and RC control |
| `opencv-python` | Video capture, frame processing, display |
| `face_recognition` | Face detection and identity matching (wraps `dlib`) |
| `mediapipe` | Hand landmark detection for gesture recognition |

---

## Known Limitations

- The Tello's camera has noticeable latency (~100–200ms), which can cause slight oscillation in the tracking loop.
- Face recognition runs on every frame; on slower machines this may reduce responsiveness. Consider running recognition every N frames if needed.
- Gesture recognition uses one hand at a time from a multi-hand result — in practice this works fine but the first detected hand takes priority.
- The corkscrew maneuver includes a yaw correction heuristic that may not be perfectly accurate across all environments.
- `ref_img.jpg` is not committed to the repo (see `.gitignore`) — each user must provide their own.
