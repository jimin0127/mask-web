from django.utils import timezone
import os
from datetime import datetime
import threading
import cv2.cv2 as cv2
from MaskGuestBook.models import GuestBookModel

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

    def get_frame_(self):
        return self.frame

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