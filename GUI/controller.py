import cv2
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap

from UI import Ui_MainWindow
from function.RLE_to_maskarea import RLEtoMaskArea
from function.get_label_name import GetLabelName
from function.get_roi import GetROI
from function.perspective_transformation import PerspectiveTransformation
from function.picture_connect import PictureConnect
from function.show_defect import ShowDefect

picture_path = './picture/'
perspective_path = './transformation/'
roi_path = './roi/'
area_file_path = "./outputs/areas/"
predict_script = "python network/image_demo.py transformation network/config.py --weights network/model.pth"


class MainWindow(QtWidgets.QMainWindow):
    """
    ReadPartImage - display_left_img - display_all_img -
    RLE_to_maskarea - display_defect_location
    """

    def __init__(self):
        # in python3, super(Class, self).xxx = super().xxx
        super(MainWindow, self).__init__()
        self.GetLabelName = GetLabelName()
        self.ReadPartImage = ReadPartImage()
        self.ShowDefectLocation = ShowDefectLocation()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):  # 啟動時預載入函式，連結顯示用訊號
        self.ReadPartImage.ReadPartImageFinished.connect(self.display_left_img)
        self.ReadPartImage.ReadAllImageFinished.connect(self.display_all_img)
        self.ShowDefectLocation.ConvertMaskAreaFinished.connect(self.display_defect_location)
        self.ReadPartImage.start()

    def display_left_img(self):
        label_left = GetLabelName.label_left
        for index, pic in enumerate(self.ReadPartImage.pic_list):
            img_path = str(roi_path + pic) + '.png'
            img = cv2.imread(img_path)
            img = cv2.resize(img, (115, 115))
            height, width, channel = img.shape
            self.qimg = QImage(img, width, height, 3 * width, QImage.Format_RGB888).rgbSwapped()
            exec(f'self.ui.{label_left[index]}.setPixmap(QPixmap.fromImage(self.qimg))')

    def display_all_img(self):
        img_path = 'connect_output.png'
        img = cv2.imread(img_path)
        img = cv2.resize(img, (450, 450))
        height, width, channel = img.shape
        self.qimg = QImage(img, width, height, 3 * width, QImage.Format_RGB888).rgbSwapped()
        self.ui.label_tire_all.setPixmap(QPixmap.fromImage(self.qimg))
        self.ShowDefectLocation.start()

    def display_defect_location(self):
        defect_location = GetLabelName.label_defect_location
        defect_check = GetLabelName.label_defect_check

        for defect, element in enumerate(self.ShowDefectLocation.json_defect_location):
            if self.ShowDefectLocation.json_defect_location[defect]:
                json_defect_str = ', '.join(GetLabelName.label_defect_direction[direct]
                                            for direct, _ in enumerate(self.ShowDefectLocation.
                                                                       json_defect_location[defect]))
                exec(f'self.ui.{defect_check[element]}.setText("Yes")')
                exec(f'self.ui.{defect_location[element]}.setText(json_defect_str)')
            else:
                exec(f'self.ui.{defect_check[element]}.setText("No")')
                pass


class ReadPartImage(QtCore.QThread):  # 繼承 QtCore.QThread 來建立
    ReadPartImageFinished = QtCore.pyqtSignal()  # 建立讀取完畢的信號
    ReadAllImageFinished = QtCore.pyqtSignal()
    perspective_pic_list = []

    def __init__(self, parent=None):
        super().__init__()
        self.perspectiveTransformation = PerspectiveTransformation()
        self.getROI = GetROI()
        self.pic_list = self.perspectiveTransformation.read_image()
        self.pic_list = sorted(self.pic_list)
        self.pictureConnect = PictureConnect()

    def run(self):
        # 進行圖片透視校正與擷取ROI，預測圖片後進行圖片拼接
        self.perspectiveTransformation.transformation_image(self.pic_list)
        self.getROI.get_roi(self.pic_list)
        self.ReadPartImageFinished.emit()

        os.system(predict_script)  # 預測圖片
        self.pictureConnect.connect_picture(self.pic_list)
        self.ReadAllImageFinished.emit()


class ShowDefectLocation(QtCore.QThread):
    ConvertMaskAreaFinished = QtCore.pyqtSignal()  # 建立傳遞信號，傳遞型態為任意格式

    def __init__(self, parent=None):
        super().__init__()
        self.convertRLEToMaskArea = RLEtoMaskArea()
        self.json_list = self.convertRLEToMaskArea.read_json()
        self.ShowDefect = ShowDefect()

    def run(self):
        self.convertRLEToMaskArea.RLE_to_maskarea(self.json_list)
        self.json_defect_location = self.ShowDefect.show_defect(self.ShowDefect.read_json())
        self.ConvertMaskAreaFinished.emit()
