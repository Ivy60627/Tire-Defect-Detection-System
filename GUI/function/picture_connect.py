import os
import cv2
import numpy as np
import time
from PIL import Image

from function.helper_function import read_image_list


def show_xy(event, x, y, flags, userdata):
    if event != 0:
        print(event, x, y, flags)


def blackToClear(img):  # 把黑色底調整成透明
    mask = np.all(img[:, :, :] == [0, 0, 0], axis=-1)
    dst = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    dst[mask, 3] = 0
    return dst


def resize_image(image, image_size):
    top, bottom, left, right = (0, 0, 0, 0)
    h, w, _ = image.shape
    # 在上方加上黑色邊
    if h < image_size:
        dh = image_size - h
        top = dh
        bottom = 0
    if w < image_size:
        dw = image_size - w
        left = dw // 2
        right = dw - left

    color = [0, 0, 0]  # RGB颜色
    # 加圖片邊界，cv2.BORDER_CONSTANT指定顏色
    constant = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    mask_1 = np.all(constant[:, :, :] == [0, 0, 0], axis=-1)
    dst = cv2.cvtColor(constant, cv2.COLOR_BGR2BGRA)
    dst[mask_1, 3] = 0
    return cv2.resize(dst, (image_size, image_size))  # 調整圖片大小


def connect_picture(pic_path: str):
    image_size = 7000
    output_Image = []
    start = time.time()
    for index, pic in enumerate(read_image_list(pic_path)):
        img = cv2.imread(str(pic_path + pic) + '.png')

        # 去除黑底後，調整圖片大小並加上透明邊
        img = blackToClear(img)
        img = resize_image(img, image_size)
        # 取得圖像的高度和寬度
        (h, w) = img.shape[:2]
        # 計算圖像的中心點
        center = (3550, 3855)
        # 取得旋轉矩陣
        matrix = cv2.getRotationMatrix2D(center, index * 60, 1.0)
        cos = np.abs(matrix[0, 0])
        sin = np.abs(matrix[0, 1])
        nw = int((h * sin) + (w * cos))  # 往右移，需要更大空間
        nh = int((h * cos) + (w * sin))
        # 旋轉圖像
        output = cv2.warpAffine(img, matrix, (nw, nh))
        output_Image.append(Image.fromarray(np.uint8(output)))

    end = time.time()
    print(f"Finish rotating pictures, used{(end - start): .2f} seconds.")

    # 新開一張全白的畫布
    bg = Image.new('RGBA', (8000, 8000), '#FFFFFF')
    # 將圖片拼貼到底板上
    for i, _ in enumerate(output_Image):
        r, g, b, a = output_Image[i].split()
        bg.paste(output_Image[i], (500, 800), mask=a)

    # 轉換為cv2格式
    bg = cv2.cvtColor(np.asarray(bg), cv2.COLOR_RGBA2BGRA)
    # 裁切圖片 [上下, 左右]
    bg = bg[1450:7800, 550:7700]
    cv2.imwrite('connect_output.png', bg)
    return bg
