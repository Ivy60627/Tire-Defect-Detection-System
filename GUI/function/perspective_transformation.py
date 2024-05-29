import cv2
import numpy as np

from function.helper_function import read_image_list


def transformation_image(pic_path: str, output_path: str, flip_vertical=False) -> np.ndarray:
    # Define the transformation location of the image
    x_1 = 250
    p1 = np.float32([[500, x_1], [500, 3000 - x_1], [3550, 0], [3550, 3000]])
    x_2 = 15
    p2 = np.float32([[0, 0], [0, 3000], [4000, x_2], [4000, 3000 - x_2]])

    # Get the transformation matrix from p1 to p2
    m = cv2.getPerspectiveTransform(p1, p2)
    for pic in read_image_list(pic_path)[:6]:
        img = cv2.imread(pic_path + pic + '.png')
        if flip_vertical:
            img = cv2.flip(img, 0)
        output = cv2.warpPerspective(img, m, (4000, 4000))
        cv2.imwrite(f'{output_path}{pic}.png', output)
    return output
