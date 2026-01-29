from constants import palm_side

class GestureDetector:
    @staticmethod
    def get_fingers(landmarks, handedness):
        """Определяет, какие пальцы подняты"""
        fingers = {
            'thumb': False,
            'index': False,
            'middle': False,
            'ring': False,
            'pinky': False
        }
        if handedness == "Right":
            if landmarks[5].x < landmarks[17].x:
                palm_side = "Inner"
            else:
                palm_side = "Outside"
        elif handedness == "Left":
            if landmarks[5].x > landmarks[17].x:
                palm_side = "Inner"
            else:
                palm_side = "Outside"
        
        fingers['index'] = landmarks[8].y < landmarks[6].y
        fingers['middle'] = landmarks[12].y < landmarks[10].y
        fingers['ring'] = landmarks[16].y < landmarks[14].y
        fingers['pinky'] = landmarks[20].y < landmarks[18].y
        
        # Большой палец - отдельная логика
        if handedness == "Right":
            if palm_side == "Inner":
                fingers['thumb'] = landmarks[4].x < landmarks[5].x
            else:
                fingers['thumb'] = landmarks[4].x > landmarks[5].x
        else:
            if palm_side == "Inner":
                fingers['thumb'] = landmarks[4].x > landmarks[5].x
            else:
                fingers['thumb'] = landmarks[4].x < landmarks[5].x
        return fingers
    
    @staticmethod
    def detect_gesture(fingers):
        """Определяет жест по положению пальцев"""
        if fingers['index'] and not any([fingers['middle'], fingers['ring'], fingers['pinky']]):
            return "POINT"
        
        if fingers['index'] and not fingers['middle'] and not fingers['ring'] and fingers['pinky']:
            return "ROCK"
        
        if fingers['index'] and fingers['middle'] and not fingers['ring'] and not fingers['pinky']:
            return "VICTORY"
        
        if not fingers['thumb'] and all([fingers['index'], fingers['middle'], fingers['ring'], fingers['pinky']]):
            return "STOP"
        
        return "UNKNOWN"