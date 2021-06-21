import threading
import cv2.cv2 as cv2
import cvlib as cv
import numpy as np

class detect_v(threading.Thread):
    def __init__(self, timer):
        threading.Thread.__init__(self)
        self.sample_p = 0
        self.timer = timer

    def set_cam(self, frame):
        self.cam = frame

    def detect(self, img):
        face, confidence = cv.detect_face(img)
        if len(face) == 0:
            return []

        return face

    def removeFaceArea(self, img):
        faces = self.detect(img)
        for x1, y1, x2, y2 in faces:
            cv2.rectangle(img, (x1 - 10, y1), (x2 + 20, y2+50), (0, 0, 0), -1)
        return img


    def make_mask_image(self, img_bgr):
        #Hue(색상), Saturation(채도), Value(진하기)
        img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

        low = (0, 30, 0) # 청록
        #low = (0, 75, 150) # 갈색
        #low = (0, 40, 80) # 갈색
        high = (15, 255, 255) # 노랑
        # 범위 안에 들어가면 검은색 0, 들어가지 않으면 1 -> 흑백 사진으로, 살구색을 추출하기 위해
        img_mask = cv2.inRange(img_hsv, low, high)
        return img_mask


    def findMaxArea(self, contours):
        max_contour = None
        max_area = -1

        for contour in contours:
            # contour의 윤곽영역 면적구하기
            area = cv2.contourArea(contour)


            # contour로 직사각형의 모양을 그림, 직사각형의 4면을 리턴
            x, y, w, h = cv2.boundingRect(contour)

            # ??????
            if (w * h) * 0.4 > area:
                continue

            # 손의 방향을 지정, 세로 X, 기로 O
            if w > h:
                continue

            # 최대 면적 윤곽 구하기, 얼굴은 이미 제외 되어 있음
            if area > max_area:
                max_area = area
                max_contour = contour

        if max_area < 10000:
            max_area = -1

        return max_area, max_contour

    def distanceBetweenTwoPoints(self, start, end):
        x1, y1 = start
        x2, y2 = end

        return int(np.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2)))

    def calculateAngle(self, A, B):
        # 거리 계산(벡터 끼리의 연산)
        A_norm = np.linalg.norm(A)
        B_norm = np.linalg.norm(B)
        # 행렬 곱
        C = np.dot(A, B)

        # 각도 계산
        angle = np.arccos(C / (A_norm * B_norm)) * 180 / np.pi
        return angle


    def getFingerPosition(self, max_contour, img_result, debug):
        points1 = []

        # STEP 6-1
        M = cv2.moments(max_contour)

        # Contour의 중심값(무게중심)을 찾기
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        # 0.02 * cv.arcLength(max_contour, True)만큼 꼭짓점의 개수를 줄여 새로운 곡선을 리턴
        max_contour = cv2.approxPolyDP(max_contour, 0.02 * cv2.arcLength(max_contour, True), True)

        # 블록껍질(경계면을 둘러싸는 다각형을 구하는 알고리즘) : 스크랜스키 -> 볼록한 외관을 찾는다.
        try :
            hull = cv2.convexHull(max_contour)
        except :
            return

        for point in hull:
            if cy > point[0][1]: # ?????
                points1.append(tuple(point[0])) # 손가락 위치 추가

        if debug:
            cv2.drawContours(img_result, [hull], 0, (0, 255, 0), 2)
            # 손가락의 위치 그리기
            for point in points1:
                # 이미지, 원의 중심 좌표, 원의 반지름, 색상, 선의 두께
                cv2.circle(img_result, tuple(point), 15, [0, 0, 0], -1)


        # STEP 6-2
        # max_contour의 외곽 경계선을 찾아 손가락 꼭짓점을 찾는다.
        hull = cv2.convexHull(max_contour, returnPoints=False)
        # max_contour 손바닥의 윤곽선과 손가락의 윤곽선을 비교하여 오목하게 들어간 부분을 찾는다.
        try :
            defects = cv2.convexityDefects(max_contour, hull)
        except:
            return

        if defects is None:
            return -1, None

        points2 = []
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(max_contour[s][0])
            end = tuple(max_contour[e][0])
            far = tuple(max_contour[f][0])
            # 손가락이 이루는 꼭짓점의 각도를 구한다.
            angle = self.calculateAngle(np.array(start) - np.array(far), np.array(end) - np.array(far))

            # 손가락이 이루는 각도가 90가 이하면
            if angle < 90:
                if start[1] < cy:
                    points2.append(start)

                if end[1] < cy:
                    points2.append(end)


        if debug:
            cv2.drawContours(img_result, [max_contour], 0, (255, 0, 255), 2)
            for point in points2:
                cv2.circle(img_result, tuple(point), 20, [0, 255, 0], 5)

        # STEP 6-3
        points = points1 + points2
        points = list(set(points))

        # STEP 6-4
        new_points = []
        for p0 in points:

            i = -1
            for index, c0 in enumerate(max_contour):
                c0 = tuple(c0[0])

                if p0 == c0 or self.distanceBetweenTwoPoints(p0, c0) < 20:
                    i = index
                    break

            if i >= 0:
                pre = i - 1
                if pre < 0:
                    pre = max_contour[len(max_contour) - 1][0]
                else:
                    pre = max_contour[i - 1][0]

                next = i + 1
                if next > len(max_contour) - 1:
                    next = max_contour[0][0]
                else:
                    next = max_contour[i + 1][0]

                if isinstance(pre, np.ndarray):
                    pre = tuple(pre.tolist())
                if isinstance(next, np.ndarray):
                    next = tuple(next.tolist())

                angle = self.calculateAngle(np.array(pre) - np.array(p0), np.array(next) - np.array(p0))

                if angle < 90:
                    new_points.append(p0)

        return 1, new_points



    def run(self):
        while True:
            # STEP 1
            img_bgr = self.removeFaceArea(self.cam)

            # STEP 2
            img_binary = self.make_mask_image(img_bgr)

            # STEP 3
            # 타원형 터널
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            # 작은 구멍이나 검은 점을 없앤다(kernel로 채우는 것)
            img_binary = cv2.morphologyEx(img_binary, cv2.MORPH_CLOSE, kernel, 1)

            # STEP 4
            # contours : 동일한 색 또는 동일한 색상 강도를 가진 가장 자리를 연결한 선
            # RETR_EXTERNAL : 이미지의 가장 바깥쪽의 contours만 추출
            # CHAIN_APPROX_SIMPLE : 모든 점을 저장하지 않고 끝점만 저장
            contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # STEP 5
            max_area, max_contour = self.findMaxArea(contours)

            if max_area == -1:
                continue

            # STEP 6
            try:
               ret, points = self.getFingerPosition(max_contour, self.cam, False)
            except:
                continue

            # STEP 7
            if ret > 0 and len(points) > 0:
                if len(points) == 2 or len(points) == 1:
                    print(2)
                    self.sample_p += 2

            if self.sample_p >= 20:
                print("찰칵")
                break
        print('stop')
        self.timer.start()