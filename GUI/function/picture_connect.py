import os
import cv2
import numpy as np
import time
from PIL import Image




def show_xy(event,x,y,flags,userdata):
    if (event != 0):       
        print(event,x,y,flags)
 
class PictureConnect():    
    def __init__(self):
        self.IMAGE_SIZE = 6000
        # 讀取圖片路徑
        self.path = './roi/'
        self.pic_list = []
        self.output_Image= []
    
    
    def read_image(self):
        for root,dirs,files in os.walk(self.path):
        	for file in files:
        		file=file.rstrip(".png")
        		self.pic_list.append(file)
        print("Finish reading " + str(len(self.pic_list)) + " pictures!")
        self.pic_list = self.pic_list[:6] # 取前六                
        return self.pic_list
    
    def blackToClear(self, img):   # 把黑色底調整成透明
        mask = np.all(img[:,:,:] == [0, 0, 0], axis=-1)
        dst = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        dst[mask, 3] = 0
        return dst

    
    def resize_image(self, image):

        top, bottom, left, right = (0, 0, 0, 0)      
        h, w, _ = image.shape
        # 在上方加上黑色邊
        if h < self.IMAGE_SIZE:
            dh = self.IMAGE_SIZE - h
            top = dh
            bottom = 0
        if w < self.IMAGE_SIZE:
            dw = self.IMAGE_SIZE - w
            left = dw // 2
            right = dw - left     
        BLACK = [0, 0, 0] # RGB颜色
        # 加圖片邊界，cv2.BORDER_CONSTANT指定顏色
        constant = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK)     
        mask_1 = np.all(constant[:,:,:] == [0, 0, 0], axis=-1)
        dst = cv2.cvtColor(constant, cv2.COLOR_BGR2RGBA)
        dst[mask_1,3] = 0
        return cv2.resize(dst, (self.IMAGE_SIZE, self.IMAGE_SIZE)) # 調整圖片大小
    
    def connect_picture(self, pic_list):   
        for index, pic in enumerate(pic_list):
            start = time.time()
            img = cv2.imread(str(self.path + pic) + '.png')        
            
                        
            # 轉換成 BGRA 色彩模式         
            #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA) 
            # 新增 gray 變數為轉換成灰階的圖片       
            #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 去除黑底
            img = self.blackToClear(img)  
            
            # 調整圖片大小並加上透明邊
            img = self.resize_image(img)
            # 取得圖像的高度和寬度
            (h, w) = img.shape[:2]
            # 計算圖像的中心點
            center = (3452, 3010)
            # 取得旋轉矩陣
            M = cv2.getRotationMatrix2D(center, index*60, 1.0)
            cos=np.abs(M[0,0])
            sin=np.abs(M[0,1])
            nw = int((h*sin)+(w*cos)) #往右移，需要更大空間
            nh = int((h*cos)+(w*sin))
            # 旋轉圖像
            output = cv2.warpAffine(img, M, (nw, nh))
            self.output_Image.append(Image.fromarray(np.uint8(output)))
            end = time.time()
            print("Finish rotate " + str(index + 1) + " picture(s), used " + str(end - start) +" seconds.")
            
        # 新開一張全白的畫布
        bg = Image.new('RGBA',(8000, 8000), '#FFFFFF')
        # 將圖片拼貼到底板上
        for i, _ in enumerate(self.output_Image):
            r,g,b,a = self.output_Image[i].split() 
            bg.paste(self.output_Image[i],(500, 500),mask=a)   
        
        #轉換為cv2格式
        bg = cv2.cvtColor(np.asarray(bg), cv2.COLOR_RGBA2BGRA)
        # 顯示 + 儲存    
        cv2.imwrite('connect_output.png', bg)
        return bg