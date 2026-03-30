import time
import cv2
from djitellopy import Tello
from config import HORIZONTAL_DEADZONE, HORIZONTAL_SCALE, MAX_HORIZONTAL_ERROR, MAX_VERTICAL_ERROR, WIDTH, HEIGHT, TARGET_FACE_AREA

class DroneController:
    def __init__(self):
        self.tello = Tello()
        self.width, self.height = WIDTH, HEIGHT
        self.is_flying = False
        print("is_flying: " + str(self.is_flying))

    def connect_and_setup(self):
        print("Connecting to drone...")
        self.tello.connect()
        print(f"Battery: {self.tello.get_battery()}%")
        print("Stream on...")
        self.tello.streamon()
        time.sleep(2)
        print("Connected to drone and stream on")

    def takeoff(self):
        print("Taking off...")
        self.tello.takeoff()
        self.is_flying = True
        print("is_flying: " + str(self.is_flying))
        time.sleep(1)

    def land(self):
        """safely land the drone if flying"""
        if self.is_flying:
            print("Landing...")
            try:
                self.tello.land()
            except Exception as e:
                print(f"Error landing: {e}")
            finally:
                self.is_flying = False
            print("is_flying: " + str(self.is_flying))
        else:
            print("Called land() but Drone is not flying")

    def check_for_quit(self):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quitting while loop...")
            return True
        else:
            return False

    def get_frame(self):
        img = self.tello.get_frame_read().frame
        return cv2.resize(img, (self.width, self.height))

    def find_matched_face(self, face_locations, face_matches):
        """return first matched face, or none if no face is matched"""
        for i, is_matched_face in enumerate(face_matches):
            if is_matched_face:
                return face_locations[i]
        return None

    def follow_matched_face(self, matched_face):
        # print("Calculating follow movement...")
        if matched_face is None:
            # print("No matched face found, hovering...")
            return
        top, right, bottom, left = matched_face
        width = right - left
        height = bottom - top
        area = width * height
        print("Width: " + str(width))
        print("Height: " + str(height))
        print("Area: " + str(area))

        center_x = left + (width // 2)
        center_y = top + (height // 2)
        print("Center X: " + str(center_x))
        print("Center Y: " + str(center_y))

        hor_error = (center_x - (self.width // 2))
        vert_error = (center_y - (self.height // 2))
        area_error = (area - (TARGET_FACE_AREA))
        print("Hor Error: " + str(hor_error))
        print("Vert Error: " + str(vert_error))
        print("Area Error: " + str(area_error))

        horizontal_error = max(-MAX_HORIZONTAL_ERROR, min(MAX_HORIZONTAL_ERROR, hor_error))
        vertical_error = max(-MAX_VERTICAL_ERROR, min(MAX_VERTICAL_ERROR, vert_error))

        yaw = 0
        if abs(horizontal_error) > HORIZONTAL_DEADZONE:
            yaw = int(horizontal_error * HORIZONTAL_SCALE)
            yaw = max(-100, min(100, yaw))
            print("Yaw: " + str(yaw))
        if yaw != 0:
            self.tello.send_rc_control(0, 0, 0, yaw)
            

