# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 21:03:26 2024

@author: iamiv
"""
import os, cv2
import matplotlib.pyplot as plt

def read_image_list(path: str) -> list:
    pic_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            pic_list.append(file.rstrip(".jpg"))
    return pic_list

#path = 'images_sort/image_4_png_jpg.rf.0ee0a6c9078a59d3d551fee2cc645210/'
path = 'images_sort/image_28_png.rf.ae27fa0c300bcf7a2776cfdc8da90491/'
#path = 'images_sort/image_12_png_jpg.rf.a7221fc10f9af9ca9aab6947c0984001/'
pic_list = read_image_list(path)

pic_list.pop(5)

img = cv2.imread(path + 'Original Image.jpg')
img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.rcParams["figure.figsize"] = (32, 24)

# modify the crop image range
# o1 = 0
# o2 = 1536
# p1 = 0
# p2 = 2048

o1 = 600
o2 = o1 + 240
p1 = 600
p2 = p1 + 320

plt.subplot(3, 3, 1)
crop_img = img_RGB[o1:o2,p1:p2]
plt.imshow(crop_img)
plt.xticks([]), plt.yticks([])
plt.title('Original Image',fontsize=30)

img = cv2.imread(path + 'Improved Mask R-CNN.jpg')
img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.subplot(3, 3, 2)
crop_img = img_RGB[o1:o2,p1:p2]
plt.imshow(crop_img)
plt.xticks([]), plt.yticks([])
plt.title('Ground Truth',fontsize=30)


for num, pic in enumerate(pic_list):
    img = cv2.imread(path +  pic + '.jpg')
    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    crop_img = img_RGB[o1:o2,2049+p1:2048+p2]
    plt.subplot(3, 3, num + 3)
    plt.imshow(crop_img)
    plt.xticks([]), plt.yticks([])
    
    plt.title(pic,fontsize=30)



