from PySide2.QtWidgets import QLabel, QMessageBox, QFrame, QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton, QProgressBar
from PySide2.QtCore import Qt, Slot, Signal, QTimer, QThread
from PySide2.QtGui import QPixmap
from fbs_runtime.application_context.PySide2 import ApplicationContext
from project.auto import DeviceHub
from project.task_form import TaskForm
import time


class Device(QFrame, ApplicationContext):
    def __init__(self, parent=None, serial=None, hub=None):
        super().__init__(parent)
        self.serial = serial
        self.hub = hub
        self.setupUi()
        self.working = False
        self.btn.clicked.connect(self.on_btn_clicked)
        self.hub.called.connect(self.on_called)

    def setupUi(self):
        self.setObjectName('box')
        self.vlayout = QVBoxLayout(self)

        # tip
        self.tip = QLabel('序列号: {}'.format(self.serial))
        self.tip.setObjectName('tip')

        # bg
        self.bg = QLabel()
        self.bg.setObjectName('bg')
        self.bglayout = QHBoxLayout(self.bg)

        # progress
        self.progress_panel = QFrame(self)
        self.progress_layout = QFormLayout(self.progress_panel)

        # total time progress
        self.total_time_left = QProgressBar(self)
        self.total_time_left.setRange(0, 100)

        # sleep progress
        self.qty_left = QProgressBar(self)
        self.qty_left.setRange(0, 100)

        # sleep progress
        self.sleep_left = QProgressBar(self)
        self.sleep_left.setRange(0, 100)

        self.progress_layout.addRow('任务进度:', self.total_time_left)
        self.progress_layout.addRow('宝贝数量:', self.qty_left)
        # self.progress_layout.addRow('休息进度', self.sleep_left)

        # btn
        self.btn = QPushButton('使用设备')
        self.btn.setObjectName('btn')

        self.bglayout.addWidget(self.btn)
        self.vlayout.addWidget(self.tip)
        self.vlayout.addWidget(self.bg)
        self.vlayout.addWidget(self.progress_panel)

        style_sheet = self.get_resource('device.qss')
        self.setStyleSheet(open(style_sheet).read())

    def on_btn_clicked(self, e):
        text = self.btn.text()
        if text == '使用设备':
            self.btn.setText('启动设备中...')
            self.hub.call(self.serial)
            self.d = self.hub.store[self.serial]
            self.img_data = self.d.screenshot()
            # self.bg.setPixmap(
            #     QPixmap(self.img_data.toqpixmap().scaled(
            #         300, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
            self.bg.setPixmap(QPixmap(self.img_data.toqpixmap()))
            self.bg.setScaledContents(True)
            self.btn.setText('开始任务')
            self.update_panel()

        elif text == '开始任务':
            self.task_form = TaskForm(self)
            self.btn.setText('结束任务')

        elif text == '结束任务':
            self.hub.task_pool[self.serial].stop()
            self.btn.setText('开始任务')

    def update_panel(self):
        self.u = UThread(self)
        self.u.start()

    @Slot(dict)
    def on_called(self, device):
        pass


class UThread(QThread):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

    def run(self):
        while (True):
            self.parent.img_data = self.parent.d.screenshot()
            self.parent.bg.setPixmap(QPixmap(self.parent.img_data.toqpixmap()))
            self.sleep(1)
