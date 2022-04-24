# Haar Cascade Classifiers
import numpy as np
import cv2
import  math
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('mat.xml')
nose_cascade= cv2.CascadeClassifier('E:\python\THONG KE MAY TINH\PYTHON\series\haarcascade_mcs_nose.xml')
mouth_cascade= cv2.CascadeClassifier('E:\python\THONG KE MAY TINH\PYTHON\series\mouth.xml')
while True:
    ret, frame = cap.read()
    cv2.medianBlur(frame, 5)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame,"Khuon mat",(x,y-4),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        roi_gray = gray[x:x + w, y:y + w]
        roi_color = frame[x:x + h, y:y + w]
        eyes = eye_cascade.detectMultiScale(roi_gray,1.1,5)
        nose =  nose_cascade.detectMultiScale(roi_gray,1.1,5)
        mouth = mouth_cascade.detectMultiScale(roi_gray,1.1,5)
        for (x2, y2, w2, h2) in eyes:
            eye_center = (x2 + w2 // 2, y2 + h2 // 2)
            radius = int(round((w2 + h2) * 0.25))
            cv2.circle(roi_color, eye_center, radius, (255, 255, 0), 4)
            cv2.putText(frame, "Mat", (x2+150, y2+150), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 0), 2)
        for (nx, ny, nw, nh) in nose:
            cv2.rectangle(roi_color, (nx, ny), (nx + nw, ny + nh), (0, 0, 0), 2)
            cv2.putText(frame, "Mui", (x+150, y+200), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 2)
            for (mx, my, mw, mh) in mouth:
                center = (mx + mw // 2, my + mh // 2)
                cv2.ellipse(roi_color, center, (mw // 2, mh // 2), 0, 0, 360, (255, 0, 255), 4)
            cv2.putText(frame, "Mieng", (x+50, y+200), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 0, 255), 2)
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()