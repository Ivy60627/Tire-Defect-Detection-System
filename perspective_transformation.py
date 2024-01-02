import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def show_xy(event,x,y,flags,userdata):
    if (event != 0):
        print(event,x,y,flags)

# [x,y]      
x_1 = 220 
p1 = np.float32([[x_1,0],[4000 - x_1 ,0], [0,2536], [4000,2536]])
x_2 = 580
p2 = np.float32([[50,0], [3950,0], [x_2,3600], [4000 - x_2 ,3600]])

# old
# p1 = np.float32([[400,200],[3600,200], [3,2536], [3997,2536]])
# p2 = np.float32([[100,0], [3900,0], [453,3650], [3557,3650]])
m = cv2.getPerspectiveTransform(p1, p2)

path = './picture/'
pic_list = []

for root,dirs,files in os.walk(path):
	for file in files:
		file=file.rstrip(".png")
		pic_list.append(file)
        
for pic in pic_list:
    img = cv2.imread(path +  pic + '.png',)    
    
    #cv2.namedWindow('image', cv2.WINDOW_KEEPRATIO)
    #cv2.imshow('image',img)
    #cv2.setMouseCallback('image', show_xy)  # 設定偵測事件的函式與視窗
    
    output = cv2.warpPerspective(img, m, (4000, 4000))
    
    img_original = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.subplot(1,2,1)
    plt.imshow(img_original)
    plt.xticks([]), plt.yticks([])
    plt.title('original image')

    img_gardien = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    plt.subplot(1,2,2)
    plt.imshow(img_gardien)
    plt.xticks([]), plt.yticks([])
    plt.title('output')
    
    #cv2.namedWindow('image2', cv2.WINDOW_KEEPRATIO)
    #cv2.imshow('image2', output)
    cv2.imwrite('transformation\\' + pic + '_t.png', output)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
