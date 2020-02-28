from django.shortcuts import render
from django.http import HttpResponse
from .forms import Register
from . import nouden as no
from . import capture_img
from django.views import View
import cv2
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
    camera = cv2.VideoCapture(0)
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
            data=cv2.rectangle(img, (x, y), (end_cord_x, end_cord_y), color, stroke)
        imgencode = cv2.imencode('.jpg',data )[1]
        stringData = imgencode.tostring()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + stringData + b'\r\n')
        end = datetime.datetime.now()
        second_end = end.second
        minute_end=end.minute
        hour_end=end.hour
        b=hour_end*3600+minute_end*60+second_end

        if b-c == 10:
            if currentframe != 10:
                if len(faces) == 1:
                    face = faces[0]
                    # lưu lại những điểm của khuôn mặt
                    x, y, w, h = face
                    im_face = img[y:y + h, x:x + w]
                    name = './Image/' + a + '/' + str(currentframe) + '.jpg'
                    print('Creating...' + name)
                    cv2.imwrite(name, im_face)
                    currentframe += 1
            else:
                break

    face_training.train()
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
        except ObjectDoesNotExist:
            return HttpResponse("chua đăng ki")
        return render(request,'login/login_camera.html')


#nhận dạng khuôn mặt
def camera_recognize():
    camera = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('I:\Program Files\Python\Lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")

    labels = {"person_name": 1}
    with open("labels.pickle", "rb") as f:
        labels = pickle.load(f)
        labels = {v: k for k, v in labels.items()}

    while True:
        name=""
        ret, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]  # (cord1-height,cord2-height)
            id_, conf = recognizer.predict(roi_gray)
            if conf >= 45 and conf <= 85:
                print("id",id_)
                print("conf",conf)
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = (labels[id_])
                print("name",name)
                color = (255, 243, 153)
                stroke = 2
                cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            color = (255, 0, 0)
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            font = cv2.FONT_HERSHEY_SIMPLEX
            img2=cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)+cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            imgencode = cv2.imencode('.jpg', img2)[1]
            stringData = imgencode.tostring()
            yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + stringData + b'\r\n')

    del (camera)


#hiển thị video
def video_cam_recog(request):
    try:
        return StreamingHttpResponse(camera_recognize(), content_type='multipart/x-mixed-replace; boundary=frame')
    except:
        return "error"
