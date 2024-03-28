import os


def read_image_list(path: str) -> list:
    pic_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file = file.rstrip(".png")
            pic_list.append(file)
    return pic_list


def read_json_list(path: str) -> list:
    json_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            json_list.append(file)
    return json_list[:6]
