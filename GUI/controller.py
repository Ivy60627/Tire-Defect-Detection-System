from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage, QPixmap

from UI import Ui_MainWindow
from function.perspective_transformation import PerspectiveTransformation
from function.get_roi import GetROI

import cv2



picture_path = './picture/'
perpsective_path = './transformation/'
roi_path = './roi/'


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # in python3, super(Class, self).xxx = super().xxx
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

    
    def setup_control(self): # 啟動時預載入函式
        self.ReadPartImage = ReadPartImage()
        self.ReadPartImage.ReadPartImageFinished.connect(self.display_left_img) # 連結訊號到顯示左側圖片
        self.ReadPartImage.start()
        
    def display_left_img(self):
        label_left = ['label_camera_left1','label_camera_left2','label_camera_left3',
                 'label_camera_left4','label_camera_left5','label_camera_left6']
        print(self.ReadPartImage.pic_list)
        for index, pic in enumerate(self.ReadPartImage.pic_list):            
            img_path = str(roi_path + pic) + '.png'
            self.img = cv2.imread(img_path)
            self.img = cv2.resize(self.img, (115, 115))
            height, width, channel = self.img.shape
            bytesPerline = 3 * width
            self.qimg = QImage(self.img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
            exec(f'self.ui.{label_left[index]}.setPixmap(QPixmap.fromImage(self.qimg))')

class ReadPartImage(QtCore.QThread):  # 繼承 QtCore.QThread 來建立 
    ReadPartImageFinished = QtCore.pyqtSignal()  # 建立傳遞信號，設定傳遞型態為任意格式
    perspective_pic_list=[]
    
    def __init__(self, parent=None):
        super().__init__()
        self.perspectiveTransformation = PerspectiveTransformation()
        self.getROI = GetROI()
        self.pic_list = self.perspectiveTransformation.read_image()


    def run(self):
        # 進行圖片透視校正
        self.perspectiveTransformation.transformation_image(self.pic_list)
        # TODO ROI
        self.getROI.get_roi(self.pic_list)
        # 完成後發送完成訊號
        self.ReadPartImageFinished.emit()
        

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
