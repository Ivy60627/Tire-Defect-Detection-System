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
    
        x1 = 2420 #調整左右
        y1 = 0    #調整上下
        x2 = x1 + 1700 + 85
        y2 = y1 + 2930 + 146
    
        #求旋轉後的向量
        v = np.array([x1-x2, y1-y2])
        v2 = np.dot(rot, v)
        
        x3 = [int(x2+v2[0]-50), int(y2+v2[1])]
        if x3[1]>4000:
            x3[1]=4000

        # 顏色 粗細 橢圓大小
        color = (0, 0, 255)
        thickness = 10
        oval_size=(3000,2950)
        
        # 畫橢圓
        cv2.ellipse(img, (x1,y1), oval_size,90,0,360,color,thickness)
        # 畫線
        cv2.line(img, (x1, y1), (x2, y2), color, thickness)
        cv2.line(img, x3, (x2, y2), color, thickness)
        cv2.line(img, (x1, y1), x3, color, thickness)

        # 加ROI遮罩
        mask_triangle = np.zeros((4000,4000), dtype=np.uint8)
        mask_oval = np.zeros((4000,4000), dtype=np.uint8)
        
        # 畫一個填充白色的橢圓遮罩
        cv2.ellipse(mask_oval, (x1,y1), oval_size, 90, 0, 360, (255), -1)
        
        # 選三個點填充白色的三角形遮罩
        x_data = np.array([x1,x2,x3[0]])
        y_data = np.array([y1,y2,x3[1]])
        pts=np.vstack((x_data,y_data)).astype(np.int32).T       
        cv2.fillPoly(mask_triangle,[pts],(255),8,0)
        
        mask_triangle=cv2.bitwise_and(mask_triangle, mask_oval)
        img=cv2.bitwise_and(img, img, mask=mask_triangle)
        output = img[0:3300, 300:4000]

        cv2.imwrite(f'{output_path}{pic}.png', output)
    return output
