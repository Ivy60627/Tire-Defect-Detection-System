import os
import json
import cv2
from function.helper_function import read_image_list, read_json_list


def get_pixel_num(pic_path):
    """
    :return: the pixels of the colored areas
    """
    pic_list = read_image_list(pic_path)
    img = cv2.imread(pic_path + pic_list[0] + ".png")
    front_pixel_num = len(img[img != 0]) / 3
    return front_pixel_num


def get_defect_rate(json_path: str, pic_path: str) -> dict:
    """
    :param json_list:
    :param pic_path: the roi picture path
    :param json_path: the defect json file path
    :return: each defect rate in the wheel
    """
    defect = {}
    defect_rate = {}
    front = get_pixel_num(pic_path)

    for num in range(7):
        defect[num] = 0
        defect_rate[num] = 0.0

    for json_file in read_json_list(json_path):
        data = json.load(open(json_path + json_file))

        # check the masks exists
        if "maskarea" not in data:
            print(f"The file {json_file} doesn't have mask area.")
            continue
        # add the areas from all jsons
        label = list(set(data["labels"]))
        for defect_num in label:
            defect[defect_num] += int(data["maskarea"][label.index(defect_num)])

    # calculate defect %
    for defect_num in range(7):
        defect_rate[defect_num] = round(float(defect[defect_num] * 100 / front), 2)
    print("Finished get defect rate.")
    return defect_rate
