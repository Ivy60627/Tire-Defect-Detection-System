import os
import json


def get_key(dicts, value):
    return [k for k, v in dicts.items() if v in dicts.value()]


class ShowDefect:
    def __init__(self):
        self.json_defect_file_path = "images/outputs/areas/"

    def read_json(self):
        json_list = []
        for root, dirs, files in os.walk(self.json_defect_file_path):
            for file in files:
                json_list.append(file)
        return json_list

    def show_defect(self, json_list):
        """
        :param json_list: defect json
        :return: the json name numbers
        """
        defect = {}
        for num in range(7):
            defect[num] = []
        for json_file in json_list:
            f = open(self.json_defect_file_path + json_file)
            data = json.load(f)

            # check the masks exists
            if "maskarea" not in data:
                print(f"The file {json_file} doesn't have maskarea.")
                continue

            label = list(set(data["labels"]))
            for defect_num in label:
                defect[defect_num].append(int(json_file[6:7]))
        return defect
