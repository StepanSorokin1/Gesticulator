import cv2
from constants import CAMERA_WIDTH, CAMERA_HEIGHT
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
    show_fps = False
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
                fingers = detector.get_fingers(landmarks, handedness)
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
                show_fps = not(show_fps)
            
            if show_fps:
                cv2.putText(frame, f"FPS: {timer.fps_counter()}", (CAMERA_WIDTH - 160, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
            
            # Показываем изображение
            cv2.imshow("Gesture Control", frame)

    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
    else:
        print("Успешное завершение программы")  
            
    
    finally:
        # Очистка ресурсов
        camera.release()
        tracker.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()