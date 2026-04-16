# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'error_widgetxFMlwW.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import QCoreApplication, QLocale, QMetaObject, QRect, QSize, Qt
from qtpy.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_error_widget(object):
    def setupUi(self, error_widget):
        if not error_widget.objectName():
            error_widget.setObjectName("error_widget")
        error_widget.resize(565, 395)
        self.verticalLayout = QVBoxLayout(error_widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.main_widget = QWidget(error_widget)
        self.main_widget.setObjectName("main_widget")
        self.verticalLayout_2 = QVBoxLayout(self.main_widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.top_widget = QWidget(self.main_widget)
        self.top_widget.setObjectName("top_widget")
        self.top_widget_layout = QHBoxLayout(self.top_widget)
        self.top_widget_layout.setObjectName("top_widget_layout")
        self.top_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(self.top_widget)
        self.label_title.setObjectName("label_title")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy)

        self.top_widget_layout.addWidget(self.label_title)

        self.horizontalSpacer_2 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.top_widget_layout.addItem(self.horizontalSpacer_2)

        self.verticalLayout_2.addWidget(self.top_widget)

        self.frame_error = QFrame(self.main_widget)
        self.frame_error.setObjectName("frame_error")
        self.frame_error.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_error.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_error)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.sa_error = QScrollArea(self.frame_error)
        self.sa_error.setObjectName("sa_error")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sa_error.sizePolicy().hasHeightForWidth())
        self.sa_error.setSizePolicy(sizePolicy1)
        self.sa_error.setWidgetResizable(True)
        self.sa_error_contents = QWidget()
        self.sa_error_contents.setObjectName("sa_error_contents")
        self.sa_error_contents.setGeometry(QRect(0, 0, 521, 54))
        self.verticalLayout_6 = QVBoxLayout(self.sa_error_contents)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_error = QLabel(self.sa_error_contents)
        self.label_error.setObjectName("label_error")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_error.sizePolicy().hasHeightForWidth())
        self.label_error.setSizePolicy(sizePolicy2)
        self.label_error.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )
        self.label_error.setTextInteractionFlags(
            Qt.TextInteractionFlag.LinksAccessibleByMouse
            | Qt.TextInteractionFlag.TextSelectableByKeyboard
            | Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.verticalLayout_6.addWidget(self.label_error)

        self.sa_error.setWidget(self.sa_error_contents)

        self.verticalLayout_5.addWidget(self.sa_error)

        self.verticalLayout_2.addWidget(self.frame_error)

        self.label_traceback_section = QLabel(self.main_widget)
        self.label_traceback_section.setObjectName("label_traceback_section")

        self.verticalLayout_2.addWidget(self.label_traceback_section)

        self.frame_traceback = QFrame(self.main_widget)
        self.frame_traceback.setObjectName("frame_traceback")
        self.frame_traceback.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_traceback.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_traceback)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.sa_traceback = QScrollArea(self.frame_traceback)
        self.sa_traceback.setObjectName("sa_traceback")
        self.sa_traceback.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.sa_traceback.setWidgetResizable(True)
        self.sa_traceback_contents = QWidget()
        self.sa_traceback_contents.setObjectName("sa_traceback_contents")
        self.sa_traceback_contents.setGeometry(QRect(0, 0, 521, 185))
        self.sa_traceback_contents.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout_4 = QVBoxLayout(self.sa_traceback_contents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_traceback = QLabel(self.sa_traceback_contents)
        self.label_traceback.setObjectName("label_traceback")
        self.label_traceback.setScaledContents(True)
        self.label_traceback.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )
        self.label_traceback.setWordWrap(True)
        self.label_traceback.setTextInteractionFlags(
            Qt.TextInteractionFlag.LinksAccessibleByMouse
            | Qt.TextInteractionFlag.TextSelectableByKeyboard
            | Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.verticalLayout_4.addWidget(self.label_traceback)

        self.sa_traceback.setWidget(self.sa_traceback_contents)

        self.verticalLayout_3.addWidget(self.sa_traceback)

        self.verticalLayout_2.addWidget(self.frame_traceback)

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

        self.button_copy = QPushButton(self.frame_bottom)
        self.button_copy.setObjectName("button_copy")

        self.horizontalLayout.addWidget(self.button_copy)

        self.button_ok = QPushButton(self.frame_bottom)
        self.button_ok.setObjectName("button_ok")
        self.button_ok.setMinimumSize(QSize(80, 0))
        self.button_ok.setAutoDefault(True)

        self.horizontalLayout.addWidget(self.button_ok)

        self.verticalLayout_2.addWidget(self.frame_bottom)

        self.verticalLayout.addWidget(self.main_widget)

        self.retranslateUi(error_widget)

        self.button_ok.setDefault(True)

        QMetaObject.connectSlotsByName(error_widget)

    # setupUi

    def retranslateUi(self, error_widget):
        error_widget.setWindowTitle(QCoreApplication.translate("error_widget", "Form", None))
        self.label_title.setText(QCoreApplication.translate("error_widget", "Error", None))
        self.label_title.setProperty("tag", QCoreApplication.translate("error_widget", "H2", None))
        self.label_error.setText(QCoreApplication.translate("error_widget", "Error", None))
        self.label_error.setProperty("status", QCoreApplication.translate("error_widget", "code", None))
        self.label_traceback_section.setText(QCoreApplication.translate("error_widget", "Traceback", None))
        self.label_traceback_section.setProperty("tag", QCoreApplication.translate("error_widget", "H2", None))
        self.label_traceback.setText(QCoreApplication.translate("error_widget", "No traceback available", None))
        self.label_traceback.setProperty("status", QCoreApplication.translate("error_widget", "code", None))
        self.button_copy.setText(QCoreApplication.translate("error_widget", "Copy Traceback", None))
        self.button_ok.setText(QCoreApplication.translate("error_widget", "Ok", None))
        self.button_ok.setProperty("status", QCoreApplication.translate("error_widget", "important", None))

    # retranslateUi
