import serial as sa
import time 

serial=sa.Serial("/dev/ttyUSB0", 9600, timeout = 1)
input_ser = serial.readline()
print("Status: "+input_ser.decode("utf-8").strip()+" ARDUINO")
while 1:
    serial.write(bytes("i", 'utf-8'))
    print("ON")
    time.sleep(3)
    serial.write(bytes("j", 'utf-8'))
    print("OFF")
    time.sleep(3)
    if serial.in_waiting:
        packet = serial.readline()
        print(packet.decode('utf'))