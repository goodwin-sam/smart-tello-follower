import cv2
import face_recognition

class FaceRecognizer:
    def __init__(self, ref_img_path):
        ref_img = cv2.imread(ref_img_path)
        if ref_img is None:
            raise FileNotFoundError(f"Reference image not found at {ref_img_path}")
        encodings = face_recognition.face_encodings(ref_img)
        if not encodings:
            raise ValueError("No face encodings found in reference image")
        self.ref_encoding = face_recognition.face_encodings(ref_img)[0]
        print("reference image loaded and encoded")
        
    def recognize_faces(self, img):
        """Detect faces and compare them to the reference image"""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(img_rgb)
        face_encodings = face_recognition.face_encodings(img_rgb, face_locations)

        if not face_encodings:
            return face_locations, []

        face_matches = face_recognition.compare_faces([self.ref_encoding], face_encodings, tolerance=0.6)
        return face_locations, face_matches

    def draw_faces(self, img, face_locations, face_matches):
        for each_face in face_locations:
            cv2.rectangle(img, (each_face[3], each_face[0]), (each_face[1], each_face[2]), (255, 0, 0), 1)
        for i in range(len(face_matches)):
            if face_matches[i]:
                face_match = face_locations[i]
                cv2.rectangle(img, (face_match[3], face_match[0]), (face_match[1], face_match[2]), (255, 0, 255), 4)
        return img
