import cv2
from constants import CAMERA_WIDTH, CAMERA_HEIGHT

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    
    def get_frame(self):
        success, frame = self.cap.read()
        if success:
            frame = cv2.flip(frame, 1)  # Зеркальное отражение
            return frame
        return None
    
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()