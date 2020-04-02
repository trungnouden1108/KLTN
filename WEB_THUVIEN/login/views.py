from django.shortcuts import render
from django.http import HttpResponse
from .forms import Register,Sach
from . import nouden as no
from django.views import View
from django.http import StreamingHttpResponse,HttpResponseServerError,HttpResponseRedirect,JsonResponse
from .models import Book,DocGia,Cart,Check_book,Category_Book
import serial
import numpy as np
import cv2
import pickle
import datetime
import time
from django.views.decorators import gzip
import os
from django.core.exceptions import ObjectDoesNotExist
from . import face_training
from django.contrib import messages
import serial
from django.utils import timezone
import pytz
from django.db.models import (
    Count,
)
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
                if (c==1):
                    id_user=id_check
                    user = DocGia.objects.get(id_DG=id_user)
                    book=Book.objects.all()
                    book1=book.filter(active=True)
                    sl=book1.aggregate(Count('id'))
                    Data = {'list_book': Book.objects.all(),'sl':sl, 'tenDG': user.ten_DG}
                    return render(request, 'book/book.html', Data)
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
                        print("eyes", eyes_conf)
                        print("conf", conf)
                        #print("1",flag)
                        if conf >=20 and conf <=45 and eyes_conf>=100 and eyes_conf <=150:

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

def detailbook(request,id):
    user = DocGia.objects.get(id_DG=id_user)
    detailbook=Book.objects.get(id=id)
    return render(request,'book/detailbook.html',{'detailbook':detailbook,'tenDG':user.ten_DG})

"""cart={}
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
        return render(request,'cart/addcart.html',{'cart':cartInfo})"""

"""class yourcart(View):
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
"""

class book(View):
    def get(self,request):
        user = DocGia.objects.get(id_DG=id_user)
        book = Book.objects.all()
        book1 = book.filter(active=True)
        sl = book1.aggregate(Count('id'))
        Data={'list_book':Book.objects.all(),'sl':sl,'tenDG':user.ten_DG}
        return render(request,'book/book.html',Data)



def book_cate1(request):
    user = DocGia.objects.get(id_DG=id_user)
    get_cate=Book.objects.filter(category=Category_Book.objects.get(title="Giáo trình"))
    get_cate2=get_cate.filter(active=True)
    sl=get_cate2.aggregate(Count('id'))
    Data={'list_book':Book.objects.filter(category=Category_Book.objects.get(title="Giáo trình")),'sl':sl,'tenDG':user.ten_DG,
          'list_book1':Book.objects.all()}
    return render(request,'book/book_cate1.html',Data)

def book_cate2(request):
    user = DocGia.objects.get(id_DG=id_user)
    get_cate=Book.objects.filter(category=Category_Book.objects.get(title="Văn học nghệ thuật"))
    get_cate2=get_cate.filter(active=True)
    sl=get_cate2.aggregate(Count('id'))
    Data={'list_book':Book.objects.filter(category=Category_Book.objects.get(title="Văn học nghệ thuật")),'sl':sl,'tenDG':user.ten_DG,
          'list_book1':Book.objects.all()}
    return render(request,'book/book_cate2.html',Data)

def book_cate3(request):
    user = DocGia.objects.get(id_DG=id_user)
    get_cate=Book.objects.filter(category=Category_Book.objects.get(title="Tâm lý, tâm linh, tôn giáo"))
    get_cate2 = get_cate.filter(active=True)
    sl=get_cate2.aggregate(Count('id'))
    Data={'list_book':Book.objects.filter(category=Category_Book.objects.get(title="Tâm lý, tâm linh, tôn giáo")),'sl':sl,'tenDG':user.ten_DG,
          'list_book1':Book.objects.all()}
    return render(request,'book/book_cate3.html',Data)

def book_cate4(request):
    user = DocGia.objects.get(id_DG=id_user)
    get_cate=Book.objects.filter(category=Category_Book.objects.get(title="Truyện, tiểu thuyết"))
    get_cate2 = get_cate.filter(active=True)
    sl=get_cate2.aggregate(Count('id'))
    Data={'list_book':Book.objects.filter(category=Category_Book.objects.get(title="Truyện, tiểu thuyết")),'sl':sl,'tenDG':user.ten_DG,
          'list_book1':Book.objects.all()}
    return render(request,'book/book_cate4.html',Data)

