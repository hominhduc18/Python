import serial as sa
import time 


def connect_COM():
    try:
        serial=sa.Serial("/dev/ttyUSB0", 9600, timeout = 1)
        input_ser = serial.readline()
        print("Status: "+input_ser.decode("utf-8").strip()+" ARDUINO")
        return serial
    except:
        return 0
def open_servo(serial):
    serial.write(bytes("i", 'utf-8'))
def close_servo(serial):
    serial.write(bytes("j", 'utf-8'))
def open_servo2(serial):
    serial.write(bytes("k", 'utf-8'))
def close_servo2(serial):
    serial.write(bytes("l", 'utf-8'))


