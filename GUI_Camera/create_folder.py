import os
import shutil

paths = ['../GUI/images/picture', '../GUI/images/picture/left', '../GUI/images/picture/right']


def remove_folder():
    try:
        for path in paths:
            shutil.rmtree(path)
            print('Folder and its content removed')
    except:
        print('Folder not deleted')


def create_folder():
    for path in paths:
        if not os.path.isdir(path):
            os.makedirs(path)
