import cv2
import numpy as np
cap = cv2.VideoCapture('videothihk.avi')
object_detector = cv2.createBackgroundSubtractorMOG2()
kernel = np.ones((5,5),np.uint8)
while True:
    ret, frame = cap.read()
    mask = object_detector.apply(frame)
    _, thresh = cv2.threshold(mask, 0.1, 255, cv2.THRESH_BINARY)
    open = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    close = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    dem = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > 255:
             dem += 1
             x, y, w, h = cv2.boundingRect(cnt)
             cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 225, 255), 2)
             cv2.putText(frame, 'xe '+ str(dem), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,250, 64), 2)
    cv2.putText(frame, "So Luong xe xuat hien: " + str(dem) , (200,300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 134), 2)
    cv2.imshow('Ho Minh Duc -19480771', frame)
    if cv2.waitKey(30) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()