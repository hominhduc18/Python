import mediapipe as mp
import cv2
import time
id = 0
scale = 2
cap = cv2.VideoCapture(id)
wCam, hCam = 640 * scale, 480 * scale
cap.set(3, wCam)
cap.set(4, hCam)
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=10)
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            # get location of each point
            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 0:
                    # cv2.circle(img, (cx,cy), 10, (255,255,255), cv2.FILLED)
                    cv2.putText(img, 'hand', (cx - 5, cy + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
            mpDraw.draw_landmarks(img, hand, mpHands.HAND_CONNECTIONS)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
    cv2.imshow('camera', img)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(5)