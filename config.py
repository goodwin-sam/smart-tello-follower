"""
configuration settings for smart tello follower
tunable parameters are centralized here
"""

# camera
WIDTH = 480
HEIGHT = 320

# face recognition
TOLERANCE = 0.6
REF_IMG_PATH = "ref_img.jpg"

# face tracking deadzones
HORIZONTAL_DEADZONE = 50
VERTICAL_DEADZONE = 50
AREA_DEADZONE = 2000

# face tracking max errors for clamping
MAX_HORIZONTAL_ERROR = 200
MAX_VERTICAL_ERROR = 100
MAX_AREA_ERROR = 5000

# target face size
TARGET_FACE_AREA = 7000

# vertical centering
VERTICAL_OFFSET = 100

# movement scales
HORIZONTAL_SCALE = 0.12
VERTICAL_SCALE = 0.25
AREA_SCALE = 0.005

# face search behavior
NO_FACE_SEARCH_THRESHOLD = 60
SEARCH_YAW_SPEED = 30
