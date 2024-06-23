import os, shutil

paths = ['images/roi', 'images/roi/left', 'images/roi/right',
         'images/transformation', 'images/transformation/left', 'images/transformation/right',
         'images/outputs', 'images/outputs/areas', 'reports']


def remove_folder():
    folder_path = ['images/roi', 'images/transformation', 'images/outputs']
    try:
        for path in folder_path:
            shutil.rmtree(path)
            print('Folder and its content removed')
    except:
        print('Folder not deleted')


def create_folder():
    for path in paths:
        if not os.path.isdir(path):
            os.makedirs(path)
