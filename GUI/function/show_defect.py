import json

from function.helper_function import read_json_list


def get_key(dicts, value):
    return [k for k, v in dicts.items() if v in dicts.value()]


def show_defect(json_path: str) -> dict:
    """
    :param json_path: the defect json file path
    :param json_list: defect json list
    :return: the defect json name numbers, their location
    """
    defect = {}
    for num in range(7):
        defect[num] = []
    for json_file in read_json_list(json_path):
        f = open(json_path + json_file)
        data = json.load(f)

        # check the masks exists
        if "maskarea" not in data:
            print(f"The file {json_file} doesn't have mask area.")
            continue

        label = list(set(data["labels"]))
        for defect_num in label:
            # Only use the numbers in the file name "image_{number}.png
            defect[defect_num].append(int(json_file[6:7]))
    return defect
