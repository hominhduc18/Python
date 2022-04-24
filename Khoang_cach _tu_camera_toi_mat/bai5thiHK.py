import numpy as np
import cv2
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
while True:
    ret, img = cap.read()
    cv2.medianBlur(img, 5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255), 2)
        print(w)
        F = gray[x:x + w, y:y + h]
        dai = F.shape[0]
        rong = F.shape[1]
        khoangcach=dai *rong
        cm = khoangcach/w
        inch = cm/2.54
        feet=inch/12
        inch = '%.2f inch'%inch
        feet = '%.2f feet'%feet
        cm = '%.2f cm' %cm
        cv2.putText(img,'Don Vi Cm: '+str(cm),(x-80,y-80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(img,'Don Vi Inch:  '+str(inch), (x-100,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (158, 255, 255), 2)
        cv2.putText(img,'Don Vi feet: '+str(feet), (x-150,y-150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 108, 38), 2)
    cv2.imshow('Ho Minh Duc - 19480771', img)
    if cv2.waitKey(30) & 0xff==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()