def book_cate5(request):
    user = DocGia.objects.get(id_DG=id_user)
    get_cate=Book.objects.filter(category=Category_Book.objects.get(title="Văn hóa xã hội - Lịch sử"))
    get_cate2 = get_cate.filter(active=True)
    sl=get_cate2.aggregate(Count('id'))
    Data={'list_book':Book.objects.filter(category=Category_Book.objects.get(title="Văn hóa xã hội - Lịch sử")),'sl':sl,'tenDG':user.ten_DG,
          'list_book1':Book.objects.all()}
    return render(request,'book/book_cate5.html',Data)

def book_cate6(request):
    user = DocGia.objects.get(id_DG=id_user)
    get_cate=Book.objects.filter(category=Category_Book.objects.get(title="Khoa học công nghệ – Kinh tế"))
    get_cate2 = get_cate.filter(active=True)
    sl=get_cate2.aggregate(Count('id'))
    Data={'list_book':Book.objects.filter(category=Category_Book.objects.get(title="Khoa học công nghệ – Kinh tế")),'sl':sl,'tenDG':user.ten_DG,
          'list_book1':Book.objects.all()}
    return render(request,'book/book_cate6.html',Data)

def book_cate7(request):
    user = DocGia.objects.get(id_DG=id_user)
    get_cate=Book.objects.filter(category=Category_Book.objects.get(title="Chính trị - Pháp luật"))
    get_cate2 = get_cate.filter(active=True)
    sl=get_cate2.aggregate(Count('id'))
    Data={'list_book':Book.objects.filter(category=Category_Book.objects.get(title="Chính trị - Pháp luật")),'sl':sl,'tenDG':user.ten_DG,
          'list_book1':Book.objects.all()}
    return render(request,'book/book_cate7.html',Data)
a=""
b=""
c=""

#Scan id
def scan_id(request):
    if request.is_ajax():
        global a
        try:
            a = no.getsensordata()
        except:
            print("....")
        context={'tagid1':a,'tagid2':a,'tagid3':a}
        return JsonResponse(context)
    else:
        return HttpResponse("This route only handles AJAX requests")


class bor_book(View):
    def get(self, request):
        user = DocGia.objects.get(id_DG=id_user)
        return render(request,'muontra/muonsach.html',{'tenDG':user.ten_DG,'list_book1':Book.objects.all()})

    def post(self,request):
        flag=0
        id_book1=request.POST.get('book_1')
        id_book2=request.POST.get('book_2')
        id_book3=request.POST.get('book_3')
        try:
            Cart.objects.get(id_user=id_user)
            flag=1
        except ObjectDoesNotExist:
            flag=0
        if flag==1:
            messages.success(request, "Bạn đã mượn sách rồi, vui lòng trả sách đã mượn thì mới có thể mượn thêm sách")
            user = DocGia.objects.get(id_DG=id_user)
            return render(request, 'muontra/muonsach.html', {'tenDG': user.ten_DG, 'list_book1': Book.objects.all()})
        elif flag==0:
            if(id_book1 !="" and id_book1 == id_book2 and id_book2 == id_book3):
                user = DocGia.objects.get(id_DG=id_user)
                messages.error(request,"3 quyển sách trùng nhau")
                return render (request,'muontra/muonsach.html',{'tenDG': user.ten_DG, 'list_book1': Book.objects.all()})
            elif (id_book1 != "" and id_book3!="" and id_book2!=""):
                    if(id_book1 == id_book2 or id_book2 ==id_book3 or id_book1==id_book3):
                        user = DocGia.objects.get(id_DG=id_user)
                        messages.error(request, "2 quyển sách trùng nhau")
                        return render(request, 'muontra/muonsach.html',
                              {'tenDG': user.ten_DG, 'list_book1': Book.objects.all()})
            elif (id_book1 == "" and id_book2 == "" and id_book3 == ""):
                messages.error(request, "Vui lòng scan sách")
                user = DocGia.objects.get(id_DG=id_user)
                return render(request, 'muontra/muonsach.html',
                              {'tenDG': user.ten_DG, 'list_book1': Book.objects.all()})
            store_cart = Cart(id_user=id_user, id_bor1=id_book1,id_bor2=id_book2,id_bor3=id_book3)
            store_cart.save()
            if(id_book1 !=""):
                check_id=Check_book(id_bor=id_book1)
                check_id.save()
                bookDetail = Book.objects.get(id_book=id_book1)
                if(bookDetail.active==False):
                    messages.error(request, "Sách đã được mượn rồi")
                    user = DocGia.objects.get(id_DG=id_user)
                    return render(request, 'muontra/muonsach.html',
                                  {'tenDG': user.ten_DG, 'list_book1': Book.objects.all()})
                bookDetail.active = False
                bookDetail.save()
            if(id_book2 !=""):
                check_id = Check_book(id_bor=id_book2)
                check_id.save()
                bookDetail = Book.objects.get(id_book=id_book2)
                if (bookDetail.active == False):
                    messages.error(request, "Sách đã được mượn rồi")
                    user = DocGia.objects.get(id_DG=id_user)
                    return render(request, 'muontra/muonsach.html',
                                  {'tenDG': user.ten_DG, 'list_book1': Book.objects.all()})
                bookDetail.active = False
                bookDetail.save()
            if(id_book3 !=""):
                check_id = Check_book(id_bor=id_book3)
                check_id.save()
                bookDetail = Book.objects.get(id_book=id_book3)
                if (bookDetail.active == False):
                    messages.error(request, "Sách đã được mượn rồi")
                    user = DocGia.objects.get(id_DG=id_user)
                    return render(request, 'muontra/muonsach.html',
                                  {'tenDG': user.ten_DG, 'list_book1': Book.objects.all()})
                bookDetail.active = False
                bookDetail.save()


            messages.success(request,"Bạn đã mượn sách thành công")
            user = DocGia.objects.get(id_DG=id_user)
            return render(request, 'muontra/muonsach.html', {'tenDG': user.ten_DG, 'list_book1': Book.objects.all()})

