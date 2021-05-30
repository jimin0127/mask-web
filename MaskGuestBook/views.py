import os
import threading
from datetime import datetime
from msilib.schema import ListView
#from .maskdemo import *

from Mask import settings
#from .mask import camera

import cv2.cv2 as cv2
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import GuestBookForm
from .models import GuestBook, Image, GuestBookModel


# Create your views here.
def goGuestBook(request):
    form = GuestBookForm()
    if request.method == 'POST':
        return render(
            request,
            'MaskGuestBook/GuestBook.html',
            {'form' : form}
        )
def postGuestBook(request):
    if request.method == 'POST':
        form = GuestBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # return render(
            #     request,
            #     'MaskGuestBook/index.html',
            #     {'form': form}
            # )
            return redirect('index')

    else:
        form = GuestBookForm()
        # return render(
        #     request,
        #     'MaskGuestBook/GuestBook.html',
        #     {'form': form}
        # )
        return render(
            request,
            'MaskGuestBook/GuestBook.html',
            {'form': form}
        )

def index(request):
    guests = GuestBookModel.objects.all()
    images = Image.objects.all()

    return render(request,
                  'MaskGuestBook/list.html',
                  {'guests':guests,
                   'images':images}
                  )

    # return render(
    #     request,
    #     'MaskGuestBook/index.html',
    #     {}
    # )
    # return HttpResponse(str)


def keyboard(request):
    return JsonResponse(
        {
            'type': 'buttons',
            'buttons': ['Mask란', '개발자 소개']
        }
    )


# 웹캠 django에 표시하기

directory = os.getcwd()
filePath = directory + '/MaskGuestBook/static/resources/images/'

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        self.flag = True
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while self.flag:
            (self.grabbed, self.frame) = self.video.read()

    def take_frame(self, name, phone, message):
        now = datetime.now()
        fileName = filePath + now.strftime('%y%m%d_%H%M%S') + '.png'
        print (fileName)
        cv2.imwrite(fileName, self.frame)

        db = GuestBookModel(name= name, phone=phone, message = message, image_name=now.strftime('%y%m%d_%H%M%S'), pub_date=timezone.now())
        db.save()
        self.flag = True
        threading.Thread(target=self.update, args=()).start()



cam = VideoCamera()

def gen(camera):
    while True:
        frame = cam.get_frame()


        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def stream2(request):
    try:
        return StreamingHttpResponse(gen(()), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass

def gen1(camera):
    frame = cam.get_frame()
    yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def capture(request):
    try:
        cam.flag = False
        return StreamingHttpResponse(gen1(()), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass


def live(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        message = request.POST['message']
        cam.take_frame(name, phone, message)
    return render(request, 'MaskGuestBook/live.html')


# def mask(request):
#     mask = camera()
#     mask.start()
#
#     return render(request, 'MaskGuestBook/live.html')




