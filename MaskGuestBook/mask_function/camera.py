import threading
import cv2.cv2 as cv2
from .timer import timer
from .detect_v import detect_v
from .detect_mask import detect_mask

class camera(threading.Thread):
    def __init__(self, cam, target=None):
        self.cam = cam
        threading.Thread.__init__(self)
        print("camera")
        self.timer = timer(self, cam)

        self.pro2 = detect_v(self.timer)
        self.pro2.set_cam(self.cam.get_frame_())

        self.pro = detect_mask(self.pro2)
        self.pro.set_cam(self.cam.get_frame_())
        self.pro.start()

        self.break_flag = True

    def set_frame(self, count_file):
        self.flag = False
        self.count_file = count_file


    def get_frame(self, frame):
        width = frame.shape[1]
        height = frame.shape[0]
        count = cv2.imread(self.count_file)
        count = cv2.resize(count, (width, height))
        frame_count = cv2.addWeighted(frame, 0.5, count, 1.0, 0)

        return frame_count

    def run(self):
        self.flag = True
        while self.break_flag:
            if self.flag == False:
                self.cam.frame = self.get_frame(self.cam.get_frame_())
            self.pro.set_cam(self.cam.get_frame_())
            self.pro2.set_cam(self.cam.get_frame_())