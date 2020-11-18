from PySide2.QtGui import QPixmap, QImage, QFont
from PySide2.QtCore import Qt, Slot, Signal, QObject, QThread, QTimer
from PySide2.QtWidgets import QFrame, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QMessageBox, QToolTip
import time


class TaskForm(QFrame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi()
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress_flash)

    def setupUi(self):
        self.setWindowTitle('设置任务详情')
        self.flayout = QFormLayout(self)
        form_dict = dict(关键词=QLineEdit(),
                         休息数量=QLineEdit(),
                         休息间隔=QLineEdit(),
                         持续时间=QLineEdit())
        form_data_dict = dict()

        for i in form_dict:
            if i == '休息数量':
                form_data_dict[i] = '20'
                form_dict[i].setPlaceholderText('单位:个；默认20个')
            elif i == '休息间隔':
                form_data_dict[i] = '10'
                form_dict[i].setPlaceholderText('单位:秒；默认10秒')
            elif i == '持续时间':
                form_data_dict[i] = '45'
                form_dict[i].setPlaceholderText('单位:分钟；默认45分钟')
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
        self.run_task()

    def run_task(self):
        self.parent.hub.run(form_data_dict=self.form_data_dict,
                            serial=self.parent.serial)

        self.task = self.parent.hub.task_pool[self.parent.serial]
        self.parent.total_time_left.setRange(
            0,
            int(self.task.form_data_dict['持续时间']) * 60)
        self.parent.qty_left.setRange(0, int(self.task.form_data_dict['休息数量']))
        self.timer.start(1000)
        # self.pthread = PThread(self)
        # self.pthread.start()

    def progress_flash(self):
        self.task = self.parent.hub.task_pool[self.parent.serial]
        self.parent.total_time_left.setValue(
            int(time.time() - self.task.start_at))
        self.parent.qty_left.setValue(int(self.task.qty))
        print(time.time() - self.task.start_at)


class PThread(QThread):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.task = self.parent.parent.hub.task_pool[self.parent.parent.serial]
        self.parent.parent.total_time_left.setRange(
            0,
            int(self.task.form_data_dict['持续时间']) * 60)
        self.parent.parent.qty_left.setRange(
            0, int(self.task.form_data_dict['休息数量']))

    def run(self):
        while (True):
            self.sleep(1)
            self.parent.parent.total_time_left.setValue(
                int(time.time() - self.task.start_at))
            self.parent.parent.qty_left.setValue(int(self.task.qty))
            print(time.time() - self.task.start_at)
