import cv2 as cv
import threading
from time import time
import mediapipe as mp
import pyautogui as gui
from functions import get_hand_information, get_finger_state, recognize_gesture, move_mouse


cap = cv.VideoCapture(0)
screen_width, screen_height = gui.size()
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)


# Инициализация переменных для подсчета fps
prev_time = 0
fps = 0
interval = 0.25
frame_counter = 0


# Инициализация MediaPipe Hands
mp_drawing = mp.solutions.drawing_utils  # для рисования landmarks
mp_drawing_styles = mp.solutions.drawing_styles  # стили рисования
mp_hands = mp.solutions.hands  # модель распознавания рук



with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=1,           # 0, 1, 2 - кочество модели по возрастанию
    min_detection_confidence=0.5, # минимальная уверенность при обнаружении руки
    min_tracking_confidence=0.5   # минимальная уверенность при отслеживании между кадрами
) as hands:


    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        frame.flags.writeable = False  # изображение становится read-only (ускоряет обработку)
        frame = cv.cvtColor(cv.flip(frame, 0), cv.COLOR_BGR2RGB)


        results = hands.process(frame) # Нахождение руки
        

        # Визуализация распознавания рук
        if results.multi_hand_landmarks:
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):  # для каждой обнаруженной руки
                # mp_drawing.draw_landmarks(
                #     frame,
                #     hand_landmarks,
                #     mp_hands.HAND_CONNECTIONS,
                #     mp_drawing_styles.get_default_hand_landmarks_style(),  # стиль точек
                #     mp_drawing_styles.get_default_hand_connections_style()  # стиль линий
                # )
                
                # Точки руки
                landmarks = {point: hand_landmarks.landmark[point] for point in range(21)}

                # Определение правой\левой руки, направления руки, стороны руки
                if results.multi_handedness and i < len(results.multi_handedness):
                    handedness, direction, side = get_hand_information(results.multi_handedness[i], landmarks)
                else:
                    handedness, direction, side = None, None, None
                
                # Распознавание жестов для каждой руки
                if handedness and direction and side:
                    finger_states = get_finger_state(handedness, direction, side, landmarks)
                    gesture = recognize_gesture(handedness, direction, side, landmarks, finger_states)
                
                
                if gesture == "Pointing_Up":
                    x = int((1 - landmarks[8].x) * screen_width)
                    y = int((1 - landmarks[8].y) * screen_height)
                    threading.Thread(target=move_mouse, args=(x, y)).start()
                
                if gesture == "Stop":
                    cap.release()
                    cv.destroyAllWindows()
                    exit()
                
                # if gesture == "Fist":
                #     gui.click()



        # Вывод информации
        
        # Расчет fps
        # frame_counter += 1
        # next_time = time()
        # if next_time - prev_time >= interval:
        #     fps = frame_counter // (next_time - prev_time)
        #     prev_time = next_time
        #     frame_counter = 0
        

        # Переворачиваем по оси y, т.к. ренее мы его перевернули
        # Преобразование изображения обратно в BGR, иначе все посинеет)
        # frame = cv.cvtColor(cv.flip(frame, 0), cv.COLOR_RGB2BGR) 
        # cv.putText(frame, f"FPS: {fps}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
        # cv.imshow('check', frame)
        # cv.waitKey(1) # Обновление окна вывода
        

        



cap.release()
cv.destroyAllWindows()