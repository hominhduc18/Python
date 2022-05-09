import numpy as np
import cv2
from tkinter import *
from PIL import Image, ImageTk
import pytesseract
import webbrowser
from subprocess import Popen
import os
from tkinter import messagebox
import connectCOM as com
import database as dat
import firebasetest as frb
COM = com.connect_COM()
con = dat.sql_connection("database_dakt.db")
rows = dat.sql_fetch(con, "TinhVN")

def test(temp):
    s = temp
    i = 0
    j = len(s) - 1
    flag1 = False
    flag2 = False
    while True:
        if (s[i].isdigit()):
            flag1 = True
        else:
            i += 1
        if (s[j].isdigit()):
            flag2 = True
        else:
            j -= 1
        if (flag1 and flag2):
            break
    return s[i:j + 1]

#Set up GUI
window = Tk()  #Makes main window
window.wm_title("Nhan dien bien so xe")
window.config(background="#FFFFFF")

#Graphics window
imageFrame = Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

#Capture video frames
lmain = Label(imageFrame)
lmain.grid(row=0, column=0)
cap = cv2.VideoCapture(0)
data_key =  StringVar()
check_key = StringVar()
addr_key = StringVar()
def show_frame():
    ret, frame = cap.read()
    scale_percent = 90
    # calculate the 50 percent of original dimensions
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)

    # dsize
    dsize = (width, height)

    # resize image
    frame = cv2.resize(frame ,dsize)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    noise_removal = cv2.bilateralFilter(gray, 9, 75, 75)
    equal_histogram = cv2.equalizeHist(noise_removal)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    morph_image = cv2.morphologyEx(equal_histogram, cv2.MORPH_OPEN, kernel, iterations=20)
    sub_morp_image = cv2.subtract(equal_histogram, morph_image)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    canny_image = cv2.Canny(thresh, 250, 255)
    kernel = np.ones((3, 3), np.uint8)
    # cv2.putText(frame, "KHUNG BIEN SO", (40, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
    # Tạo đường viền để theo dõi bien so
    contours, h = cv2.findContours(thresh, 1, 2)
    largest_rectangle = [0, 0]
    for cnt in contours:
        lenght = 0.05 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, lenght, True)
        if len(approx) == 4:
            area = cv2.contourArea(cnt)
            if area > largest_rectangle[0]:
                largest_rectangle = [cv2.contourArea(cnt), cnt, approx]
    x, y, w, h = cv2.boundingRect(largest_rectangle[1])
    image = frame[y:y + h, x:x + w]
    # cv2.drawContours(frame, [largest_rectangle[1]], 0, (0, 255, 0), 11)
    cropped = frame[y:y + h, x:x + w]
    cv2.putText(frame, "BIEN SO", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
    cv2.drawContours(frame, [largest_rectangle[1]], 0, (255, 0, 0), 8)
    # cv2.imshow('Dinh Vi Bien So Xe', frame)
    # DOC HINH ANH CHUYEN THANH FILE TEXT

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 1)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # cv2.imshow('Bien So La', thresh)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
    # print("Bien so xe la:", data)
    # dat = data[0:2]
    # print(dat)
    
    try:
        data = test(data)
        data = data.replace(".", "")
        data = data.replace("\n", " ")
        print(data)
        if (((int(data[0:2]) in i) for i in rows) and data[2] == "-" and data[4].isdigit()
    and data[3].isalpha() and (data[6:len(data)].isdigit()) ):
            print("Bien so xe la:", data)
            for i in rows:
                if int(data[0:2])in i:
                    #print(i[1])
                    addr_key.set(str(i[1]))
                    
            lst = (int(data[0:2]), data[3:5], int(data[6:]))
            
            
            data_key.set(data)
            
        #if (int(data[0:2]) < 100 and int(data[0:2]) > 0 and data[2] == "-" and data[4].isdigit()):
            #if (data[6:10].isdigit() or data[6:11].isdigit() or data[6:9].isdigit()):
            #    print("Bien so xe la:", data)
             #   addr_key.set(str(array.get(int(data[0:2]))))
              #  for i in range(len(data)-1):
               #     if(data[i]=="\n"):
                #        data = data[0:i] + " " + data[i+1:]
                #data_key.set(data)

    except:
        pass
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

