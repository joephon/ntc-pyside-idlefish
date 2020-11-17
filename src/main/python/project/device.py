from PySide2.QtWidgets import QLabel, QMessageBox, QFrame, QVBoxLayout, QHBoxLayout, QPushButton
from PySide2.QtCore import Qt, Slot, Signal
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
        self.tip = QLabel('序列号: {}'.format(self.serial))
        self.tip.setObjectName('tip')
        self.bg = QLabel()
        self.bg.setObjectName('bg')
        self.bglayout = QHBoxLayout(self.bg)
        self.btn = QPushButton('使用设备')
        self.btn.setObjectName('btn')
        self.bglayout.addWidget(self.btn)
        self.vlayout.addWidget(self.tip)
        self.vlayout.addWidget(self.bg)

        style_sheet = self.get_resource('device.qss')
        self.setStyleSheet(open(style_sheet).read())

    def on_btn_clicked(self, e):
        text = self.btn.text()
        if text == '使用设备':
            self.btn.setText('启动设备中...')
            self.hub.call(self.serial)
            img_data = self.hub.store[self.serial].screenshot()
            self.bg.setPixmap(QPixmap(img_data.toqpixmap()))
            self.bg.setScaledContents(True)
            self.btn.setText('开始任务')

        elif text == '开始任务':
            self.task_form = TaskForm(self)
            self.btn.setText('结束任务')

        elif text == '结束任务':
            print('end')

        # self.btn.hide()

    @Slot(dict)
    def on_called(self, device):
        pass
