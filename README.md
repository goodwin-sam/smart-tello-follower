# smart-tello-follower

Face-recognition drone follower using a DJI Tello stream, OpenCV, and `face_recognition`.

## Prerequisites (Manjaro/Linux)

Install system packages required for Python venvs and native dependencies used by `dlib`:

```bash
sudo pacman -S --needed python311 python311-pip base-devel cmake openblas lapack
```

## Python Environment Setup

Create and activate a Python 3.11 virtual environment:

```bash
python3.11 -m venv venv
source venv/bin/activate
python --version
```

Upgrade packaging tools, then install pinned dependencies:

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Quick Verification

Validate imports before running the drone loop:

```bash
python -c "import dlib, face_recognition, cv2, djitellopy; print('imports ok')"
```

If this prints `imports ok`, your Python/native dependency stack is configured correctly.