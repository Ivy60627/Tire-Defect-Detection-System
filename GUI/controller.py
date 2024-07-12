import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTranslator

from UI import Ui_MainWindow
from function.RLE_to_mask_area import RLE_to_mask_area
from function.get_label_name import GetLabelName
from function.get_roi import get_roi
from function.perspective_transformation import transformation_image
from function.picture_connect import connect_picture
from function.show_defect import show_defect
from function.get_defect_rate import get_defect_rate
from function.get_result_csv import GetResultCSV
from function.helper_function import *
from function.create_folder import *

# All the paths the program used
picture_path = './images/picture/'
perspective_path = './images/transformation/'
roi_path = './images/roi/'
output_file_path = "./images/outputs"
predict_path = './images/outputs/vis/'

# The predict command
predict_script = ("python network/image_demo.py images/roi/left network/config.py "
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
        remove_folder()
        create_folder()
        self.trans = QTranslator()
        self.setup_control()

        # Debug option, remember to remove this
        # self.ui.pushButton_translate.click()

    def setup_control(self):  # 啟動時預載入函式，連結顯示用訊號
        self.ReadPartImage.ReadPartImageFinished.connect(self.display_area_img)
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

    def display_area_img(self):
        self.display_img("left")
        self.display_img("right")

    def display_img(self, direction: str):
        if direction == "left":
            label = GetLabelName.label_left
        else:
            label = GetLabelName.label_right
        for index, pic in enumerate(read_image_list(f"{picture_path}{direction}/")):
            img = cv2.imread(f"{roi_path}{direction}/{pic}.png")
            img = cv2.resize(img, (115, 115))
            height, width, channel = img.shape
            qimg = QImage(img, width, height, 3 * width, QImage.Format_RGB888).rgbSwapped()
            exec(f'self.ui.{label[index]}.setPixmap(QPixmap.fromImage(qimg))')

    def display_all_img(self):
        img_path = 'connect_output.png'
        img = cv2.imread(img_path)
        img = cv2.resize(img, (410, 410))
        height, width, channel = img.shape
        qimg = QImage(img, width, height, 3 * width, QImage.Format_RGB888).rgbSwapped()
        self.ui.label_tire_all.setPixmap(QPixmap.fromImage(qimg))
        self.ShowDefectLocation.start()

    def display_defect_location(self):
        defect_location = GetLabelName.label_defect_location
        defect_check = GetLabelName.label_defect_check
        defect_rate = GetLabelName.label_defect_rate
        json_defect_str = ''

        for defect, element in enumerate(self.ShowDefectLocation.dict_defect_location):
            if self.ShowDefectLocation.dict_defect_location[defect]:
                if self.translate_to_zh_tw:
                    direction = GetLabelName.label_defect_direction_zh
                else:
                    direction = GetLabelName.label_defect_direction_en
                location = self.ShowDefectLocation.dict_defect_location
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
            GetResultCSV(self.ShowDefectLocation.dict_defect_location,
                         self.ShowDefectLocation.defect_rate,
                         self.translate_to_zh_tw)
        except Exception:
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

    def __init__(self, parent=None):
        super().__init__()

    def run(self):
        # 進行圖片透視校正與擷取ROI，預測圖片後進行圖片拼接
        # left camera
        transformation_image(f"{picture_path}left/", f"{perspective_path}left/")
        get_roi(f"{perspective_path}left/", f"{roi_path}left/")
        # right camera
        transformation_image(f"{picture_path}right/", f"{perspective_path}right/", flip_vertical=False, loc='right')
        get_roi(f"{perspective_path}right/", f"{roi_path}right/", loc='right')
        self.ReadPartImageFinished.emit()

        os.system(predict_script)  # 預測圖片
        connect_picture(predict_path)
        self.ReadAllImageFinished.emit()


class ShowDefectLocation(QtCore.QThread):
    """
    Convert predict label and calculate masks to their areas.
    Store location data and rate and wait to send them to display_defect_location function.
    """
    ConvertMaskAreaFinished = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        RLE_to_mask_area(f"{output_file_path}/preds/",
                         f"{output_file_path}/areas/")
        self.dict_defect_location = show_defect(f"{output_file_path}/areas/")
        self.defect_rate = get_defect_rate(f"{output_file_path}/areas/",
                                           f"{roi_path}left/")
        self.ConvertMaskAreaFinished.emit()
