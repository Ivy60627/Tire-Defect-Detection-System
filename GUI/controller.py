import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap

from UI import Ui_MainWindow
from function.perspective_transformation import PerspectiveTransformation
from function.get_roi import GetROI
from function.picture_connect import PictureConnect
from function.RLE_to_maskarea import RLEtoMaskArea

picture_path = './picture/'
perpsective_path = './transformation/'
roi_path = './roi/'


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # in python3, super(Class, self).xxx = super().xxx
        super(MainWindow, self).__init__()
        self.ShowDefectLocation = ShowDefectLocation()
        self.ReadPartImage = ReadPartImage()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):  # 啟動時預載入函式
        # 連結訊號到顯示左側圖片
        self.ReadPartImage.ReadPartImageFinished.connect(self.display_left_img)
        # 連結訊號到顯示全域圖片
        self.ReadPartImage.ReadAllImageFinished.connect(self.display_all_img)
        # 連結訊號到顯示瑕疵位置
        self.ShowDefectLocation.ConvertMaskAreaFinished.connect(self.display_defect_location)

        self.ReadPartImage.start()
        self.ShowDefectLocation.start()

    def display_left_img(self):
        label_left = ['label_camera_left1', 'label_camera_left2', 'label_camera_left3',
                      'label_camera_left4', ' label_camera_left5', 'label_camera_left6']
        # print(self.ReadPartImage.pic_list)

        for index, pic in enumerate(self.ReadPartImage.pic_list):
            img_path = str(roi_path + pic) + '.png'
            self.img = cv2.imread(img_path)
            self.img = cv2.resize(self.img, (115, 115))
            height, width, channel = self.img.shape
            self.qimg = QImage(self.img, width, height, 3 * width, QImage.Format_RGB888).rgbSwapped()
            exec(f'self.ui.{label_left[index]}.setPixmap(QPixmap.fromImage(self.qimg))')

    def display_all_img(self):
        img_path = 'connect_output.png'
        self.img = cv2.imread(img_path)
        self.img = cv2.resize(self.img, (450, 450))
        height, width, channel = self.img.shape
        self.qimg = QImage(self.img, width, height, 3 * width, QImage.Format_RGB888).rgbSwapped()
        self.ui.label_tire_all.setPixmap(QPixmap.fromImage(self.qimg))

    def display_defect_location(self):
        # TODO
        pass


class ReadPartImage(QtCore.QThread):  # 繼承 QtCore.QThread 來建立 
    ReadPartImageFinished = QtCore.pyqtSignal()  # 建立傳遞信號，設定傳遞型態為任意格式
    ReadAllImageFinished = QtCore.pyqtSignal()  # 建立傳遞信號，設定傳遞型態為任意格式

    perspective_pic_list = []

    def __init__(self, parent=None):
        super().__init__()
        self.perspectiveTransformation = PerspectiveTransformation()
        self.getROI = GetROI()
        self.pic_list = self.perspectiveTransformation.read_image()
        self.pic_list = sorted(self.pic_list)
        self.pictureConnect = PictureConnect()

    def run(self):
        # 進行圖片透視校正
        self.perspectiveTransformation.transformation_image(self.pic_list)
        # ROI
        self.getROI.get_roi(self.pic_list)
        # 完成後發送完成訊號
        self.ReadPartImageFinished.emit()
        # 圖片連結
        self.pictureConnect.connect_picture(self.pic_list)
        # 完成後發送完成訊號
        self.ReadAllImageFinished.emit()


class ShowDefectLocation(QtCore.QThread):
    # 建立傳遞信號，設定傳遞型態為任意格式
    ConvertMaskAreaFinished = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.convertRLEToMaskArea = RLEtoMaskArea()
        self.json_list = self.convertRLEToMaskArea.read_json()

    def run(self):
        self.convertRLEToMaskArea.RLE_to_maskarea(self.json_list)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
