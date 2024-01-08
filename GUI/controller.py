from PyQt5 import QtWidgets, QtGui, QtCore
from UI import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # in python3, super(Class, self).xxx = super().xxx
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        # TODO
        pass

class ReadPartImage(QtCore.QThread):  # 繼承 QtCore.QThread 來建立 SystemTime 類別
    '''讀取圖片並做圖片校正與旋轉'''
    def run(self):
        self.

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
