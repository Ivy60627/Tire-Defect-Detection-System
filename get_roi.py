import os
import cv2
import numpy as np
from math import cos, sin
import matplotlib.pyplot as plt

def show_xy(event,x,y,flags,userdata):
    if (event != 0):       
        print(event,x,y,flags)

path = './transformation/'
pic_list = []

for root,dirs,files in os.walk(path):
	for file in files:
		file=file.rstrip(".png")
		pic_list.append(file)

#求旋轉矩陣
theta = np.deg2rad(-60)
rot = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
        
for pic in pic_list[:6]:
    img = cv2.imread(path +  pic + '.png',)     
    

    x1 = 2180 #調整左右
    y1 = 0    #調整上下
    x2 = x1 + 1700
    y2 = y1 + 2930
    
    # cv2.namedWindow('image', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('image',img)
    # cv2.setMouseCallback('image', show_xy)  # 設定偵測事件的函式與視窗
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    #求旋轉後的向量
    v = np.array([x1-x2, y1-y2])
    v2 = np.dot(rot, v)
    
    x3 = [int(x2+v2[0]-50), int(y2+v2[1])]
    if x3[1]>4000:
        x3[1]=4000
        
    # 畫紅線
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 5)
    cv2.line(img, x3, (x2, y2), (0, 0, 255), 5)
    cv2.line(img, (x1, y1), x3, (0, 0, 255), 5)
                 
    img_original = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.subplot(1,2,1)
    plt.imshow(img_original)
    plt.xticks([]), plt.yticks([])
    plt.title('original image')
                
    # 加ROI遮罩
    mask = np.zeros((4000,4000), dtype=np.uint8)

    x_data = np.array([x1,x2,x3[0]])
    y_data = np.array([y1,y2,x3[1]])
    pts=np.vstack((x_data,y_data)).astype(np.int32).T
    cv2.fillPoly(mask,[pts],(255),8,0)
    img=cv2.bitwise_and(img, img, mask=mask)
    
    output = img[0:3300, 300:4000]
    # cv2.namedWindow('image', cv2.WINDOW_KEEPRATIO)
    # cv2.setMouseCallback('image', show_xy)  # 設定偵測事件的函式與視窗
    # cv2.imshow('image',output)
    


    img_gardien = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    plt.subplot(1,2,2)
    plt.imshow(img_gardien)
    plt.xticks([]), plt.yticks([])
    plt.title('output')
    
    cv2.imwrite('roi/' + pic + '_roi.png', output)
    
    
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

