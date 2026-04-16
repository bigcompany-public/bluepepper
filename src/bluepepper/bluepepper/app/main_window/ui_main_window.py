# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowGVsypA.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


class Ui_bluepepper_app_widget(object):
    def setupUi(self, bluepepper_app_widget):
        if not bluepepper_app_widget.objectName():
            bluepepper_app_widget.setObjectName("bluepepper_app_widget")
        bluepepper_app_widget.resize(1113, 830)
        self.verticalLayout = QVBoxLayout(bluepepper_app_widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_topbar = QFrame(bluepepper_app_widget)
        self.frame_topbar.setObjectName("frame_topbar")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_topbar.sizePolicy().hasHeightForWidth())
        self.frame_topbar.setSizePolicy(sizePolicy)
        self.frame_topbar.setFrameShape(QFrame.StyledPanel)
        self.frame_topbar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_topbar)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.frame_topbar)
        self.frame_3.setObjectName("frame_3")
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QSize(0, 0))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_3)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.frame_3)
        self.frame.setObjectName("frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(0, 0))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_2 = QSpacerItem(
            10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.label_main_title = QLabel(self.frame)
        self.label_main_title.setObjectName("label_main_title")
        self.label_main_title.setAlignment(
            Qt.AlignBottom | Qt.AlignLeading | Qt.AlignLeft
        )

        self.horizontalLayout_2.addWidget(self.label_main_title)

        self.horizontalSpacer_4 = QSpacerItem(
            10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.label_important_content = QLabel(self.frame)
        self.label_important_content.setObjectName("label_important_content")
        self.label_important_content.setAlignment(
            Qt.AlignBottom | Qt.AlignLeading | Qt.AlignLeft
        )
        self.label_important_content.setMargin(2)

        self.horizontalLayout_2.addWidget(self.label_important_content)

        self.horizontalSpacer = QSpacerItem(
            10, 5, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.label_version = QLabel(self.frame)
        self.label_version.setObjectName("label_version")
        self.label_version.setAlignment(Qt.AlignBottom | Qt.AlignLeading | Qt.AlignLeft)

        self.horizontalLayout_2.addWidget(self.label_version)

        self.verticalLayout_7.addWidget(self.frame)

        self.verticalSpacer = QSpacerItem(20, 3, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.horizontalLayout.addWidget(self.frame_3)

        self.frame_2 = QFrame(self.frame_topbar)
        self.frame_2.setObjectName("frame_2")
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pb_minimize = QPushButton(self.frame_2)
        self.pb_minimize.setObjectName("pb_minimize")
        self.pb_minimize.setMinimumSize(QSize(27, 27))
        self.pb_minimize.setMaximumSize(QSize(27, 27))

        self.horizontalLayout_4.addWidget(self.pb_minimize)

        self.pb_maximize = QPushButton(self.frame_2)
        self.pb_maximize.setObjectName("pb_maximize")
        self.pb_maximize.setMinimumSize(QSize(27, 27))
        self.pb_maximize.setMaximumSize(QSize(27, 27))

        self.horizontalLayout_4.addWidget(self.pb_maximize)

        self.pb_close = QPushButton(self.frame_2)
        self.pb_close.setObjectName("pb_close")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pb_close.sizePolicy().hasHeightForWidth())
        self.pb_close.setSizePolicy(sizePolicy1)
        self.pb_close.setMinimumSize(QSize(27, 27))
        self.pb_close.setMaximumSize(QSize(27, 27))

        self.horizontalLayout_4.addWidget(self.pb_close)

        self.horizontalLayout.addWidget(self.frame_2)

        self.verticalLayout.addWidget(self.frame_topbar)

        self.widget_main = QWidget(bluepepper_app_widget)
        self.widget_main.setObjectName("widget_main")
        self.verticalLayout_2 = QVBoxLayout(self.widget_main)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_middle = QFrame(self.widget_main)
        self.frame_middle.setObjectName("frame_middle")
        self.frame_middle.setFrameShape(QFrame.StyledPanel)
        self.frame_middle.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_middle)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_leftbar = QFrame(self.frame_middle)
        self.frame_leftbar.setObjectName("frame_leftbar")
        self.frame_leftbar.setFrameShape(QFrame.StyledPanel)
        self.frame_leftbar.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_leftbar)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_apps = QFrame(self.frame_leftbar)
        self.frame_apps.setObjectName("frame_apps")
        self.frame_apps.setFrameShape(QFrame.StyledPanel)
        self.frame_apps.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_apps)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.spacer_apps = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_5.addItem(self.spacer_apps)

        self.verticalLayout_3.addWidget(self.frame_apps)

        self.frame_settings = QFrame(self.frame_leftbar)
        self.frame_settings.setObjectName("frame_settings")
        sizePolicy.setHeightForWidth(
            self.frame_settings.sizePolicy().hasHeightForWidth()
        )
        self.frame_settings.setSizePolicy(sizePolicy)
        self.frame_settings.setMinimumSize(QSize(20, 50))
        self.frame_settings.setFrameShape(QFrame.StyledPanel)
        self.frame_settings.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_settings)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.spacer_settings = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_6.addItem(self.spacer_settings)

        self.verticalLayout_3.addWidget(self.frame_settings)

        self.horizontalLayout_3.addWidget(self.frame_leftbar)

        self.frame_app = QFrame(self.frame_middle)
        self.frame_app.setObjectName("frame_app")
        self.frame_app.setFrameShape(QFrame.StyledPanel)
        self.frame_app.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_app)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.frame_app)
        self.stackedWidget.setObjectName("stackedWidget")

        self.verticalLayout_4.addWidget(self.stackedWidget)

        self.horizontalLayout_3.addWidget(self.frame_app)

        self.verticalLayout_2.addWidget(self.frame_middle)

        self.verticalLayout.addWidget(self.widget_main)

        self.retranslateUi(bluepepper_app_widget)

        QMetaObject.connectSlotsByName(bluepepper_app_widget)

    # setupUi

    def retranslateUi(self, bluepepper_app_widget):
        bluepepper_app_widget.setWindowTitle(
            QCoreApplication.translate("bluepepper_app_widget", "Form", None)
        )
        self.frame_topbar.setProperty(
            "tag", QCoreApplication.translate("bluepepper_app_widget", "topbar", None)
        )
        self.label_main_title.setText(
            QCoreApplication.translate("bluepepper_app_widget", "BluePepper", None)
        )
        self.label_main_title.setProperty(
            "tag", QCoreApplication.translate("bluepepper_app_widget", "H0", None)
        )
        self.label_important_content.setText(
            QCoreApplication.translate(
                "bluepepper_app_widget", "important content", None
            )
        )
        self.label_important_content.setProperty(
            "status",
            QCoreApplication.translate("bluepepper_app_widget", "secondary", None),
        )
        self.label_version.setText(
            QCoreApplication.translate("bluepepper_app_widget", "version", None)
        )
        self.label_version.setProperty(
            "status",
            QCoreApplication.translate("bluepepper_app_widget", "secondary", None),
        )
        self.pb_minimize.setText("")
        self.pb_minimize.setProperty(
            "status",
            QCoreApplication.translate(
                "bluepepper_app_widget", "menu_bar_button", None
            ),
        )
        self.pb_maximize.setText("")
        self.pb_maximize.setProperty(
            "status",
            QCoreApplication.translate(
                "bluepepper_app_widget", "menu_bar_button", None
            ),
        )
        self.pb_close.setText("")
        self.pb_close.setProperty(
            "status",
            QCoreApplication.translate(
                "bluepepper_app_widget", "menu_bar_button_close", None
            ),
        )
        self.widget_main.setProperty(
            "visibility",
            QCoreApplication.translate("bluepepper_app_widget", "transparent", None),
        )
        self.frame_leftbar.setProperty(
            "tag", QCoreApplication.translate("bluepepper_app_widget", "sidebar", None)
        )
        self.frame_app.setProperty(
            "depth", QCoreApplication.translate("bluepepper_app_widget", "-1", None)
        )

    # retranslateUi