temp1=""
temp2=""
temp3=""
class ret_book(View):
    def get(self, request):
        user = DocGia.objects.get(id_DG=id_user)
        return render(request, 'muontra/trasach.html', {'tenDG': user.ten_DG, 'list_book1': Book.objects.all()})

    def post(self,request):
        user = DocGia.objects.get(id_DG=id_user)
        global temp1,temp2,temp3
        sum=0
        flag = 0
        i=0
        id_book1 = request.POST.get('book_1')
        id_book2 = request.POST.get('book_2')
        id_book3 = request.POST.get('book_3')
        try:
            Cart.objects.get(id_user=id_user)
            flag=1
        except:
            flag=0
        if flag==1:
            if (id_book1 != "" and id_book1 == id_book2 and id_book2 == id_book3):
                user = DocGia.objects.get(id_DG=id_user)
                messages.error(request, "3 quyển sách trùng nhau")
                return render(request, 'muontra/trasach.html',
                              {'tenDG': user.ten_DG, 'list_book1': Book.objects.all()})
            elif (id_book1 != "" and id_book3 != "" and id_book2 != ""):
                if (id_book1 == id_book2 or id_book2 == id_book3 or id_book1 == id_book3):
                    user = DocGia.objects.get(id_DG=id_user)
                    messages.error(request, "2 quyển sách trùng nhau")
                    return render(request, 'muontra/trasach.html',
                                  {'tenDG': user.ten_DG, 'list_book1': Book.objects.all()})
            elif (id_book1 == "" and id_book2 == "" and id_book3 == ""):
                messages.error(request, "Vui lòng scan sách")
                user = DocGia.objects.get(id_DG=id_user)
                return render(request, 'muontra/trasach.html',
                              {'tenDG': user.ten_DG, 'list_book1': Book.objects.all()})
            check_cart=Cart.objects.get(id_user=id_user)
            tz_hcm = pytz.timezone('Asia/Ho_Chi_Minh')
            time_pre=datetime.datetime.now(timezone.utc)+datetime.timedelta(hours=7)
            print("time_pre",time_pre)

            if (id_book1 != ""):
                if (check_cart.id_bor1 !=id_book1 and check_cart.id_bor2 !=id_book1 and check_cart.id_bor3 !=id_book1):
                    messages.error(request,"Sách không khớp")
                    return render(request,'muontra/trasach.html',{'tenDG': user.ten_DG, 'list_book1': Book.objects.all()})
                temp1=id_book1
                book_bor = Cart.objects.get(id_user=id_user)
                i=i+1
                time_cre=book_bor.created_at
                print("time_create",time_cre)
                t3=time_pre-time_cre
                print(t3)
                sum=sum+no.day(t3.days)

            if (id_book2 != ""):
                if (check_cart.id_bor1 !=id_book2 and check_cart.id_bor2 !=id_book2 and check_cart.id_bor3 !=id_book2):
                    messages.error(request,"Sách trả không khớp")
                    return render(request,'muontra/trasach.html',{'tenDG': user.ten_DG, 'list_book1': Book.objects.all()})
                temp2=id_book2
                book_bor = Cart.objects.get(id_user=id_user)
                i=i+1
                time_cre = book_bor.created_at
                print("time_create", time_cre)
                t3 = time_pre - time_cre
                sum = sum + no.day(t3.days)

            if (id_book3 != ""):
                if (check_cart.id_bor1 !=id_book3 and check_cart.id_bor2 !=id_book3 and check_cart.id_bor3 !=id_book3):
                    messages.success("Sách không khớp")
                    return render(request,'muontra/trasach.html',{'tenDG': user.ten_DG, 'list_book1': Book.objects.all()})
                temp3=id_book3
                book_bor = Cart.objects.get(id_user=id_user)
                i=i+1
                time_cre = book_bor.created_at
                print("time_create", time_cre)
                t3 = time_pre - time_cre
                print(t3)
                sum = sum + no.day(t3.days)


            return render(request,'muontra/thanhtoan.html',{'tenDG': user.ten_DG, 'list_book1': Book.objects.all(),'i':i,'tien':sum,'day':t3.days})
        else:
            messages.error(request,"Bạn chưa mượn sách nào")
            return render(request,'muontra/trasach.html',{'tenDG': user.ten_DG, 'list_book1': Book.objects.all()})

