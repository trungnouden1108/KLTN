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

def getdata():
    #st = list(str(arduino.readline(), 'utf-8'))
    #return (str(''.join(st[:])))
    i=0
    c=""
    while i!=12:
        a = arduino.read()
        b = a.decode()
        c=c+b
        i=i+1
    d=c.replace(" ","")
    return d
