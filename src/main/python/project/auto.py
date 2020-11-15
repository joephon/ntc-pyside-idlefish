import os
import time
import asyncio
import re
import cv2
import base64
import threading
import traceback
import uiautomator2 as u2
from adbutils import adb
from PySide2.QtGui import QPixmap, QImage, QFont
from PySide2.QtCore import Qt, Slot, Signal, QObject
from PySide2.QtWidgets import QMessageBox


class DeviceHub(QObject):
    seeked = Signal(list)
    called = Signal(dict)
    _instance_lock = threading.Lock()

    def __init__(self):
        super().__init__()
        self.adb = adb
        self.store = dict()
        self.hold = list()

    def __new__(cls, *args, **kwargs):
        if not hasattr(DeviceHub, "_instance"):
            with DeviceHub._instance_lock:
                if not hasattr(DeviceHub, "_instance"):
                    DeviceHub._instance = QObject.__new__(cls)
        return DeviceHub._instance

    def seek(self):
        try:
            self.hold = [i for i in adb.devices()]
            self.seeked.emit(self.hold)
            if not len(self.hold):
                return QMessageBox.information(self, '提示信息', '未发现设备',
                                               QMessageBox.Ok)
        except Exception as error:
            traceback.print_exc()
            print(error)

    def call(self, serial=None):
        try:
            self.store[serial] = u2.connect(serial)
            self.called.emit(dict(serial=self.store[serial]))
        except Exception as error:
            traceback.print_exc()
            print(error)
