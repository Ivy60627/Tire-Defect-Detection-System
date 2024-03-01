import os
import cv2
import numpy as np
from math import cos, sin


def show_xy(event, x, y, flags, userdata):
    if (event != 0):
        print(event, x, y, flags)


class GetROI:
    def __init__(self):
        self.path = './transformation/'
        self.pic_list = []

        # 求旋轉矩陣
        self.theta = np.deg2rad(-60)
        self.rot = np.array([[cos(self.theta), -sin(self.theta)],
                             [sin(self.theta), cos(self.theta)]])

    def read_image(self):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                file = file.rstrip(".png")
                self.pic_list.append(file)
        return self.pic_list

    def get_roi(self, pic_list):
        for pic in pic_list:
            self.img = cv2.imread(self.path + pic + '.png', )

            x1 = 2200
            y1 = 200
            x2 = 3910
            y2 = 3160

            # 求旋轉後的向量
            v = np.array([x1 - x2, y1 - y2])
            v2 = np.dot(self.rot, v)

            x3 = [int(x2 + v2[0]), int(y2 + v2[1])]
            if x3[1] > 4000:
                x3[1] = 4000

            # 畫紅線
            cv2.line(self.img, (x1, y1), (x2, y2), (0, 0, 255), 5)
            cv2.line(self.img, x3, (x2, y2), (0, 0, 255), 5)
            cv2.line(self.img, (x1, y1), x3, (0, 0, 255), 5)

            # 加ROI遮罩
            mask = np.zeros((4000, 4000), dtype=np.uint8)
            x_data = np.array([x1, x2, x3[0]])
            y_data = np.array([y1, y2, x3[1]])
            pts = np.vstack((x_data, y_data)).astype(np.int32).T
            cv2.fillPoly(mask, [pts], (255), 8, 0)
            self.img = cv2.bitwise_and(self.img, self.img, mask=mask)

            # 取得圖像的高度和寬度
            # (h, w) = self.img.shape[:2]
            # # 計算圖像的中心點
            # center = (h // 2, w // 2)
            # # 取得旋轉矩陣
            # M = cv2.getRotationMatrix2D(center, 91, 1.0)
            # cos = np.abs(M[0, 0])
            # sin = np.abs(M[0, 1])
            # nw = int((h * sin) + (w * cos))
            # nh = int((h * cos) + (w * sin))
            # # 旋轉圖像
            # self.output = cv2.warpAffine(self.img, M, (nw, nh))
            # self.output = self.output[1000:3700, 1000:3900]
            self.output = self.img[0:3300, 300:4000]
            cv2.imwrite('roi/' + pic + '.png', self.output)
        return self.output
