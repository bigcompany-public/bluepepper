# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'launcher_widgetYBJsyL.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


class Ui_launcher_widget(object):
    def setupUi(self, launcher_widget):
        if not launcher_widget.objectName():
            launcher_widget.setObjectName(u"launcher_widget")
        launcher_widget.resize(721, 486)
        self.verticalLayout = QVBoxLayout(launcher_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.main_widget = QWidget(launcher_widget)
        self.main_widget.setObjectName(u"main_widget")
        self.verticalLayout_2 = QVBoxLayout(self.main_widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_title = QLabel(self.main_widget)
        self.label_title.setObjectName(u"label_title")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.label_title)

        self.frame_apps = QFrame(self.main_widget)
        self.frame_apps.setObjectName(u"frame_apps")
        self.frame_apps.setFrameShape(QFrame.StyledPanel)
        self.frame_apps.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_apps)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_apps = QLabel(self.frame_apps)
        self.label_apps.setObjectName(u"label_apps")

        self.verticalLayout_3.addWidget(self.label_apps)

        self.list_apps = QListWidget(self.frame_apps)
        self.list_apps.setObjectName(u"list_apps")
        self.list_apps.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list_apps.setSelectionMode(QAbstractItemView.NoSelection)
        self.list_apps.setViewMode(QListView.IconMode)

        self.verticalLayout_3.addWidget(self.list_apps)


        self.verticalLayout_2.addWidget(self.frame_apps)

        self.frame_tools = QFrame(self.main_widget)
        self.frame_tools.setObjectName(u"frame_tools")
        self.frame_tools.setFrameShape(QFrame.StyledPanel)
        self.frame_tools.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_tools)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_tools = QLabel(self.frame_tools)
        self.label_tools.setObjectName(u"label_tools")

        self.verticalLayout_4.addWidget(self.label_tools)

        self.list_tools = QListWidget(self.frame_tools)
        self.list_tools.setObjectName(u"list_tools")

        self.verticalLayout_4.addWidget(self.list_tools)


        self.verticalLayout_2.addWidget(self.frame_tools)


        self.verticalLayout.addWidget(self.main_widget)


        self.retranslateUi(launcher_widget)

        QMetaObject.connectSlotsByName(launcher_widget)
    # setupUi

    def retranslateUi(self, launcher_widget):
        launcher_widget.setWindowTitle(QCoreApplication.translate("launcher_widget", u"Form", None))
        self.label_title.setText(QCoreApplication.translate("launcher_widget", u"Launcher", None))
        self.label_title.setProperty("tag", QCoreApplication.translate("launcher_widget", u"H2", None))
        self.label_apps.setText(QCoreApplication.translate("launcher_widget", u"Apps", None))
        self.label_apps.setProperty("tag", "")
        self.label_tools.setText(QCoreApplication.translate("launcher_widget", u"Tools", None))
    # retranslateUi

