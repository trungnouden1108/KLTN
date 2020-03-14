from django.shortcuts import render
from django.http import HttpResponse
from .forms import Register,Sach
from . import nouden as no
from django.views import View
from django.http import StreamingHttpResponse,HttpResponseServerError,HttpResponseRedirect
from .models import Book,DocGia,Cart
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
from django.contrib import messages

# Create your views here.

global name
name =""
global id_check
id_check=""
id_user="null"

class begin(View):
    def get(self,request):
        return render(request,'login/begin.html')


class register(View):
    def get(self, request):
        while True:
            q = Register()
            return render(request, 'login/register.html', {'f': q, 'id_card': no.getsensordata()})

    def post(self,request):
        q=Register(request.POST)
        if q.is_valid():
            q.save()
            messages.success(request,"Tài khoản được tạo thành công")
            return render(request,'login/begin.html')
        else:
            messages.error(request,"ID đã tồn tại")
            return render(request,'login/begin.html')


def get_frame():
    camera = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('I:\Program Files\Python\Lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml')

    a=no.getsensordata()
    b=a
    try:
        #creating a folder named data
        if os.path.exists('Image/' + b):
            os.remove('Image/' + b)
            os.makedirs('Image/' + b)
            print("trung")
        else:
            os.makedirs('Image/' + b)
    #if not created then raise error
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
        end = datetime.datetime.now()
        second_end = end.second
        minute_end = end.minute
        hour_end = end.hour
        b = hour_end * 3600 + minute_end * 60 + second_end
        ret, img = camera.read()
        img1=img
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
            font = cv2.FONT_HERSHEY_SIMPLEX
            stroke = 2
            if currentframe!=5:
                cv2.putText(img1, "Processing", (150,100), font, 2, color, stroke, cv2.LINE_AA)
            else:
                cv2.putText(img1, "Done", (240, 100), font, 2, color, stroke, cv2.LINE_AA)

        imgencode = cv2.imencode('.jpg',img )[1]
        stringData = imgencode.tostring()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + stringData + b'\r\n')

        if currentframe !=5:
            if b - c == 2:
                if len(faces) == 1:
                    face=faces[0]
                    x, y, w, h = face
                    image=img[y:y+h,x:x+w]
                # lưu lại những điểm của khuôn mặt
                    name = './Image/' + a + '/' + str(currentframe) + '.jpg'
                    print('Creating...' + name)
                    cv2.imwrite(name, image)
                    currentframe += 1
                    c=b
        else:
            break

    face_training.train()
    face_training.eye_train()
    del (camera)




#stream_video
def video_feed(request):
    try:
        return StreamingHttpResponse(get_frame(), content_type='multipart/x-mixed-replace; boundary=frame')
    except:
        return "error"

#Login


class login(View):
    def get(self, request):
        return render(request, 'login/login.html', {'id_check': no.getsensordata()})

    def post(self,request):
        id_check=request.POST.get('id_check')
        global id_user
        try:
            DocGia.objects.get(id_DG=id_check)
            try:
                c = camera_recognize(id_check)
                print("flag",c)
                if (c==1):
                    id_user=id_check
                    print('trung', id_user)
                    Data_book = {'list_book': Book.objects.all().order_by("-time_create"), 'id_user': id_user}
                    return render(request, 'cart/list_book.html', Data_book)
                else:
                    messages.error(request,"Khuôn mặt không khớp")
                    return render(request,'login/begin.html')
            except:
                return "error"
        except ObjectDoesNotExist:
            messages.error(request,"ID chưa được đăng kí")
            return render(request,'login/begin.html')



#nhận dạng khuôn mặt
def camera_recognize(check):
    camera = cv2.VideoCapture(0)
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
            if (b - c) != 15:
                for (x, y, w, h) in faces:
                    for(ex,ey,ew,eh) in eyes:
                        roi_gray = gray[y:y + h, x:x + w]  # (cord1-height,cord2-height)
                        capture_eyes = gray[ey:ey + eh, ex:ex + ew]
                        id_, conf = recognizer.predict(roi_gray)
                        temp, eyes_conf = eyes_recognizer.predict(capture_eyes)
                        #print("1",flag)
                        if conf >=25 and conf <=45 and eyes_conf>=120 and eyes_conf <=135:
                            #print("eyes",eyes_conf)
                            #print("conf",conf)
                            #print("2",flag)
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            name = (labels[id_])
                            upper_name=name.upper()
                            #print("name", upper_name)
                            if upper_name==check:
                                flag=1
                                #print("trung")
                    if flag==1:
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
        return StreamingHttpResponse(get_frame(), content_type='multipart/x-mixed-replace; boundary=frame')
    except:
        return "error"


#------------------Book------------------#
class input_book(View):
    def get(self,request):
        b=Sach()
        return render(request,'cart/nhapsach.html',{'b':b,'id_book':no.getsensordata()})

    def post(self,request):
        b=Sach(request.POST,request.FILES)
        if b.is_valid():
            im=b.save(commit=False)
            im.image_book=request.FILES['image_book']
            im.save()
            return render(request,'cart/success.html')
        else:
            return render(request,'cart/fail.html')

def list_book(request):
    print('trung',id_user)
    Data_book={'list_book':Book.objects.all().order_by("-time_create"),'id_user':id_user}
    return render(request,'cart/list_book.html',Data_book)

def view_book(request,id):
    view_book=Book.objects.get(id=id)
    return render(request,'cart/view_book.html',{'view_book':view_book,'id_user':id_user})

cart={}
def addcart(request):
    if request.is_ajax():
        id=request.POST.get('id')
        bookDetail=Book.objects.get(id=id)
        if id in cart.keys():
            BookCart={
                'id_book':bookDetail.id_book,
                'name':bookDetail.title,
                'image':str(bookDetail.image_book.url),
            }
        else:
            BookCart = {
                'id_book': bookDetail.id_book,
                'name': bookDetail.title,
                'image': str(bookDetail.image_book.url),
            }
        cart[id]=BookCart
        request.session['cart']=cart
        cartInfo=request.session['cart']
        return render(request,'cart/addcart.html',{'cart':cartInfo})

class yourcart(View):
    def get(self,request):
        return render(request,'cart/yourcart.html')

    def post(self,request):
        cartInfo=request.session['cart']
        flag=0
        for key,value in cartInfo.items():
            store_cart=Cart(id_user=id_user,id_bor=value['id_book'])
            store_cart.save()
            bookDetail = Book.objects.get(id=key)
            bookDetail.active=False
            bookDetail.save()
            no.sendidbook(value['id_book'])
            flag=flag+1
        if(flag != 0):
            return HttpResponse('success')
        else:
            return HttpResponse('mươn ko thành công')