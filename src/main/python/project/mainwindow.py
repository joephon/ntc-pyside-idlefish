from PySide2.QtWidgets import QMainWindow, QLabel, QMessageBox, QFrame, QHBoxLayout, QPushButton
from PySide2.QtCore import Qt, Slot, Signal
from ui.mainwindow import Ui_MainWindow
from project.auto import DeviceHub


class MainWindow(QMainWindow):
    seeked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.setWindowState(Qt.WindowMaximized)
        self.init_events()
        self.hub = DeviceHub()
        self.hub.seeked.connect(self.on_hub_seek)
        self.seeked.connect(self.show_result)

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
        self.devices = devices
        self.ui.searchBtn.setText('搜索设备')
        QMessageBox.information(self, '搜索结果',
                                '发现{}台设备'.format(len(self.devices)),
                                QMessageBox.Ok)

        if len(devices):
            self.seeked.emit()

    @Slot()
    def show_result(self):
        self.panel = QFrame()
        self.panel_layout = QHBoxLayout(self.panel)
        for i in self.devices:
            setattr(self, i.serial, QFrame())
            layout = QHBoxLayout(getattr(self, i.serial))
            bg = QPushButton(i.serial)
            #  bg.setScaledContents(True)
            bg.setStyleSheet('background-color:orange;')
            layout.addWidget(bg)
            self.panel_layout.addWidget(getattr(self, i.serial))
        self.panel.show()
