import os
import cv2
import numpy as np

def show_xy(event,x,y,flags,userdata):
    if (event != 0):
        print(event, x, y, flags)


class PerspectiveTransformation():    
    def __init__(self):  
        # Set the path of the pictures
        self.path = './picture/'
        self.pic_list = []          
        
        # Define the transformation location of the image      
        self.x_1 = 220 
        self.p1 = np.float32([[self.x_1,0], [4000 - self.x_1 ,0], [0,2536], [4000,2536]])
        self.x_2 = 580
        self.p2 = np.float32([[50,0], [3950,0], [self.x_2,3600], [4000 - self.x_2 ,3600]])
        
        # Get the tranformation matrix from p1 to p2
        self.m = cv2.getPerspectiveTransform(self.p1, self.p2)
        
    
    def read_image(self):
        for root,dirs,files in os.walk(self.path):
        	for file in files:
        		file=file.rstrip(".png")
        		self.pic_list.append(file)                
        return self.pic_list
    
    def transformation_image(self, pic_list):
        for pic in self.pic_list:
            self.img = cv2.imread(self.path +  pic + '.png',)               
            self.output = cv2.warpPerspective(self.img, self.m, (4000, 4000))            
            self.img_original = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            cv2.imwrite('transformation\\' + pic + '.png', self.output)       
        return self.output

