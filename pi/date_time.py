#
#Example file for formatting time and date output
#
from datetime import datetime
def main():
      now= datetime.now() #get the current date and time
      #%c - local date and time, %x-local's date, %X- local's time
      print(now.strftime("%d %m %Y - %H:%M %p")) # 24-Hour:Minute
def getdate():
    now= datetime.now()
    return now.strftime("%d/%m/%Y - %H:%M %p")
if __name__== "__main__":
    main()