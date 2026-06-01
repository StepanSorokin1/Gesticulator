import mediapipe as mp
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandTracker:
    def __init__(self, model_path='hand_landmarker.task', draw_landmarks=False):
        base_options = python.BaseOptions(model_asset_path=model_path)
        self.last_landmarks = None
        self.last_handedness = None

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            num_hands=1,  # Количество рук для отслеживания
            min_hand_detection_confidence=0.5, # Чувствительность обнаружения руки
            min_hand_presence_confidence=0.5, # Чувствительность нахождения в кадре
            min_tracking_confidence=0.7,       # Стабильность отслеживания
            result_callback=self.result_callback
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.draw_landmarks = draw_landmarks

    def result_callback(self, detection_result, output_image, timestamp_ms: int):
        if detection_result.hand_landmarks:
            # Сохраняем результат в полях класса
            self.last_landmarks = detection_result.hand_landmarks[0]
            self.last_handedness = detection_result.handedness[0][0].category_name
        else:
            self.last_landmarks = None
            self.last_handedness = None

    def process_async(self, frame, timestamp_ms: int):
        # Конвертируем BGR в RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        self.detector.detect_async(mp_image, timestamp_ms)
    
    def get_latest_results(self):
        return self.last_landmarks, self.last_handedness
    
    @staticmethod
    def draw_landmarks(frame, landmarks):
        if landmarks is None:
            return
        
        h, w, _ = frame.shape
        connections = [
            (0,1), (1,2), (2,3), (3,4),          # большой палец
            (0,5), (5,6), (6,7), (7,8),          # указательный
            (0,9), (9,10), (10,11), (11,12),     # средний
            (0,13), (13,14), (14,15), (15,16),   # безымянный
            (0,17), (17,18), (18,19), (19,20),   # мизинец
            (0,5), (5,9), (9,13), (13,17)        # соединения между пальцами
        ]
                
        for start, end in connections:
            x1, y1 = int(landmarks[start].x * w), int(landmarks[start].y * h)
            x2, y2 = int(landmarks[end].x * w), int(landmarks[end].y * h)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)

        for lm in landmarks:
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)
    
    def close(self):
        self.detector.close()