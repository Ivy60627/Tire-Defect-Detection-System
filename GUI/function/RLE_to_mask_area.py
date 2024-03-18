import os
import numpy as np
import pycocotools.mask as mask_util
import json


class RLEtoMaskArea():
    def __init__(self):
        self.json_file_path = "images/outputs/preds/"
        self.json_out_file_path = "images/outputs/areas/"
        self.newdict = {}
        self.json_list = []
        self.maskarea = []

    def read_json(self):
        for root, dirs, files in os.walk(self.json_file_path):
            for file in files:
                self.json_list.append(file)
        return self.json_list

    def add_masks(self, labels, mask):

        def find_indices(labels: list, value: int) -> list:
            """
            Get the index list of the specific elements
            :labels: The label list
            :value: The element that will get the indexes in labels list
            :Return: return the list of indexes
    
            example:
            labels = [1, 2, 2, 3, 2, 3]
            value = 2
            return: [1, 2, 4]
    
            """

            return [index for index, element in enumerate(labels) if element == value]

        label_element_index_list = [find_indices(labels, x) for x in set(labels)]

        new_mask = []
        for index in label_element_index_list:
            element_masks_sum = sum([mask[x] for x in index])
            new_mask.append(element_masks_sum)

        return list(set(labels)), new_mask

    def RLE_to_maskarea(self, json_list):
        for json_file in json_list:
            f = open(self.json_file_path + json_file)
            data = json.load(f)

            # check the masks is exists
            if "masks" not in data:
                print(f"The file {json_file} doesn't have masks.")
                continue

            for i, _ in enumerate(data["labels"]):
                mask_decode = mask_util.decode(data["masks"][i])
                self.maskarea.append(np.count_nonzero(mask_decode))

            self.newdict["labels"], self.newdict["maskarea"] = self.add_masks(
                data["labels"], self.maskarea)

            tf = open(self.json_out_file_path + json_file, "w")
            json.dump(self.newdict, tf)
            tf.close()
            print(f"Convert {json_file} successfully.")
            self.maskarea = []
