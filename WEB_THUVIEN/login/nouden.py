import serial

try:
    arduino = serial.Serial('COM3', timeout=1, baudrate=9600)
except:
    print('please check the port')


def getsensordata():
    #st = list(str(arduino.readline(), 'utf-8'))
    #return (str(''.join(st[:])))
    while True:
        a = arduino.readline()
    # b=str(a,encode='utf-8')
        b = a.decode()
        c = b.replace(" ", "")
        if c != "":
            return c
