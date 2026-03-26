import os

# Suppress harmless OpenCV/Qt warnings
os.environ["QT_QPA_PLATFORM"] = "xcb"
os.environ["QT_LOGGING_RULES"] = "*.debug=false;*.info=false;*.warning=false" 

import time
import cv2

from drone_controller import DroneController
from face_recognizer import FaceRecognizer

def main():  
    time.sleep(5)
    whileCount = 0
    drone = DroneController()
    face_recognizer = FaceRecognizer("ref_img.jpg")

    try:
        drone.connect_and_setup()
        drone.takeoff()

        while True:
            whileCount += 1
            if whileCount % 10 == 0:
                print("whileCount: " + str(whileCount))
            if drone.check_for_quit():
                break
            img = drone.get_frame()
            face_locations, face_matches = face_recognizer.recognize_faces(img)
            img = face_recognizer.draw_faces(img, face_locations, face_matches)       

            cv2.imshow("Drone Camera", img)

            time.sleep(0.03)

    except Exception as e:
        print(f"Unexpected error: {e}")

    except KeyboardInterrupt:
        print("Keyboard interrupt detected (ctrl+c). shutting down...")

    finally:
        print("Cleaning up and landing drone...")
        drone.land()
        cv2.destroyAllWindows()
        print("Drone landed and windows closed")

if __name__ == "__main__":
    main()
