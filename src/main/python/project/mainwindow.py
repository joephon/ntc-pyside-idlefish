from PySide2.QtWidgets import QMainWindow, QLabel, QMessageBox, QFrame, QHBoxLayout, QPushButton
from PySide2.QtCore import Qt, Slot, Signal
from ui.mainwindow import Ui_MainWindow
from project.auto import DeviceHub
from project.device import Device


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.setWindowState(Qt.WindowMaximized)
        self.init_events()
        self.hub = DeviceHub()
        self.hub.seeked.connect(self.on_hub_seek)

    def init_events(self):
        self.ui.searchBtn.clicked.connect(
            self.on_searchBtn_clicked(self.ui.searchBtn))

    def on_searchBtn_clicked(self, which):
        def on(e):
            which.setText('搜索中...')
            self.hub.seek()

        return on

    @Slot(list)
    def on_hub_seek(self, devices):
        self.ui.searchBtn.setText('搜索设备')
        QMessageBox.information(self, '搜索结果',
                                '发现{}台设备'.format(len(self.hub.hold)),
                                QMessageBox.Ok)

        if len(devices):
            self.show_result()

    @Slot()
    def show_result(self):
        self.panel = QFrame()
        self.panel.setWindowTitle('设备列表')
        self.panel_layout = QHBoxLayout(self.panel)
        for i in self.hub.hold:
            device = Device(serial=i.serial, hub=self.hub)
            self.panel_layout.addWidget(device)
        self.panel.show()