def ghibienso():
    try:
        bienso = data_key.get()
        print(bienso)
        lst = (int(bienso[0:2]), bienso[3:5], bienso[6:])
        print(lst)
        if dat.find_e_luubienso(con,lst):
            frb.send_data_firebase(lst,False)
            dat.delete_e(con,lst)
            try:
                com.open_servo2(COM)
                com.close_servo2(COM) 
            except:
                pass
            messagebox.showinfo(title=None, message="Biển "+bienso+" đã ra khỏi bãi xe")
            
        else:
            dat.sql_insert_luubienso(con,lst)
            frb.send_data_firebase(lst,True)
            try:
                com.open_servo(COM)
                com.close_servo(COM) 
            except:
                pass
            messagebox.showinfo(title=None, message="Biển "+bienso+"  đã vào bãi xe")  
    except:
        messagebox.showerror(title=None, message="Biển số không hợp lệ")
        print("Bien khong hop le")
        
def quit():
    if messagebox.askyesno(title="Thoát chương trình", message="Bạn có muốn thoát chương trình ?"):
        window.destroy()

def openCloud():
    webbrowser.open("https://daktbiensoxe-default-rtdb.asia-southeast1.firebasedatabase.app/")
    
def openSqlite():
    os.system("xdg-open /home/pi/Downloads/New/DAKR\ provip/database_dakt.db")
def saveCSV():
    try:
        bienso = data_key.get()
        print(bienso)
        lst = (int(bienso[0:2]), bienso[3:5], bienso[6:])
        frb.get_data_firebase(lst)
    except:
        messagebox.showerror(title=None, message="Biển số không hợp lệ")
#Slider window (slider controls stage position)
sliderFrame = Frame(window, width=600, height=200,bg="#FFFFFF")
sliderFrame.grid(row = 1, column=0, padx=10, pady=2)

button1 = Button(sliderFrame, text = "Ghi biển số" ,width=15,font=('Arial', 10, 'bold'),command = ghibienso).grid(row=0,column=0,padx=10, pady=10)

buttonCSV = Button(sliderFrame, text = "Xuat CSV" ,width=15,font=('Arial', 10, 'bold'), command = saveCSV).grid(row=0,column=2,padx=10, pady=10)
buttonData = Button(sliderFrame, text = "Cloud Database" ,width=15,font=('Arial', 10, 'bold'), command = openCloud).grid(row=4,column=0,padx=10, pady=10)
buttonSQLite = Button(sliderFrame, text = "SQLite Database" ,width=15,font=('Arial', 10, 'bold'), command = openSqlite).grid(row=4,column=1,padx=10, pady=10)
label1 = Label(sliderFrame, text = "Thông tin biển số",bg="#FFFFFF",font=('Arial', 10, 'bold')).grid(row=1,column=0,padx=5, pady=2)
entry1 = Entry(sliderFrame,width=25,textvariable=data_key,font=('Arial',12)).grid(row=1,column=1,padx=5, pady=2)
label1_2 = Label(sliderFrame, text = "Biển tỉnh",bg="#FFFFFF",font=('Arial', 10, 'bold')).grid(row=2,column=0,padx=5, pady=2)
entry1_2 = Entry(sliderFrame,width=25,textvariable=addr_key,font=('Arial',12)).grid(row=2,column=1,padx=5, pady=2)
label2 = Label(sliderFrame, text = "Kiểm tra thông tin",bg="#FFFFFF",font=('Arial', 10, 'bold')).grid(row=3,column=0,padx=5, pady=2)
#entry2 = Entry(sliderFrame,width=20,textvariable=check_key,font=('Arial',12)).grid(row=3,column=1,padx=5, pady=2)
text = Text(sliderFrame, width  = 28, height =2)
text.grid(row=3,column=1,padx=5, pady=2)
def kiemtra():
    text.delete('1.0', 'end')
    bienso = data_key.get()
    print(bienso)
    lst = (int(bienso[0:2]), bienso[3:5], bienso[6:])
    if dat.find_e_luubienso(con,lst):
        text.insert('1.0',"Biển "+data_key.get()+"\nđang có trong bãi")
    else:
        text.insert('1.0',"Biển "+data_key.get()+"\nkhong có trong bãi")
    
    
button2 = Button(sliderFrame, text = "Kiểm tra" ,width=15,font=('Arial', 10, 'bold'),command = kiemtra).grid(row=0,column=1,padx=10, pady=10)

button3 = Button(window, text = "Thoát" ,width=15,font=('Arial', 10, 'bold'),command=quit).grid(row=3,column=0,padx=40, pady=10,sticky=NE)
show_frame()  #Display 2


window.protocol("WM_DELETE_WINDOW", quit)
window.resizable(False, False)
window.mainloop()  #Starts GUI