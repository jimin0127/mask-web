from ..playSound import playsound
import threading
import os
from datetime import datetime
import time
import cv2.cv2 as cv2

directory = os.getcwd()
filePath = directory + '/MaskGuestBook/static/resources/images/'
countFilePath = directory + '/MaskGuestBook/count_down_img/countDown'

playsound = playsound()

class timer(threading.Thread):
    def __init__(self, camera, cam):
        threading.Thread.__init__(self)
        self.camera = camera
        self.cam = cam

    def set_cam(self, frame):
        self.cam = frame

    def run(self):
        playsound.play_countdown()
        for i in range(1, 3+1):
            self.camera.set_frame(countFilePath+ str(i) + '.png')
            time.sleep(1)
            if i == 3:
                self.camera.flag = True
                playsound.play_camera()
        time.sleep(0.5)
        self.camera.break_flag = False
        now = datetime.now()
        self.fileName = filePath + now.strftime('%y%m%d_%H%M%S') + '.png'
        cv2.imwrite(self.fileName, self.cam.get_frame_())

        self.cam.flag = False