import time
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui

from UI import Ui_MainWindow
from create_folder import create_folder


class Camera(QtCore.QThread):  # 繼承 QtCore.QThread 來建立 Camera 類別
    rawdata = QtCore.pyqtSignal(np.ndarray)  # 建立傳遞信號，需設定傳遞型態為 np.ndarray

    def __init__(self, parent=None, camera_num: int = 0):
        """ 初始化
            - 執行 QtCore.QThread 的初始化
            - 建立 cv2 的 VideoCapture 物件
            - 設定屬性來確認狀態
              - self.connect：連接狀態
              - self.running：讀取狀態
        """
        # 將父類初始化
        super().__init__(parent)
        self.cam = cv2.VideoCapture(camera_num)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 4000)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 3000)
        # self.cam.set(cv2.CAP_PROP_FPS, 2)
        # self.fps = 0
        # 判斷攝影機是否正常連接
        if self.cam is None or not self.cam.isOpened():
            self.connect = False
            self.running = False
        else:
            self.connect = True
            self.running = False

    def run(self):
        """ 執行多執行緒 - 讀取影像 - 發送影像 - 簡易異常處理 """
        width = 440
        height = 330
        # 當正常連接攝影機才能進入迴圈
        while self.running and self.connect:
            ret, img = self.cam.read()  # 讀取影像
            frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (width, height))

            self.rawdata.emit(img)  # 發送影像
            # else:    # 例外處理
            #    print("Warning!!!")
            #    self.connect = False

            # self.fps = self.fps + 1
            # if self.fps == 3:
            #     self.fps = 0

    def open(self):
        """ 開啟攝影機影像讀取功能 """
        if self.connect:
            self.running = True  # 啟動讀取狀態

    def stop(self):
        """ 暫停攝影機影像讀取功能 """
        if self.connect:
            self.running = False  # 關閉讀取狀態

    def close(self):
        """ 關閉攝影機功能 """
        if self.connect:
            self.running = False  # 關閉讀取狀態
            time.sleep(1)
            self.cam.release()  # 釋放攝影機


class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        create_folder()
        self.setup_control()

        # 設定相機功能
        self.ProcessCamLeft = Camera(camera_num=0)  # 建立相機物件
        self.ProcessCamRight = Camera(camera_num=1)  # 建立相機物件
        if self.ProcessCamLeft.connect:
            # 連接影像訊號 (rawdata) 至 getRaw()
            self.ProcessCamLeft.rawdata.connect(self.getRaw)  # 槽功能：取得並顯示影像
            self.ui.pushButton_left_open.setEnabled(True)  # 攝影機啟動按鈕的狀態：ON
        else:
            self.ui.pushButton_left_open.setEnabled(False)  # 攝影機啟動按鈕的狀態：OFF
        self.ui.pushButton_left_close.setEnabled(False)  # 攝影機的其他功能狀態：OFF

    def setup_control(self):
        # 連接按鍵
        self.ui.pushButton_left_open.clicked.connect(self.openCam)  # 槽功能：開啟攝影機
        self.ui.pushButton_left_close.clicked.connect(self.stopCam)  # 槽功能：暫停讀取影像

    def getRaw(self, data):  # 取得影像  # data 為接收到的影像
        self.showData(data)  # 將影像傳入至 showData()

    def openCam(self):
        """ 啟動攝影機的影像讀取 """
        if self.ProcessCamLeft.connect:  # 判斷攝影機是否可用
            self.ProcessCamLeft.open()  # 影像讀取功能開啟
            self.ProcessCamLeft.start()  # 在子緒啟動影像讀取
            # 按鈕的狀態：啟動 OFF、暫停 ON、視窗大小 ON
            self.ui.pushButton_left_open.setEnabled(False)
            self.ui.pushButton_left_close.setEnabled(True)

    def stopCam(self):
        """ 凍結攝影機的影像 """
        if self.ProcessCamLeft.connect:  # 判斷攝影機是否可用
            self.ProcessCamLeft.stop()  # 影像讀取功能關閉
            # 按鈕的狀態：啟動 ON、暫停 OFF、視窗大小 OFF
            self.ui.pushButton_left_open.setEnabled(True)
            self.ui.pushButton_left_close.setEnabled(False)

    def showData(self, img):
        """ 顯示攝影機的影像 """
        height, width, _ = img.shape  # 取得影像尺寸
        qimg = QtGui.QImage(img.data, height, width, QtGui.QImage.Format_RGB888).rgbSwapped()
        self.ui.label_camera_left.setScaledContents(True)  # 尺度可變
        self.ui.label_camera_left.setPixmap(QtGui.QPixmap.fromImage(qimg))
