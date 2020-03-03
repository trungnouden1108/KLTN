from django.shortcuts import render
from django.http import HttpResponse
from .forms import Register
from . import nouden as no
from . import capture_img
from django.views import View
from django.http import StreamingHttpResponse,HttpResponseServerError
from .models import DocGia
import serial
import numpy as np
import cv2
import datetime
import pickle
import time
from django.views.decorators import gzip
import os
from django.core.exceptions import ObjectDoesNotExist
from . import face_training
# Create your views here.


class register(View):
    def get(self,request):
        q=Register()
        return render(request,'login/register.html',{'f':q,})

class but_register(View):
    def get(self, request):
        q = Register()
        return render(request, 'login/register_but.html', {'f': q, 'id_card': no.getsensordata()})

    def post(self,request):
        q=Register(request.POST)
        if q.is_valid():
            q.save()
            return HttpResponse("OK")
        else:
            return HttpResponse("ko hợp lệ")


def get_frame():
    camera = cv2.VideoCapture(1)
    face_cascade = cv2.CascadeClassifier('I:\Program Files\Python\Lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml')

    a=no.getdata()
    b=a
    try:
        # creating a folder named data
        if not os.path.exists('Image/' + b):
            os.makedirs('Image/' + b)

    # if not created then raise error
    except OSError:
        print('Error: Creating directory of Image')
    currentframe = 0
    start =datetime.datetime.now()
    second_start=start.second
    minute_start=start.minute
    hour_start=start.hour
    c=hour_start*3600+minute_start*60+second_start
    data = 0
    while True:
        ret, img = camera.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        faces = sorted(faces, key=lambda x: x[2] * x[3],
                       reverse=True)
        faces = faces[:1]
        if len(faces) == 1:
            face = faces[0]
            # lưu lại những điểm của khuôn mặt
            x, y, w, h = face
            color = (255, 0, 0)
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
        imgencode = cv2.imencode('.jpg',img )[1]
        stringData = imgencode.tostring()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + stringData + b'\r\n')
        end = datetime.datetime.now()
        second_end = end.second
        minute_end=end.minute
        hour_end=end.hour
        b=hour_end*3600+minute_end*60+second_end

        if (b-c) == 5:
            if currentframe !=5:
                if len(faces) == 1:
                    face=faces[0]
                    x, y, w, h = face
                    image=img[y:y+h,x:x+w]
                    # lưu lại những điểm của khuôn mặt
                    name = './Image/' + a + '/' + str(currentframe) + '.jpg'
                    print('Creating...' + name)
                    cv2.imwrite(name, image)
                    currentframe += 1
            else:
                break

    face_training.train()
    face_training.eye_train()
    del (camera)


"""def indexscreen(request):
    try:
        return render(request,'login/screen.html')
    except HttpResponseServerError:
        print('error')


@gzip.gzip_page
def dynamic_stream(request,stream_path="video"):
    try :
        return StreamingHttpResponse(get_frame(),content_type="multipart/x-mixed-replace;boundary=frame")
    except :
        return "error"
"""
global name
name =""
global id_check
id_check=""
#stream_video
def video_feed(request):
    try:
        return StreamingHttpResponse(get_frame(), content_type='multipart/x-mixed-replace; boundary=frame')
    except:
        return "error"

#Login
class login(View):
    def get(self,request):
        return render(request,'login/login.html')

class but_login(View):
    def get(self, request):
        return render(request, 'login/login_but.html', {'id_check': no.getsensordata()})

    def post(self,request):
        id_check=request.POST.get('id_check')
        try:
            DocGia.objects.get(id_DG=id_check)
            print(id_check)
            try:
                c=camera_recognize(id_check)
                print("flag",c)
                if (c==1):
                    return render(request,'login/success.html')
                else:
                    return HttpResponse("khuôn mặt ko khớp")
            except:
                return "error"
        except ObjectDoesNotExist:
            return HttpResponse("chua đăng ki")
        #return render(request,'login/login_camera.html')


#nhận dạng khuôn mặt
def camera_recognize(check):
    camera = cv2.VideoCapture(1)
    face_cascade = cv2.CascadeClassifier('I:\Program Files\Python\Lib\site-packages\cv2\data\haarcascade_frontalface_alt.xml')
    eyes_cascade = cv2.CascadeClassifier('I:\Program Files\Python\Lib\site-packages\cv2\data\haarcascade_eye.xml')

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")

    eyes_recognizer = cv2.face.LBPHFaceRecognizer_create()
    eyes_recognizer.read("eyes-trainner.yml")

    labels = {"person_name": 1}
    with open("labels.pickle", "rb") as f:
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}

    eyes_labels = {"eyes_person_name": 1}
    with open("eyeslabels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        eyes_labels = {v: k for k, v in og_labels.items()}

    flag = 0;
    start = datetime.datetime.now()
    second_start = start.second
    minute_start = start.minute
    hour_start = start.hour
    c = hour_start * 3600 + minute_start * 60 + second_start
    while True:
        end = datetime.datetime.now()
        second_end = end.second
        minute_end = end.minute
        hour_end = end.hour
        b = hour_end * 3600 + minute_end * 60 + second_end
        ret, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=5)
        eyes = eyes_cascade.detectMultiScale(frame)
        if(flag ==0):
            if (b - c) != 10:
                print(b - c)
                for (x, y, w, h) in faces:
                    for(ex,ey,ew,eh) in eyes:
                        roi_gray = gray[y:y + h, x:x + w]  # (cord1-height,cord2-height)
                        capture_eyes = gray[ey:ey + eh, ex:ex + ew]
                        id_, conf = recognizer.predict(roi_gray)
                        temp, eyes_conf = eyes_recognizer.predict(capture_eyes)

                        if conf and eyes_conf:
                            print("id",id_)
                            #print("eyes",eyes_conf)
                            print("conf",conf)
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            name = (labels[id_])
                        #print("name", name)
                            print(type(check))
                            print(type(name))
                            if name==check:
                                flag=1
                                print(1)
                                break;
            else:
                flag=2
                break;
                        #color = (255, 243, 153)
                        #stroke = 2
                        #cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
                """color = (255, 0, 0)
                stroke = 2
                end_cord_x = x + w
                end_cord_y = y + h
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
                cv2.rectangle(frame,(ex,ey),(ex+ew,ey+eh),color,stroke)
                imgencode = cv2.imencode('.jpg', frame)[1]
                stringData = imgencode.tostring()
                yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + stringData + b'\r\n')"""
        else:
            break;
    return flag
    del (camera)


#hiển thị video
def video_cam_recog(request):
    try:
        return StreamingHttpResponse(camera_recognize(), content_type='multipart/x-mixed-replace; boundary=frame')
    except:
        return "error"


