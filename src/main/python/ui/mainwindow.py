# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 700)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QSize(0, 0))
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setElideMode(Qt.ElideRight)
        self.tab_device = QWidget()
        self.tab_device.setObjectName(u"tab_device")
        self.horizontalLayout = QHBoxLayout(self.tab_device)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.searchBtn = QPushButton(self.tab_device)
        self.searchBtn.setObjectName(u"searchBtn")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.searchBtn.sizePolicy().hasHeightForWidth())
        self.searchBtn.setSizePolicy(sizePolicy1)
        self.searchBtn.setMinimumSize(QSize(300, 500))
        self.searchBtn.setBaseSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.searchBtn)

        self.tabWidget.addTab(self.tab_device, "")
        self.tab_data = QWidget()
        self.tab_data.setObjectName(u"tab_data")
        self.tabWidget.addTab(self.tab_data, "")

        self.horizontalLayout_3.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.searchBtn.setText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22\u8bbe\u5907", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_device), QCoreApplication.translate("MainWindow", u"\u8bbe\u5907", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_data), QCoreApplication.translate("MainWindow", u"\u6570\u636e", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u9000\u51fa", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u66f4\u65b0", None))
    # retranslateUi

