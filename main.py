import cv2
import time
from camera import Camera
from hand_tracker import HandTracker
from gesture_tracker import GestureDetector
from gesture_controller import GestureController

def main():
    # Инициализация всех компонентов
    camera = Camera()
    tracker = HandTracker()
    detector = GestureDetector()
    controller = GestureController()
    
    fps_time = time.time()
    frame_count = 0
    
    try:
        while True:
            # Получаем кадр с камеры
            frame = camera.get_frame()
            if frame is None:
                break
            
            # Определяем руку
            landmarks, handedness = tracker.process(frame)
            
            if landmarks and handedness:
                # Определяем жесты
                fingers = detector.get_fingers_up(landmarks, handedness)
                gesture = detector.detect_gesture(fingers)
                
                # Управление мышью
                controller.handle_gesture(gesture, landmarks, handedness)
                
                # Показываем жест на экране
                cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Считаем FPS
            frame_count += 1
            if time.time() - fps_time > 1:
                fps = frame_count
                frame_count = 0
                fps_time = time.time()
                print(f"FPS: {fps}")
            
            # Показываем изображение
            cv2.imshow("Gesture Control", frame)
            
            # Выход по клавише 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        # Очистка ресурсов
        camera.release()
        tracker.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()