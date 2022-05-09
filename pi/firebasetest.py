import pyrebase as pfb
import date_time as date

import csv_1 as csv

config = {
      "apiKey": "AIzaSyA3SGCniZPP-cBAywRJsvRRccc7AzL0Mig",
      "authDomain": "daktbiensoxe.firebaseapp.com",
      "projectId": "daktbiensoxe",
      "databaseURL": "https://daktbiensoxe-default-rtdb.asia-southeast1.firebasedatabase.app/",
      "storageBucket": "daktbiensoxe.appspot.com",
      "messagingSenderId": "901800326785",
      "appId": "1:901800326785:web:e52c776e0fa721eefb7f80",
      "measurementId": "G-0KBMSVC7SW"
    }


firebase = pfb.initialize_app(config)
database = firebase.database()

def send_data_firebase(lst,status):
    data = {"Ma tinh": lst[0], "Ki hieu": lst[1], "Bien so": lst[2],"Thoi gian nhan dien":date.getdate(),"Trang thai":status}
    database.push(data)
def get_data_firebase(lst):
    try:
        b = {"Ma tinh": lst[0], "Ki hieu": lst[1], "Bien so": lst[2]}
        a = database.get()
        a = dict(a.val())
        data = list()
        for i in a:
            temp = a.get(i)
            if(temp["Ma tinh"] == b["Ma tinh"] and temp["Ki hieu"]==b["Ki hieu"] and temp["Bien so"]==b["Bien so"]):
                data.append(list(temp.values()))
        csv.write_CSV(lst, data)
    except:
        print("Error")
            
#lst = [83, 'V2', "21661"]
#status = True
#send_data_firebase(lst,status)
#get_data_firebase(lst)


