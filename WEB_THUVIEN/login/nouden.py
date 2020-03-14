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
        e = c.replace("\r", "")
        f = e.replace("\n", "")
        if f != "":
            return f

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
            arduino.write(b'y')
            print("2")
    else:
            flag=1
            arduino.write(b'n')
            print("flag",flag)
