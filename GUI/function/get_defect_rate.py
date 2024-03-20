import os
import json
import cv2

pic_path = './images/roi/'


def get_pixel_num():
    """
    :return: the pixels of the colored areas
    """
    json_list = []
    for root, dirs, files in os.walk(pic_path):
        for file in files:
            json_list.append(file)

    img = cv2.imread(pic_path + json_list[0])
    front_pixel_num = len(img[img != 0]) / 3
    return front_pixel_num


class GetDefectRate:
    def __init__(self):
        self.json_defect_file_path = "images/outputs/areas/"
        self.defect = {}
        self.defect_rate = {}
        self.json_list = []
        for num in range(7):
            self.defect[num] = 0
            self.defect_rate[num] = 0.0

    def read_json(self):
        self.json_list = []
        for root, dirs, files in os.walk(self.json_defect_file_path):
            for file in files:
                self.json_list.append(file)
        return self.json_list

    def get_defect_rate(self, json_list):
        """
        :param json_list: defect json
        :return: each defect rate in the wheel
        """
        for num in range(7):
            self.defect[num] = 0
            self.defect_rate[num] = 0.0

        for json_file in json_list:
            f = open(self.json_defect_file_path + json_file)
            data = json.load(f)
            front = get_pixel_num()

            # check the masks exists
            if "maskarea" not in data:
                print(f"The file {json_file} doesn't have mask area.")
                continue

            # add the areas from all jsons
            label = list(set(data["labels"]))
            for defect_num in label:
                self.defect[defect_num] += int(data["maskarea"][label.index(defect_num)])

        # calculate defect %
        for defect_num in range(7):
            self.defect_rate[defect_num] = round(float(self.defect[defect_num] * 100 / front), 2)
        print("Finished get defect rate.")
        return self.defect_rate
