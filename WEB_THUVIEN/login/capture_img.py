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

import os

def camera():
    camera = cv2.VideoCapture(0)
    a = "trung"
    try:
    # creating a folder named data
        if not os.path.exists('Image/' + a):
            os.makedirs('Image/' + a)

# if not created then raise error
    except OSError:
        print('Error: Creating directory of Image')
    currentframe = 0
    while True:
        ret, img = camera.read()
        img = cv2.resize(img, (200, 150))
        imgencode = cv2.imencode('.jpg', img)[1]
        if currentframe != 10:
            name = './Image/' + a + '/' + str(currentframe) + '.jpg'
            print('Creating...' + name)
            cv2.imwrite(name, img)
            stringData = imgencode.tostring()
            yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + stringData + b'\r\n')
            currentframe += 1
        else:
            break
    del (camera)