# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'helpme_widgetUPKiBn.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt
from qtpy.QtWidgets import (
    QAbstractItemView,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QListWidget,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_helpme_widget(object):
    def setupUi(self, helpme_widget):
        if not helpme_widget.objectName():
            helpme_widget.setObjectName("helpme_widget")
        helpme_widget.resize(540, 635)
        self.verticalLayout = QVBoxLayout(helpme_widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.main_widget = QWidget(helpme_widget)
        self.main_widget.setObjectName("main_widget")
        self.verticalLayout_2 = QVBoxLayout(self.main_widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_title = QLabel(self.main_widget)
        self.label_title.setObjectName("label_title")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.label_title)

        self.frame_info = QFrame(self.main_widget)
        self.frame_info.setObjectName("frame_info")
        self.frame_info.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_info.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout = QFormLayout(self.frame_info)
        self.formLayout.setObjectName("formLayout")
        self.l_name = QLabel(self.frame_info)
        self.l_name.setObjectName("l_name")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.l_name)

        self.le_name = QLineEdit(self.frame_info)
        self.le_name.setObjectName("le_name")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.le_name)

        self.l_file = QLabel(self.frame_info)
        self.l_file.setObjectName("l_file")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.l_file)

        self.label_file = QLabel(self.frame_info)
        self.label_file.setObjectName("label_file")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.label_file)

        self.l_asset = QLabel(self.frame_info)
        self.l_asset.setObjectName("l_asset")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.l_asset)

        self.label_asset = QLabel(self.frame_info)
        self.label_asset.setObjectName("label_asset")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.label_asset)

        self.l_shot = QLabel(self.frame_info)
        self.l_shot.setObjectName("l_shot")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.l_shot)

        self.label_shot = QLabel(self.frame_info)
        self.label_shot.setObjectName("label_shot")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.label_shot)

        self.l_user = QLabel(self.frame_info)
        self.l_user.setObjectName("l_user")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.l_user)

        self.l_computer = QLabel(self.frame_info)
        self.l_computer.setObjectName("l_computer")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.l_computer)

        self.label_user = QLabel(self.frame_info)
        self.label_user.setObjectName("label_user")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.label_user)

        self.label_computer = QLabel(self.frame_info)
        self.label_computer.setObjectName("label_computer")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.label_computer)

        self.l_error = QLabel(self.frame_info)
        self.l_error.setObjectName("l_error")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.l_error)

        self.l_traceback = QLabel(self.frame_info)
        self.l_traceback.setObjectName("l_traceback")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.l_traceback)

        self.sa_error = QScrollArea(self.frame_info)
        self.sa_error.setObjectName("sa_error")
        self.sa_error.setWidgetResizable(True)
        self.sa_error_contents = QWidget()
        self.sa_error_contents.setObjectName("sa_error_contents")
        self.sa_error_contents.setGeometry(QRect(0, 0, 423, 54))
        self.verticalLayout_3 = QVBoxLayout(self.sa_error_contents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_error = QLabel(self.sa_error_contents)
        self.label_error.setObjectName("label_error")
        self.label_error.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )

        self.verticalLayout_3.addWidget(self.label_error)

        self.sa_error.setWidget(self.sa_error_contents)

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.sa_error)

        self.sa_traceback = QScrollArea(self.frame_info)
        self.sa_traceback.setObjectName("sa_traceback")
        self.sa_traceback.setWidgetResizable(True)
        self.sa_traceback_contents = QWidget()
        self.sa_traceback_contents.setObjectName("sa_traceback_contents")
        self.sa_traceback_contents.setGeometry(QRect(0, 0, 423, 54))
        self.verticalLayout_4 = QVBoxLayout(self.sa_traceback_contents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_traceback = QLabel(self.sa_traceback_contents)
        self.label_traceback.setObjectName("label_traceback")
        self.label_traceback.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )

        self.verticalLayout_4.addWidget(self.label_traceback)

        self.sa_traceback.setWidget(self.sa_traceback_contents)

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.sa_traceback)

        self.verticalLayout_2.addWidget(self.frame_info)

        self.label_help_us = QLabel(self.main_widget)
        self.label_help_us.setObjectName("label_help_us")

        self.verticalLayout_2.addWidget(self.label_help_us)

        self.frame_context = QFrame(self.main_widget)
        self.frame_context.setObjectName("frame_context")
        self.frame_context.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_context.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout_2 = QFormLayout(self.frame_context)
        self.formLayout_2.setObjectName("formLayout_2")
        self.l_description = QLabel(self.frame_context)
        self.l_description.setObjectName("l_description")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.l_description)

        self.l_screenshots = QLabel(self.frame_context)
        self.l_screenshots.setObjectName("l_screenshots")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.l_screenshots)

        self.l_empty = QLabel(self.frame_context)
        self.l_empty.setObjectName("l_empty")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.l_empty)

        self.list_screenshots = QListWidget(self.frame_context)
        self.list_screenshots.setObjectName("list_screenshots")
        self.list_screenshots.setMinimumSize(QSize(0, 100))
        self.list_screenshots.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.list_screenshots.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.list_screenshots.setProperty("showDropIndicator", False)
        self.list_screenshots.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.list_screenshots.setDefaultDropAction(Qt.DropAction.IgnoreAction)
        self.list_screenshots.setViewMode(QListView.ViewMode.IconMode)

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.list_screenshots)

        self.frame = QFrame(self.frame_context)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pb_add_screenshot = QPushButton(self.frame)
        self.pb_add_screenshot.setObjectName("pb_add_screenshot")

        self.horizontalLayout_2.addWidget(self.pb_add_screenshot)

        self.pb_remove_screenshot = QPushButton(self.frame)
        self.pb_remove_screenshot.setObjectName("pb_remove_screenshot")

        self.horizontalLayout_2.addWidget(self.pb_remove_screenshot)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.frame)

        self.text_edit_description = QPlainTextEdit(self.frame_context)
        self.text_edit_description.setObjectName("text_edit_description")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.text_edit_description)

        self.verticalLayout_2.addWidget(self.frame_context)

        self.frame_bottom = QFrame(self.main_widget)
        self.frame_bottom.setObjectName("frame_bottom")
        sizePolicy.setHeightForWidth(self.frame_bottom.sizePolicy().hasHeightForWidth())
        self.frame_bottom.setSizePolicy(sizePolicy)
        self.frame_bottom.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_bottom.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_bottom)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.button_open_ticket = QPushButton(self.frame_bottom)
        self.button_open_ticket.setObjectName("button_open_ticket")
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
        helpme_widget.setWindowTitle(QCoreApplication.translate("helpme_widget", "Form", None))
        self.label_title.setText(QCoreApplication.translate("helpme_widget", "HelpMe", None))
        self.label_title.setProperty("tag", QCoreApplication.translate("helpme_widget", "H2", None))
        self.l_name.setText(QCoreApplication.translate("helpme_widget", "Ticket Name", None))
        self.l_file.setText(QCoreApplication.translate("helpme_widget", "File", None))
        self.label_file.setText(QCoreApplication.translate("helpme_widget", "path/to/file", None))
        self.l_asset.setText(QCoreApplication.translate("helpme_widget", "Asset", None))
        self.label_asset.setText(QCoreApplication.translate("helpme_widget", "assetName", None))
        self.l_shot.setText(QCoreApplication.translate("helpme_widget", "Shot", None))
        self.label_shot.setText(QCoreApplication.translate("helpme_widget", "shotId", None))
        self.l_user.setText(QCoreApplication.translate("helpme_widget", "User", None))
        self.l_computer.setText(QCoreApplication.translate("helpme_widget", "Computer", None))
        self.label_user.setText(QCoreApplication.translate("helpme_widget", "user.name", None))
        self.label_computer.setText(QCoreApplication.translate("helpme_widget", "computer.name", None))
        self.l_error.setText(QCoreApplication.translate("helpme_widget", "Error", None))
        self.l_traceback.setText(QCoreApplication.translate("helpme_widget", "Traceback", None))
        self.label_error.setText(QCoreApplication.translate("helpme_widget", "Error", None))
        self.label_error.setProperty("status", QCoreApplication.translate("helpme_widget", "code", None))
        self.label_traceback.setText(QCoreApplication.translate("helpme_widget", "Traceback", None))
        self.label_traceback.setProperty("status", QCoreApplication.translate("helpme_widget", "code", None))
        self.label_help_us.setText(QCoreApplication.translate("helpme_widget", "Help us to help you", None))
        self.label_help_us.setProperty("tag", QCoreApplication.translate("helpme_widget", "H2", None))
        self.l_description.setText(QCoreApplication.translate("helpme_widget", "Description", None))
        self.l_screenshots.setText(QCoreApplication.translate("helpme_widget", "Screenshots", None))
        self.l_empty.setText("")
        self.pb_add_screenshot.setText(QCoreApplication.translate("helpme_widget", "Add Screenshot", None))
        self.pb_add_screenshot.setProperty("status", QCoreApplication.translate("helpme_widget", "important", None))
        self.pb_remove_screenshot.setText(QCoreApplication.translate("helpme_widget", "Remove ScreenShot", None))
        self.pb_remove_screenshot.setProperty("status", QCoreApplication.translate("helpme_widget", "danger", None))
        self.text_edit_description.setPlaceholderText(
            QCoreApplication.translate("helpme_widget", "Hello Support Staff, here is my problem...", None)
        )
        self.button_open_ticket.setText(QCoreApplication.translate("helpme_widget", "Open Ticket", None))
        self.button_open_ticket.setProperty("status", QCoreApplication.translate("helpme_widget", "important", None))

    # retranslateUi
