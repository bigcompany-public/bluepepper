# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'helpme_widgettzwWVz.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


class Ui_helpme_widget(object):
    def setupUi(self, helpme_widget):
        if not helpme_widget.objectName():
            helpme_widget.setObjectName(u"helpme_widget")
        helpme_widget.resize(540, 635)
        self.verticalLayout = QVBoxLayout(helpme_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.main_widget = QWidget(helpme_widget)
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

        self.frame_info = QFrame(self.main_widget)
        self.frame_info.setObjectName(u"frame_info")
        self.frame_info.setFrameShape(QFrame.StyledPanel)
        self.frame_info.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.frame_info)
        self.formLayout.setObjectName(u"formLayout")
        self.l_name = QLabel(self.frame_info)
        self.l_name.setObjectName(u"l_name")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.l_name)

        self.le_name = QLineEdit(self.frame_info)
        self.le_name.setObjectName(u"le_name")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.le_name)

        self.l_file = QLabel(self.frame_info)
        self.l_file.setObjectName(u"l_file")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.l_file)

        self.label_file = QLabel(self.frame_info)
        self.label_file.setObjectName(u"label_file")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.label_file)

        self.l_asset = QLabel(self.frame_info)
        self.l_asset.setObjectName(u"l_asset")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.l_asset)

        self.label_asset = QLabel(self.frame_info)
        self.label_asset.setObjectName(u"label_asset")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.label_asset)

        self.l_shot = QLabel(self.frame_info)
        self.l_shot.setObjectName(u"l_shot")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.l_shot)

        self.label_shot = QLabel(self.frame_info)
        self.label_shot.setObjectName(u"label_shot")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.label_shot)

        self.l_user = QLabel(self.frame_info)
        self.l_user.setObjectName(u"l_user")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.l_user)

        self.l_computer = QLabel(self.frame_info)
        self.l_computer.setObjectName(u"l_computer")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.l_computer)

        self.label_user = QLabel(self.frame_info)
        self.label_user.setObjectName(u"label_user")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.label_user)

        self.label_computer = QLabel(self.frame_info)
        self.label_computer.setObjectName(u"label_computer")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.label_computer)

        self.l_error = QLabel(self.frame_info)
        self.l_error.setObjectName(u"l_error")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.l_error)

        self.l_traceback = QLabel(self.frame_info)
        self.l_traceback.setObjectName(u"l_traceback")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.l_traceback)

        self.sa_error = QScrollArea(self.frame_info)
        self.sa_error.setObjectName(u"sa_error")
        self.sa_error.setWidgetResizable(True)
        self.sa_error_contents = QWidget()
        self.sa_error_contents.setObjectName(u"sa_error_contents")
        self.sa_error_contents.setGeometry(QRect(0, 0, 436, 69))
        self.verticalLayout_3 = QVBoxLayout(self.sa_error_contents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_error = QLabel(self.sa_error_contents)
        self.label_error.setObjectName(u"label_error")
        self.label_error.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.label_error)

        self.sa_error.setWidget(self.sa_error_contents)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.sa_error)

        self.sa_traceback = QScrollArea(self.frame_info)
        self.sa_traceback.setObjectName(u"sa_traceback")
        self.sa_traceback.setWidgetResizable(True)
        self.sa_traceback_contents = QWidget()
        self.sa_traceback_contents.setObjectName(u"sa_traceback_contents")
        self.sa_traceback_contents.setGeometry(QRect(0, 0, 436, 69))
        self.verticalLayout_4 = QVBoxLayout(self.sa_traceback_contents)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_traceback = QLabel(self.sa_traceback_contents)
        self.label_traceback.setObjectName(u"label_traceback")
        self.label_traceback.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_4.addWidget(self.label_traceback)

        self.sa_traceback.setWidget(self.sa_traceback_contents)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.sa_traceback)


        self.verticalLayout_2.addWidget(self.frame_info)

        self.label_help_us = QLabel(self.main_widget)
        self.label_help_us.setObjectName(u"label_help_us")

        self.verticalLayout_2.addWidget(self.label_help_us)

        self.frame_context = QFrame(self.main_widget)
        self.frame_context.setObjectName(u"frame_context")
        self.frame_context.setFrameShape(QFrame.StyledPanel)
        self.frame_context.setFrameShadow(QFrame.Raised)
        self.formLayout_2 = QFormLayout(self.frame_context)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.l_description = QLabel(self.frame_context)
        self.l_description.setObjectName(u"l_description")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.l_description)

        self.le_description = QLineEdit(self.frame_context)
        self.le_description.setObjectName(u"le_description")
        self.le_description.setMinimumSize(QSize(0, 70))
        self.le_description.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.le_description)

        self.l_screenshots = QLabel(self.frame_context)
        self.l_screenshots.setObjectName(u"l_screenshots")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.l_screenshots)

        self.l_empty = QLabel(self.frame_context)
        self.l_empty.setObjectName(u"l_empty")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.l_empty)

        self.list_screenshots = QListWidget(self.frame_context)
        self.list_screenshots.setObjectName(u"list_screenshots")
        self.list_screenshots.setMinimumSize(QSize(0, 100))
        self.list_screenshots.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.list_screenshots.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list_screenshots.setProperty("showDropIndicator", False)
        self.list_screenshots.setDragDropMode(QAbstractItemView.DragOnly)
        self.list_screenshots.setDefaultDropAction(Qt.IgnoreAction)
        self.list_screenshots.setViewMode(QListView.IconMode)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.list_screenshots)

        self.frame = QFrame(self.frame_context)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pb_add_screenshot = QPushButton(self.frame)
        self.pb_add_screenshot.setObjectName(u"pb_add_screenshot")

        self.horizontalLayout_2.addWidget(self.pb_add_screenshot)

        self.pb_remove_screenshot = QPushButton(self.frame)
        self.pb_remove_screenshot.setObjectName(u"pb_remove_screenshot")

        self.horizontalLayout_2.addWidget(self.pb_remove_screenshot)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.frame)


        self.verticalLayout_2.addWidget(self.frame_context)

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

        self.button_open_ticket = QPushButton(self.frame_bottom)
        self.button_open_ticket.setObjectName(u"button_open_ticket")
        self.button_open_ticket.setMinimumSize(QSize(80, 0))
        self.button_open_ticket.setAutoDefault(True)

        self.horizontalLayout.addWidget(self.button_open_ticket)


        self.verticalLayout_2.addWidget(self.frame_bottom)


        self.verticalLayout.addWidget(self.main_widget)


        self.retranslateUi(helpme_widget)

        self.button_open_ticket.setDefault(True)


        QMetaObject.connectSlotsByName(helpme_widget)
    # setupUi

    def retranslateUi(self, helpme_widget):
        helpme_widget.setWindowTitle(QCoreApplication.translate("helpme_widget", u"Form", None))
        self.label_title.setText(QCoreApplication.translate("helpme_widget", u"HelpMe", None))
        self.label_title.setProperty("tag", QCoreApplication.translate("helpme_widget", u"H2", None))
        self.l_name.setText(QCoreApplication.translate("helpme_widget", u"Ticket Name", None))
        self.l_file.setText(QCoreApplication.translate("helpme_widget", u"File", None))
        self.label_file.setText(QCoreApplication.translate("helpme_widget", u"path/to/file", None))
        self.l_asset.setText(QCoreApplication.translate("helpme_widget", u"Asset", None))
        self.label_asset.setText(QCoreApplication.translate("helpme_widget", u"assetName", None))
        self.l_shot.setText(QCoreApplication.translate("helpme_widget", u"Shot", None))
        self.label_shot.setText(QCoreApplication.translate("helpme_widget", u"shotId", None))
        self.l_user.setText(QCoreApplication.translate("helpme_widget", u"User", None))
        self.l_computer.setText(QCoreApplication.translate("helpme_widget", u"Computer", None))
        self.label_user.setText(QCoreApplication.translate("helpme_widget", u"user.name", None))
        self.label_computer.setText(QCoreApplication.translate("helpme_widget", u"computer.name", None))
        self.l_error.setText(QCoreApplication.translate("helpme_widget", u"Error", None))
        self.l_traceback.setText(QCoreApplication.translate("helpme_widget", u"Traceback", None))
        self.label_error.setText(QCoreApplication.translate("helpme_widget", u"Error", None))
        self.label_error.setProperty("status", QCoreApplication.translate("helpme_widget", u"code", None))
        self.label_traceback.setText(QCoreApplication.translate("helpme_widget", u"Traceback", None))
        self.label_traceback.setProperty("status", QCoreApplication.translate("helpme_widget", u"code", None))
        self.label_help_us.setText(QCoreApplication.translate("helpme_widget", u"Help us to help you", None))
        self.label_help_us.setProperty("tag", QCoreApplication.translate("helpme_widget", u"H2", None))
        self.l_description.setText(QCoreApplication.translate("helpme_widget", u"Description", None))
        self.l_screenshots.setText(QCoreApplication.translate("helpme_widget", u"Screenshots", None))
        self.l_empty.setText("")
        self.pb_add_screenshot.setText(QCoreApplication.translate("helpme_widget", u"Add Screenshot", None))
        self.pb_add_screenshot.setProperty("status", QCoreApplication.translate("helpme_widget", u"important", None))
        self.pb_remove_screenshot.setText(QCoreApplication.translate("helpme_widget", u"Remove ScreenShot", None))
        self.pb_remove_screenshot.setProperty("status", QCoreApplication.translate("helpme_widget", u"danger", None))
        self.button_open_ticket.setText(QCoreApplication.translate("helpme_widget", u"Open Ticket", None))
        self.button_open_ticket.setProperty("status", QCoreApplication.translate("helpme_widget", u"important", None))
    # retranslateUi

