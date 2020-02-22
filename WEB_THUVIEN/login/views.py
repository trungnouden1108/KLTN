from django.shortcuts import render
from django.http import HttpResponse
from .forms import Register
from . import nouden as no
from django.views import View
import cv2
from django.http import StreamingHttpResponse,HttpResponseServerError
from .models import DocGia
import serial
import numpy as np
import cv2
import pickle
import time
from django.views.decorators import gzip

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
    camera =cv2.VideoCapture(0)
    while True:
        key = cv2.waitKey(1)
        if key & 0xFF == ord("q"):
            break
        _, img = camera.read()
        img=cv2.resize(img,(200,150))
        imgencode=cv2.imencode('.jpg',img)[1]
        cv2.imwrite('trung.jpg',img)
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

    del camera
    camera.release()
    cv2.destroyAllWindows()


def indexscreen(request):
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




