import cv2
import numpy as np

from function.helper_function import read_image_list


def transformation_image(pic_path: str, output_path: str, flip_vertical=False) -> np.ndarray:
    # Define the transformation location of the image
    #[x左右,y上下]
    a_1 = 150   # 影響左側的上下
    a_2 = 220   # 影響左側的左右
    a_3 = 3850  # 影響右側的左右
    p1 = np.float32([[a_2, a_1], [a_2, 3000 - a_1], [a_3, 0], [a_3, 3000]])
    
    b_1 = 0
    b_2 = 15 #影響右側的上下
    b_3 = 3900
    p2 = np.float32([[b_1, 0], [b_1, 3300], [b_3, b_2], [4000, 3000 - b_2]])


    # Get the transformation matrix from p1 to p2
    m = cv2.getPerspectiveTransform(p1, p2)
    for pic in read_image_list(pic_path)[:6]:
        img = cv2.imread(pic_path + pic + '.png')
        if flip_vertical:
            img = cv2.flip(img, 0)
        output = cv2.warpPerspective(img, m, (4000, 4000))
        cv2.imwrite(f'{output_path}{pic}.png', output)
    return output
