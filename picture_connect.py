import os
import cv2
import numpy as np
from PIL import Image

def show_xy(event,x,y,flags,userdata):
    if (event != 0):       
        print(event,x,y,flags)
  
def blackToClear(img):   # 把黑色底調整成透明
    h, w = img.shape[:2] # 取得圖片高度&寬度 
    for x in range(w):   # 依序取出圖片中每個像素
        for y in range(h):
            if gray[y, x] < 5:  # 如果該像素的灰階度小於 5，調整成透明
                img[y, x, 3] = 0
    return img

IMAGE_SIZE = 5000

def resize_image(image, height=IMAGE_SIZE, width=IMAGE_SIZE):
     top, bottom, left, right = (0, 0, 0, 0)      
     h, w, _ = image.shape  # 获取图像尺寸 
     # 在上方加上黑色邊
     if h < IMAGE_SIZE:
         dh = IMAGE_SIZE - h
         top = dh
         bottom = 0
     if w < IMAGE_SIZE:
         dw = IMAGE_SIZE - w
         left = dw // 2
         right = dw - left     
     BLACK = [0, 0, 0] # RGB颜色
     # 给图像增加边界，是图片长、宽等长，cv2.BORDER_CONSTANT指定边界颜色由value指定
     constant = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK)
     # 调整图像大小并返回     
     return cv2.resize(constant, (height, width))

path = './roi/'
pic_list = []
output_Image= []
for root,dirs,files in os.walk(path):
	for file in files:
		file=file.rstrip(".png")
		pic_list.append(file)

pic_list = pic_list[:6]

for index, img in enumerate(pic_list):        
    img = cv2.imread('picture\\img_2_roi.png') 
    #img2 = cv2.imread('picture\\img_2_roi.png')
    
    img = resize_image(img)
    #img2 = resize_image(img2)
         
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)  # 轉換成 BGRA 色彩模式
    #img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGBA)  # 轉換成 BGRA 色彩模式  
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 新增 gray 變數為轉換成灰階的圖片
    
    
    
    img = blackToClear(img)
    #img2 = blackToClear(img2)
    
    # cv2.namedWindow('image22', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('image22',img2)
    # cv2.setMouseCallback('image22', show_xy)
    bg = Image.new('RGBA',(8000, 8000), '#FFFFFF')
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    
    # # 1 
    # output_Image = Image.fromarray(np.uint8(img))
    # r,g,b,a = output_Image.split()
    # bg.paste(output_Image,(1500, 1500),mask=a)
     
    
    # 2取得圖像的高度和寬度
    (h, w) = img.shape[:2]
    # 計算圖像的中心點
    # center = (1966, 54)
    center = (2969,2429)
    # 取得旋轉矩陣
    M = cv2.getRotationMatrix2D(center, index*60, 1.0)
    cos=np.abs(M[0,0])
    sin=np.abs(M[0,1])
    nw = int((h*sin)+(w*cos)) #往右移，需要更大空間
    nh = int((h*cos)+(w*sin))
    
     
    # 旋轉圖像
    output = cv2.warpAffine(img, M, (nw, nh))
    output_Image.append(Image.fromarray(np.uint8(output)))

for i in range(6):    
    r,g,b,a = output_Image[i].split() 
    bg.paste(output_Image[i],(1500, 1500),mask=a)   

    # 3 取得旋轉矩陣
    # M = cv2.getRotationMatrix2D(center, -60, 1.0)
    # cos=np.abs(M[0,0])
    # sin=np.abs(M[0,1])
    # nw = int((h*sin)+(w*cos))
    # nh = int((h*cos)+(w*sin))

# output2 = cv2.warpAffine(img2, M, (6000, 6000))
# output_Image2 = Image.fromarray(np.uint8(output2))
# r,g,b,a = output_Image2.split()
# bg.paste(output_Image2,(1500, 1500),mask=a)

#轉換為cv2格式
bg = cv2.cvtColor(np.asarray(bg), cv2.COLOR_RGBA2BGRA)
cv2.namedWindow('image', cv2.WINDOW_KEEPRATIO)
cv2.imshow('image',bg)            
# cv2.imwrite('connect_output.png', bg)    # 存檔儲存為 png，不可用imshow
cv2.waitKey(0)
cv2.destroyAllWindows()