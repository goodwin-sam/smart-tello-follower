import os

# Suppress harmless OpenCV/Qt warnings
os.environ["QT_QPA_PLATFORM"] = "xcb"
os.environ["QT_LOGGING_RULES"] = "*.debug=false;*.info=false;*.warning=false" 

import time
import cv2

from drone_controller import DroneController
from face_recognizer import FaceRecognizer
from gesture_recognizer import GestureRecognizer

def main():  
    time.sleep(5)
    while_count = 0
    drone = DroneController()
    face_recognizer = FaceRecognizer()
    gesture_recognizer = GestureRecognizer()

    try:
        drone.connect_and_setup()
        # drone.takeoff()

        while True:
            while_count += 1
            if while_count % 10 == 0:
                print("while_count: " + str(while_count))
                # drone.tello.send_rc_control(0, 0, 0, 0)

            # check for quit
            if drone.check_for_quit():
                break

            # gets frame from drone
            img = drone.get_frame()
            img = cv2.flip(img, 1)

            # recognizes faces in frame and draws bounding boxes around them
            face_locations, face_matches = face_recognizer.recognize_faces(img)
            img = face_recognizer.draw_faces(img, face_locations, face_matches)

            img = gesture_recognizer.recognize_and_draw_hands(img)

            # finds first matched face and follows it
            matched_face = drone.find_matched_face(face_locations, face_matches)
            drone.follow_matched_face(matched_face)

            # shows frame in window
            cv2.imshow("Drone Camera", img)

            time.sleep(0.03)

    
    except KeyboardInterrupt:
        print("Keyboard interrupt detected (ctrl+c). shutting down...")

    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        print("Cleaning up and landing drone...")
        drone.land()
        drone.tello.streamoff()
        cv2.destroyAllWindows()
        print("Drone landed and windows closed")

if __name__ == "__main__":
    main()
