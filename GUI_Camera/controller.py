import imagingcontrol4 as ic4
from functools import partial
from PyQt5 import QtWidgets

from UI import Ui_MainWindow
from create_folder import create_folder

path = '../GUI/images/picture'


def _window_handle(wnd: QtWidgets.QWidget) -> int:
    # Helper function to get window handle from a QWidget
    return wnd.winId().__int__()


class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        create_folder()
        self.setup_control()
        self.img_num_left = 0
        self.img_num_right = 0
        self.grabber_l, self.sink_l, self.display_l = self.create_display('left')
        self.grabber_r, self.sink_r, self.display_r = self.create_display('right')

    def create_display(self, pos: str):
        try:
            if pos == 'left':
                first_device_info = ic4.DeviceEnum.devices()[0]
                camera_pos = self.ui.label_camera_left
            else:
                first_device_info = ic4.DeviceEnum.devices()[1]
                camera_pos = self.ui.label_camera_right
        except:
            print("The camera can't open.")
        # Create a Grabber object
        grab = ic4.Grabber()
        grab.device_open(first_device_info)
        # Create an IC4 EmbeddedDisplay that is using video_widget from above as presentation area
        display = ic4.EmbeddedDisplay(_window_handle(camera_pos))
        # Configure the display to neatly stretch and center the live image
        display.set_render_position(ic4.DisplayRenderPosition.STRETCH_CENTER)
        try:
            grab.device_property_map.set_value(ic4.PropId.USER_SET_SELECTOR, "Default")
            grab.device_property_map.execute_command(ic4.PropId.USER_SET_LOAD)
        except ic4.IC4Exception:
            # The driver/device might not support this, ignore and move on
            pass
        # Create a SnapSink. A SnapSink allows grabbing single images (or image sequences) out of a data stream.
        sink = ic4.SnapSink()

        return grab, sink, display

    def setup_control(self):
        # 連接按鍵
        self.ui.pushButton_left_open.clicked.connect(partial(self.open_cam, location='left'))  # 槽功能：開啟攝影機
        self.ui.pushButton_left_close.clicked.connect(partial(self.stop_cam, location='left'))  # 槽功能：暫停讀取影像
        self.ui.pushButton_left_save.clicked.connect(partial(self.save_image, location='left'))
        self.ui.pushButton_right_open.clicked.connect(partial(self.open_cam, location='right'))  # 槽功能：開啟攝影機
        self.ui.pushButton_right_close.clicked.connect(partial(self.stop_cam, location='right'))  # 槽功能：暫停讀取影像
        self.ui.pushButton_right_save.clicked.connect(partial(self.save_image, location='right'))
        ic4.Library.init()

    def open_cam(self, location: str):
        """ 啟動攝影機的影像讀取 """
        if location == 'left':
            self.grabber_l.stream_setup(self.sink_l, self.display_l)
        else:
            self.grabber_r.stream_setup(self.sink_r, self.display_r)
        # 按鈕的狀態：啟動 OFF、暫停 ON、視窗大小 ON
        exec(f'self.ui.pushButton_{location}_open.setEnabled(False)')
        exec(f'self.ui.pushButton_{location}_close.setEnabled(True)')

    def stop_cam(self, location: str):
        """ 凍結攝影機的影像 """
        if location == 'left':
            self.grabber_l.stream_stop()
        else:
            self.grabber_r.stream_stop()
        # 按鈕的狀態：啟動 ON、暫停 OFF、視窗大小 OFF
        exec(f'self.ui.pushButton_{location}_open.setEnabled(True)')
        exec(f'self.ui.pushButton_{location}_close.setEnabled(False)')

    def save_image(self, location: str):  # 取得影像  # data 為接收到的影像
        try:
            # Grab a single image out of the data stream.
            if location == 'left':
                image = self.sink_l.snap_single(2000)
                # Print image information.
                print(f"Received a left image.")
                if self.img_num_left < 6:
                    self.img_num_left += 1
                else:
                    self.img_num_left = 1
                image.save_as_png(f'{path}/{location}/image_{self.img_num_left}.png')
                print(f'Save Image at {path}/{location}/image_{self.img_num_left}.png')
            else:
                image = self.sink_r.snap_single(2000)
                # Print image information.
                print(f"Received a right image.")
                if self.img_num_right < 6:
                    self.img_num_right += 1
                else:
                    self.img_num_right = 1
                image.save_as_png(f'{path}/{location}/image_{self.img_num_right}.png')
                print(f'Save Image at {path}/{location}/image_{self.img_num_right}.png')

        except ic4.IC4Exception as ex:
            print(ex.message)
