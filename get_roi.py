import cv2
import numpy as np
from math import cos, sin
import PIL

def show_xy(event,x,y,flags,userdata):
    if (event != 0):       
        print(event,x,y,flags)
        
img = cv2.imread('picture\\image_2_output.png')     

cv2.namedWindow('image', cv2.WINDOW_KEEPRATIO)
cv2.imshow('image',img)
cv2.setMouseCallback('image', show_xy)  # 設定偵測事件的函式與視窗

theta = np.deg2rad(-60)

#求旋轉矩陣
rot = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])

x1 = 391
y1 = 802
x2 = 2967
y2 = 2777

#求旋轉後的向量
v = np.array([x1-x2, y1-y2])
v2 = np.dot(rot, v)

x3 = [int(x2+v2[0]), int(y2+v2[1])]
if x3[1]>4000:
    x3[1]=4000
    
# 畫紅線
cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 5)
cv2.line(img, x3, (x2, y2), (0, 0, 255), 5)
cv2.line(img, (x1, y1), (x1,x3[1]), (0, 0, 255), 5)

                       
# 加ROI遮罩
mask = np.zeros((4000,4000),dtype=np.uint8)
x_data = np.array([x1,x2,x1])
y_data = np.array([y1,y2,x3[1]-170])
pts=np.vstack((x_data,y_data)).astype(np.int32).T
cv2.fillPoly(mask,[pts],(255),8,0)
img=cv2.bitwise_and(img,img,mask=mask)


cv2.namedWindow('image2', cv2.WINDOW_KEEPRATIO)
cv2.imshow('image2',img)
cv2.setMouseCallback('image2', show_xy)

# img[y左右,x上下]
#img = img[y1-100:x3[1],x1-200:x2]

# 取得圖像的高度和寬度
(h, w) = img.shape[:2]
# 計算圖像的中心點
center = (h// 2, w// 2)
# 取得旋轉矩陣
M = cv2.getRotationMatrix2D(center, 91, 1.0)
cos=np.abs(M[0,0])
sin=np.abs(M[0,1])
nw = int((h*sin)+(w*cos))
nh = int((h*cos)+(w*sin))
# 旋轉圖像
output = cv2.warpAffine(img, M, (nw, nh))

#output = output[200:nh,350:nw]
#output = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE) 

cv2.namedWindow('image', cv2.WINDOW_KEEPRATIO)
cv2.imshow('image',output)
# pic='img_2'
# cv2.imwrite('picture\\' + pic + '_roi.png', output)

cv2.waitKey(0)
cv2.destroyAllWindows()

