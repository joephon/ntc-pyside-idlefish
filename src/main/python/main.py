from fbs_runtime.application_context.PySide2 import ApplicationContext
from PySide2.QtWidgets import QMainWindow
from project.mainwindow import MainWindow

import sys

if __name__ == '__main__':
    appctx = ApplicationContext()  # 1. Instantiate ApplicationContext
    window = MainWindow()
    style_sheet = appctx.get_resource('default.qss')
    appctx.app.setStyleSheet(open(style_sheet).read())
    # window.resize(1400, 900)
    window.show()
    exit_code = appctx.app.exec_()  # 2. Invoke appctx.app.exec_()
    sys.exit(exit_code)