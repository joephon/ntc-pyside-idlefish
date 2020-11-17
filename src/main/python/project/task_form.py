from PySide2.QtGui import QPixmap, QImage, QFont
from PySide2.QtCore import Qt, Slot, Signal, QObject
from PySide2.QtWidgets import QFrame, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QMessageBox, QToolTip


class TaskForm(QFrame):
    def __init__(self, parent):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('设置任务详情')
        self.flayout = QFormLayout(self)
        form_dict = dict(关键词=QLineEdit(), 休息间隔=QLineEdit(), 持续时间=QLineEdit())
        form_data_dict = dict()

        for i in form_dict:
            if i == '休息间隔':
                form_data_dict[i] = '15'
                form_dict[i].setPlaceholderText('单位:秒')
            elif i == '持续时间':
                form_data_dict[i] = '60'
                form_dict[i].setPlaceholderText('单位:分钟')
            else:
                form_data_dict[i] = ''
                form_dict[i].setPlaceholderText('关键词')
            form_dict[i].textChanged.connect(self.on_text_changed(i))
            self.flayout.addRow(i, form_dict[i])

        start_btn = QPushButton('开始任务')
        start_btn.clicked.connect(self.on_start_task)
        self.flayout.addRow(start_btn)
        self.form_data_dict = form_data_dict
        self.resize(260, 180)
        self.show()

    def on_text_changed(self, which):
        def handle_text_changed(value):
            self.form_data_dict[which] = value

        return handle_text_changed

    def on_start_task(self):
        if not self.form_data_dict['关键词']:
            return QMessageBox.warning(self, '错误提示', '请输入关键词', QMessageBox.Ok)
        self.hide()
        self.working = True
        self.setStyleSheet('background-color:orange')
        self.run_task()

    def done(self):
        self.working = False
        self.setStyleSheet('background-color:#2ABf9E')

    def run_task(self):
        pass
        # self.task = TTask(name='go', boss=self)
        # self.task.start()
        # self.bg.setToolTip('该设备执行任务中...')