class thanhtoan(View):
    def post(self,request):
        money=request.POST.get('tien')
        a=int(money)
        user=DocGia.objects.get(id_DG=id_user)
        if (user.money_user==0 and a !=0):
            messages.error(request,"Tài khoản của bạn không đủ để thanh toán")
            book = Book.objects.all()
            book1 = book.filter(active=True)
            sl = book1.aggregate(Count('id'))
            return render(request, 'book/book.html', {'tenDG': user.ten_DG, 'sl': sl,
                                                      'list_book': Book.objects.all()})
        else:
            if(temp1 !=""):
                bookDetail = Book.objects.get(id_book=temp1)
                bookDetail.active = True
                bookDetail.save()
                Check_book.objects.filter(id_bor=temp1).delete()
                book_bor = Cart.objects.get(id_user=id_user)
                if (book_bor.id_bor1 == temp1):
                    book_bor.id_bor1 = ""
                    book_bor.save()

                elif (book_bor.id_bor2 == temp1):
                    book_bor.id_bor2 = ""
                    book_bor.save()

                elif (book_bor.id_bor3 == temp1):
                    book_bor.id_bor3 = ""
                    book_bor.save()

            if(temp2 !=""):
                bookDetail = Book.objects.get(id_book=temp2)
                bookDetail.active = True
                bookDetail.save()
                Check_book.objects.filter(id_bor=temp2).delete()
                book_bor = Cart.objects.get(id_user=id_user)
                if (book_bor.id_bor1 == temp2):
                    book_bor.id_bor1 = ""
                    book_bor.save()
                elif (book_bor.id_bor2 == temp2):
                    book_bor.id_bor2 = ""
                    book_bor.save()
                elif (book_bor.id_bor3 == temp2):
                    book_bor.id_bor3 = ""
                    book_bor.save()

            if(temp3 !=""):
                bookDetail = Book.objects.get(id_book=temp3)
                bookDetail.active = True
                bookDetail.save()
                Check_book.objects.filter(id_bor=temp3).delete()
                book_bor = Cart.objects.get(id_user=id_user)
                if (book_bor.id_bor1 == temp3):
                    book_bor.id_bor1 = ""
                    book_bor.save()
                elif (book_bor.id_bor2 == temp3):
                    book_bor.id_bor2 = ""
                    book_bor.save()
                elif (book_bor.id_bor3 == temp3):
                    book_bor.id_bor3 = ""
                    book_bor.save()

            check_cart = Cart.objects.get(id_user=id_user)
            if (check_cart.id_bor1 == "" and check_cart.id_bor2 == "" and check_cart.id_bor3 == ""):
                Cart.objects.filter(id_user=id_user).delete()
            user.money_user=user.money_user-a
            user.save()
        messages.success(request,"Trả sách thành công")
        book = Book.objects.all()
        book1 = book.filter(active=True)
        sl = book1.aggregate(Count('id'))
        return render(request, 'book/book.html', {'tenDG': user.ten_DG,'sl':sl,'list_book':Book.objects.all()})


d=""
def check_book(request):
    if request.is_ajax():
        global d
        flag=0
        try:
            d = no.getsensordata()
            try:
                Check_book.objects.get(id_bor=d)
                flag=1
            except ObjectDoesNotExist:
                flag=2
        except:
            print("....")
        if flag==1:
            no.sendarduino_1()
            flag=0
        elif flag==2:
            no.sendarduino_2()
            flag=0
        context={'id_book':d}
        return JsonResponse(context)
    else:
        return HttpResponse("This route only handles AJAX requests")

def testcheck(request):
    return render(request, 'check/check.html', {})

