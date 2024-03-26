import cv2
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import QApplication

from UI import Ui_MainWindow
from function.RLE_to_mask_area import RLEtoMaskArea
from function.get_label_name import GetLabelName
from function.get_roi import GetROI
from function.perspective_transformation import PerspectiveTransformation
from function.picture_connect import PictureConnect
from function.show_defect import ShowDefect
from function.get_defect_rate import GetDefectRate
from function.get_result_csv import GetResultCSV



picture_path = './images/picture/'
perspective_path = './images/transformation/'
roi_path = './images/roi/'
area_file_path = "./images/outputs/areas/"
predict_script = ("python network/image_demo.py images/roi network/config.py "
                  "--weights network/model.pth --out-dir images/outputs/")


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    System pipeline:
    ReadPartImage - display_left_img - display_all_img -
    RLE_to_mask_area - get_defect_rate - display_defect_location
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ReadPartImage = ReadPartImage()
        self.ShowDefectLocation = ShowDefectLocation()
        self.GetLabelName = GetLabelName()
        # initial UI structure
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.process_running = False
        self.translate_to_zh_tw = False
        self.trans = QTranslator()
        self.setup_control()

        # Debug option, remember to remove this
        # self.ui.pushButton_translate.click()

    def setup_control(self):  # 啟動時預載入函式，連結顯示用訊號
        self.ReadPartImage.ReadPartImageFinished.connect(self.display_left_img)
        self.ReadPartImage.ReadAllImageFinished.connect(self.display_all_img)
        self.ShowDefectLocation.ConvertMaskAreaFinished.connect(self.display_defect_location)

        # connect buttons and actions when clicked
        self.ui.pushButton_reading_images.clicked.connect(self.button_reading_images)
        self.ui.pushButton_export_result.clicked.connect(self.button_export_clicked)
        self.ui.actionChinese.triggered.connect(self.load_language_zh)
        self.ui.actionEnglish.triggered.connect(self.load_language_en)



    def load_language_zh(self):
        # 讀取語言檔案後、獲取窗口實例、將翻譯安裝到實例中後翻譯界面
        self.translate_to_zh_tw = True
        self.trans.load("zh_TW")
        QtWidgets.QApplication.instance().installTranslator(self.trans)
        self.retranslateUi(self)

    def load_language_en(self):
        # 讀取語言檔案後、獲取窗口實例、將翻譯安裝到實例中後翻譯界面
        self.translate_to_zh_tw = False
        QtWidgets.QApplication.instance().removeTranslator(self.trans)
        self.retranslateUi(self)

    def display_left_img(self):
        label_left = GetLabelName.label_left
        for index, pic in enumerate(self.ReadPartImage.pic_list):
            img_path = str(roi_path + pic) + '.png'
            img = cv2.imread(img_path)
            img = cv2.resize(img, (115, 115))
            height, width, channel = img.shape
            qimg = QImage(img, width, height, 3 * width, QImage.Format_RGB888).rgbSwapped()
            exec(f'self.ui.{label_left[index]}.setPixmap(QPixmap.fromImage(qimg))')

    def display_all_img(self):
        img_path = 'connect_output.png'
        img = cv2.imread(img_path)
        img = cv2.resize(img, (450, 450))
        height, width, channel = img.shape
        qimg = QImage(img, width, height, 3 * width, QImage.Format_RGB888).rgbSwapped()
        self.ui.label_tire_all.setPixmap(QPixmap.fromImage(qimg))
        self.ShowDefectLocation.start()

    def display_defect_location(self):
        defect_location = GetLabelName.label_defect_location
        defect_check = GetLabelName.label_defect_check
        defect_rate = GetLabelName.label_defect_rate
        json_defect_str = ''

        for defect, element in enumerate(self.ShowDefectLocation.json_defect_location):
            if self.ShowDefectLocation.json_defect_location[defect]:
                if self.translate_to_zh_tw:
                    direction = GetLabelName.label_defect_direction_zh
                else:
                    direction = GetLabelName.label_defect_direction_en
                location = self.ShowDefectLocation.json_defect_location
                json_defect_str = ', '.join(direction[direct - 1] for direct in location[defect])




                exec(f'self.ui.{defect_check[element]}.setText("Yes")')
                exec(f'self.ui.{defect_location[element]}.setText(json_defect_str)')
                exec(f'self.ui.{defect_rate[element]}.setText(str(self.ShowDefectLocation.defect_rate[element])+ "%")')
            else:
                exec(f'self.ui.{defect_check[element]}.setText("No")')
                pass
        self.close_threads()

    def button_reading_images(self):
        if not self.process_running:
            self.process_running = True
            print("The process is starting!")
            self.ReadPartImage.start()
        else:
            print("This process is still running!")

    def button_export_clicked(self):
        try:
            GetResultCSV(self.ShowDefectLocation.json_defect_location,
                         self.ShowDefectLocation.defect_rate,
                         self.translate_to_zh_tw)
        except Exception as e:
            print("Can't Export the file now, try again later.")

    def close_threads(self):
        self.ReadPartImage.exit()
        self.ShowDefectLocation.exit()
        self.process_running = False
        print("Process Finished!")


class ReadPartImage(QtCore.QThread):  # 繼承 QtCore.QThread 來建立
    """
    Doing perspective transformation, getting ROI and store them in the select folder.
    Collect the ROI images and connect them on the image and save.
    """
    ReadPartImageFinished = QtCore.pyqtSignal()  # 建立讀取完畢的信號
    ReadAllImageFinished = QtCore.pyqtSignal()
    perspective_pic_list = []

    def __init__(self, parent=None):
        super().__init__()
        self.perspectiveTransformation = PerspectiveTransformation(picture_path)
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
    """
    Convert predict label and calculate masks to their areas.
    Store location data and rate and wait to send them to display_defect_location function.
    """
    ConvertMaskAreaFinished = QtCore.pyqtSignal()  # 建立傳遞信號，傳遞型態為任意格式

    def __init__(self, parent=None):
        super().__init__()
        self.convertRLEToMaskArea = RLEtoMaskArea()
        self.json_list = self.convertRLEToMaskArea.read_json()
        self.ShowDefect = ShowDefect()
        self.GetDefectRate = GetDefectRate()

    def run(self):
        self.convertRLEToMaskArea.RLE_to_maskarea(self.json_list)
        self.json_defect_location = self.ShowDefect.show_defect(self.ShowDefect.read_json())
        self.defect_rate = self.GetDefectRate.get_defect_rate(self.GetDefectRate.read_json())
        print(self.json_defect_location)
        self.ConvertMaskAreaFinished.emit()
