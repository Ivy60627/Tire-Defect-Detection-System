# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 20:46:49 2024

@author: iamiv

抓取每個資料夾下的同名文件並整理在一起
"""

import os
import shutil

father_path = r"C:\Users\iamiv\CODE\Tire-Defect-Detection-System\show_image\images"


def mkdir(dir):
    """如資料夾不存在 創立新資料夾"""
    if not os.path.exists(dir):
        os.makedirs(dir)

sub_dirs,file_names = None, None

for root,dirs,files in os.walk(father_path):
    if not sub_dirs and dirs:
        sub_dirs = dirs
    if not file_names and files:
        file_names = files
        break
print(sub_dirs)
print(file_names)

target_father_path = os.path.join(father_path,"..") + "/images_sort/"  

for pic_name in file_names:
    print("Moving",pic_name)
    # 準備當前圖片的目標資料夾
    target_dir_name = os.path.splitext(pic_name)[0]
    target_dir = target_father_path + target_dir_name
    mkdir(target_dir)
    
    #移動
    for dir in sub_dirs:
        file_path = os.path.join(father_path, dir, pic_name)
        new_pic_name = dir + os.path.splitext(pic_name)[1]
        target_file_path = os.path.join(target_father_path, target_dir, new_pic_name)
        
        shutil.copyfile(file_path, target_file_path)


