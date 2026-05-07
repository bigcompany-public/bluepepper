# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'launcher_widgetKbtjUG.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import QCoreApplication, QMetaObject
from qtpy.QtWidgets import QAbstractItemView, QFrame, QLabel, QListView, QListWidget, QVBoxLayout, QWidget


class Ui_launcher_widget(object):
    def setupUi(self, launcher_widget):
        if not launcher_widget.objectName():
            launcher_widget.setObjectName("launcher_widget")
        launcher_widget.resize(721, 486)
        self.verticalLayout = QVBoxLayout(launcher_widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.main_widget = QWidget(launcher_widget)
        self.main_widget.setObjectName("main_widget")
        self.verticalLayout_2 = QVBoxLayout(self.main_widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_apps = QFrame(self.main_widget)
        self.frame_apps.setObjectName("frame_apps")
        self.frame_apps.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_apps.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_apps)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_apps = QLabel(self.frame_apps)
        self.label_apps.setObjectName("label_apps")

        self.verticalLayout_3.addWidget(self.label_apps)

        self.list_apps = QListWidget(self.frame_apps)
        self.list_apps.setObjectName("list_apps")
        self.list_apps.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.list_apps.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.list_apps.setViewMode(QListView.ViewMode.IconMode)

        self.verticalLayout_3.addWidget(self.list_apps)

        self.verticalLayout_2.addWidget(self.frame_apps)

        self.frame_tools = QFrame(self.main_widget)
        self.frame_tools.setObjectName("frame_tools")
        self.frame_tools.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_tools.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_tools)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_tools = QLabel(self.frame_tools)
        self.label_tools.setObjectName("label_tools")

        self.verticalLayout_4.addWidget(self.label_tools)

        self.list_tools = QListWidget(self.frame_tools)
        self.list_tools.setObjectName("list_tools")

        self.verticalLayout_4.addWidget(self.list_tools)

        self.verticalLayout_2.addWidget(self.frame_tools)

        self.verticalLayout.addWidget(self.main_widget)

        self.retranslateUi(launcher_widget)

        QMetaObject.connectSlotsByName(launcher_widget)

    # setupUi

    def retranslateUi(self, launcher_widget):
        launcher_widget.setWindowTitle(QCoreApplication.translate("launcher_widget", "Form", None))
        self.label_apps.setText(QCoreApplication.translate("launcher_widget", "Apps", None))
        self.label_apps.setProperty("tag", "")
        self.label_tools.setText(QCoreApplication.translate("launcher_widget", "Tools", None))

    # retranslateUi
