import os
import cv2
import time 
import mediapipe as mp
cap = cv2.VideoCapture(0)

# CAMERA TEST #
# pTime = 0
# while True:
#     success, img = cap.read()
#     imgRGB = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
#     cTime = time.time()
#     fps = 1/(cTime - pTime)
#     pTime = cTime
#     cv2.putText(img, f'FPS:{int(fps)}', (20,70),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)
#     cv2.imshow("Test", img)
#     cv2.waitKey(1)
# CAMERA TEST #



# HAND DETECTION #
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx,cy),10,(0,0,255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (20,70),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
# HAND DETECTION #


