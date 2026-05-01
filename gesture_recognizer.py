import cv2
import mediapipe as mp

from config import WIDTH, HEIGHT

class GestureRecognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.4, min_tracking_confidence=0.3)
        self.mp_draw = mp.solutions.drawing_utils
        print("Gesture recognizer initialized")
        

    def recognize_and_draw_hands(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        hand_results = self.hands.process(img_rgb)

        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                finger_count = self.count_fingers(hand_landmarks)
                gesture = self.get_gesture(finger_count)
                if gesture:
                    print(f"Gesture: {gesture}")
                    wrist = hand_landmarks.landmark[0]
                    label_x = int(wrist.x*img.shape[1])
                    label_y = int(wrist.y*img.shape[0])+20
                    cv2.putText(img, gesture, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        return img

    
    def count_fingers(self, hand_landmarks):
        landmarks = hand_landmarks.landmark
        extended_fingers = 0

        # thumb
        if landmarks[4].x > landmarks[3].x:
            extended_fingers += 1

        # four fingers
        for tip, mid in [(8, 6), (12, 10), (16, 14), (20, 18)]:
            if landmarks[tip].y < landmarks[mid].y:
                extended_fingers += 1

        return extended_fingers


    def get_gesture(self, finger_count):
        if finger_count == 0:
            return "Fist"
        elif finger_count == 2:
            return "Two_Fingers"
        elif finger_count == 5:
            return "Open_Palm"
        else:
            return None
            
