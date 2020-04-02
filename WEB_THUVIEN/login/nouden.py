import serial
import threading
import time,datetime
try:
    arduino = serial.Serial('COM3', timeout=1, baudrate=9600)
    connected=False
    id = ""
    a = ""
except:
    print('please check the port')



def getsensordata():

    #st = list(str(arduino.readline(), 'utf-8'))
    #return (str(''.join(st[:])))
    try:
        arduino.open()
    except Exception as e:
        print("Exception: Opening serial port: " + str(e))
        global id,a
    while True:
        a = arduino.readline().decode()
    # b=str(a,encode='utf-8')
        c = a.replace(" ", "")
        e = c.replace("\r", "")
        id = e.replace("\n", "")
        print("f",id)
        time.sleep(0.5)
        if id != "":
            break;
    arduino.close()
    return id


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
    e=d.replace("\r","")
    f=e.replace("\n","")
    return f

def sendidbook(id):
    id_rev=getsensordata()
    print("id",id)
    print("id_rev",id_rev)
    flag=0

    if id==id_rev:
            flag=2
            arduino.write("y")
            print("2")
    else:
            flag=1
            arduino.write(b'n')
            print("flag",flag)

def getid1():
    try:
        arduino.open()
    except Exception as e:
        print("Exception: Opening serial port: " + str(e))
    global id, a
    while True:
        a = arduino.readline()
        b = a.decode("UTF-8")
        c = b.replace(" ", "")
        e = c.replace("\r", "")
        id = e.replace("\n", "")
        print("id",id)
        time.sleep(0.01)
        break;
    arduino.close()
    return id

def day(a):
    c=0
    if a<7:
        c=(a)*1000
    elif a >=7:
        c=(a)*3000
    return c


id_check=""
temp=""
def checkbook():
    try:
        arduino.open()
    except Exception as e:
        print("Exception: Opening serial port: " + str(e))
    global id_check,temp
    time.sleep(0.5)
    temp = arduino.readline().decode()
    c = temp.replace(" ", "")
    e = c.replace("\r", "")
    id_check = e.replace("\n", "")
    print("f",id_check)
    if id_check != "":
        arduino.close()
        return id_check

def sendarduino_1():
    i=0
    flag=0
    try:
        arduino.open()
    except Exception as e:
        print("Exception: Opening serial port: " + str(e))
    while (i < 5000):
        arduino.write(b'0')
        i=i+1
    arduino.close()


def sendarduino_2():
    i=0
    try:
        arduino.open()
    except Exception as e:
        print("Exception: Opening serial port: " + str(e))
    while (i < 5000):
        arduino.write(b'1')
        i = i + 1
    arduino.close()
