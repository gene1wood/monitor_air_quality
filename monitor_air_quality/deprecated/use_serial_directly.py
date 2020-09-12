import time
import serial  # pyserial
ser = serial.Serial('/dev/ttyUSB0')  # open serial port

while True:
    data = []
    for index in range(0,10):
        datum = ser.read()
        data.append(datum)
    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10

    print('PM 2.5 / 10 : {} / {}'.format(pmtwofive, pmten))
    time.sleep(30)

ser.close()             # close port
