# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 17:21:31 2024

@author: GTX-960
"""
import os

def read_image(path):
    pic_list=[]
    for root,dirs,files in os.walk(path):
    	for file in files:
    		file=file.rstrip(".png")
    		pic_list.append(file)
    print("Finish reading " + str(len(pic_list)) + " pictures!")
    pic_list = pic_list[:6] # 取前六                
    return pic_list