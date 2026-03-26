import time
import cv2
from djitellopy import Tello

class DroneController:
    def __init__(self):
        self.tello = Tello()
        self.width, self.height = 480, 320
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
