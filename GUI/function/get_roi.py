import os
import cv2
import numpy as np
from math import cos, sin

from function.helper_function import read_image_list


def show_xy(event, x, y, flags, userdata):
    if (event != 0):
        print(event, x, y, flags)


def get_roi(pic_path: str, output_path: str):
    # 求旋轉矩陣
    theta = np.deg2rad(-60)
    rot = np.array([[cos(theta), -sin(theta)],
                    [sin(theta), cos(theta)]])
    for pic in read_image_list(pic_path)[:6]:
        img = cv2.imread(pic_path + pic + '.png')

        p1 = (2200, 150)
        p2 = (3900, 3080)

        # 求旋轉後的向量
        v1 = np.array([p1[0] - p2[0], p1[1] - p2[1]])
        v2 = np.dot(rot, v1)

        p3 = [int(p2[0] + v2[0] - 50), int(p2[1] + v2[1])]
        if p3[1] > 4000:
            p3[1] = 4000

        # 畫線
        color = (255, 255, 255)
        cv2.line(img, p1, p2, color, 5)
        cv2.line(img, p2, p3, color, 5)
        cv2.line(img, p1, p3, color, 5)

        # 加ROI遮罩
        mask = np.zeros((4000, 4000), dtype=np.uint8)
        x_data = np.array([p1[0], p2[0], p3[0]])
        y_data = np.array([p1[1], p2[1], p3[1]])
        pts = np.vstack((x_data, y_data)).astype(np.int32).T
        cv2.fillPoly(mask, [pts], (255), 8, 0)
        img = cv2.bitwise_and(img, img, mask=mask)
        output = img[0:3300, 300:4000]

        cv2.imwrite(f'{output_path}{pic}.png', output)
    return output
