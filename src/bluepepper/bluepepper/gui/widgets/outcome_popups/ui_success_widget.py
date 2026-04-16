# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'success_widgetNKGFOE.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


class Ui_success_widget(object):
    def setupUi(self, success_widget):
        if not success_widget.objectName():
            success_widget.setObjectName(u"success_widget")
        success_widget.resize(271, 132)
        self.verticalLayout = QVBoxLayout(success_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.main_widget = QWidget(success_widget)
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

        self.main_frame = QFrame(self.main_widget)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.main_frame)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(9, 9, 9, 9)
        self.label_message = QLabel(self.main_frame)
        self.label_message.setObjectName(u"label_message")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_message)


        self.verticalLayout_2.addWidget(self.main_frame)

        self.frame_bottom = QFrame(self.main_widget)
        self.frame_bottom.setObjectName(u"frame_bottom")
        sizePolicy.setHeightForWidth(self.frame_bottom.sizePolicy().hasHeightForWidth())
        self.frame_bottom.setSizePolicy(sizePolicy)
        self.frame_bottom.setFrameShape(QFrame.StyledPanel)
        self.frame_bottom.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_bottom)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.button_ok = QPushButton(self.frame_bottom)
        self.button_ok.setObjectName(u"button_ok")
        self.button_ok.setMinimumSize(QSize(80, 0))
        self.button_ok.setAutoDefault(True)

        self.horizontalLayout.addWidget(self.button_ok)


        self.verticalLayout_2.addWidget(self.frame_bottom)


        self.verticalLayout.addWidget(self.main_widget)


        self.retranslateUi(success_widget)

        self.button_ok.setDefault(True)


        QMetaObject.connectSlotsByName(success_widget)
    # setupUi

    def retranslateUi(self, success_widget):
        success_widget.setWindowTitle(QCoreApplication.translate("success_widget", u"Form", None))
        self.label_title.setText(QCoreApplication.translate("success_widget", u"Success", None))
        self.label_title.setProperty("tag", QCoreApplication.translate("success_widget", u"H2", None))
        self.label_message.setText(QCoreApplication.translate("success_widget", u"Everything worked perfectly", None))
        self.button_ok.setText(QCoreApplication.translate("success_widget", u"Ok", None))
        self.button_ok.setProperty("status", QCoreApplication.translate("success_widget", u"important", None))
    # retranslateUi

