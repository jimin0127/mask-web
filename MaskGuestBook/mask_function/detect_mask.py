from tensorflow.python.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import threading
import os
from ..playSound import playsound
import cv2.cv2 as cv2
import cvlib as cv
import numpy as np

playsound = playsound()

class detect_mask(threading.Thread):
    def __init__(self, pro2):
        threading.Thread.__init__(self)

        file_name = os.getcwd() + '/MaskGuestBook/model.h5'
        print('file load')
        self.model = load_model(file_name)
        self.pro2 = pro2

    def set_cam(self, frame):
        self.cam = frame

    def run(self):
        print('detect start')
        playsound.play_detect_mask()
        flag = False
        while flag == False:
            face, confidence = cv.detect_face(self.cam)
            for idx, f in enumerate(face):
                (startX, startY) = f[0], f[1]
                (endX, endY) = f[2], f[3]

                if 0 <= startX <= self.cam.shape[1] and 0 <= endX <= self.cam.shape[1] and 0 <= startY <= \
                        self.cam.shape[0] and 0 <= endY <= self.cam.shape[0]:

                    face_region = self.cam[startY:endY, startX:endX]

                    face_region1 = cv2.resize(face_region, (224, 224), interpolation=cv2.INTER_AREA)

                    x = img_to_array(face_region1)
                    x = np.expand_dims(x, axis=0)
                    x = preprocess_input(x)

                    prediction = self.model.predict(x)

                    # 마스크 미착용으로 판별된다면
                    if prediction < 0.5:
                        print("No Mask(({:.2f}%)".format((1 - prediction[0][0]) * 100))

                    # 마스크 착용으로 판별된다면(1)
                    else:
                        flag = True
                        playsound.play_pose()
                        print("Mask ({:.2f}%)".format(prediction[0][0] * 100))

        self.pro2.start()