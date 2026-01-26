import cv2
from camera import Camera
from timer import Timer
from hand_tracker import HandTracker
from gesture_tracker import GestureDetector
from gesture_controller import GestureController

def main():
    # Инициализация всех компонентов
    camera = Camera()
    tracker = HandTracker()
    detector = GestureDetector()
    controller = GestureController()
    timer = Timer()
    show_FPS = False
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
                
                # Завершение программы 
                if gesture == "STOP":
                    break

            # Вывод FPS при необходимости
            if cv2.waitKey(1) == ord('t'):
                show_FPS = not(show_FPS)
            
            if show_FPS:
                cv2.putText(frame, f"FPS: {timer.FPS_counter()}", (480, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
            
            # Показываем изображение
            cv2.imshow("Gesture Control", frame)
            
            
    
    finally:
        # Очистка ресурсов
        camera.release()
        tracker.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()