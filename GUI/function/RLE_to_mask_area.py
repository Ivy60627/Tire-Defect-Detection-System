import os
import numpy as np
import pycocotools.mask as mask_util
import json

from function.helper_function import read_json_list


def add_masks(label_list, mask):
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

    label_element_index_list = [find_indices(label_list, x) for x in set(label_list)]

    new_mask = []
    for index in label_element_index_list:
        element_masks_sum = sum([mask[x] for x in index])
        new_mask.append(element_masks_sum)

    return list(set(label_list)), new_mask


def RLE_to_mask_area(json_path: str, output_path: str):
    for json_file in read_json_list(json_path):
        new_dict = {}
        mask_area = []
        data = json.load(open(json_path + json_file))

        # check the masks is existing
        if "masks" not in data:
            print(f"The file {json_file} doesn't have masks.")
            continue

        for i, _ in enumerate(data["labels"]):
            mask_decode = mask_util.decode(data["masks"][i])
            mask_area.append(np.count_nonzero(mask_decode))

        new_dict["labels"], new_dict["maskarea"] = add_masks(
            data["labels"], mask_area)

        tf = open(output_path + json_file, "w")
        json.dump(new_dict, tf)
        tf.close()
        print(f"Convert {json_file} successfully.")
