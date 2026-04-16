# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'demo_widgetIoyXuZ.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import QCoreApplication, QMetaObject
from qtpy.QtWidgets import QCheckBox, QFrame, QLabel, QPushButton, QSizePolicy, QVBoxLayout


class Ui_demo(object):
    def setupUi(self, demo):
        if not demo.objectName():
            demo.setObjectName("demo")
        demo.resize(400, 300)
        self.verticalLayout = QVBoxLayout(demo)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(demo)
        self.label.setObjectName("label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.label)

        self.frame = QFrame(demo)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName("label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName("label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.pushButton_2 = QPushButton(self.frame)
        self.pushButton_2.setObjectName("pushButton_2")

        self.verticalLayout_2.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName("pushButton")

        self.verticalLayout_2.addWidget(self.pushButton)

        self.verticalLayout.addWidget(self.frame)

        self.checkBox = QCheckBox(demo)
        self.checkBox.setObjectName("checkBox")

        self.verticalLayout.addWidget(self.checkBox)

        self.retranslateUi(demo)

        QMetaObject.connectSlotsByName(demo)

    # setupUi

    def retranslateUi(self, demo):
        demo.setWindowTitle(QCoreApplication.translate("demo", "Form", None))
        self.label.setText(QCoreApplication.translate("demo", "H1 Text", None))
        self.label.setProperty("tag", QCoreApplication.translate("demo", "H1", None))
        self.frame.setProperty("depth", QCoreApplication.translate("demo", "0", None))
        self.label_2.setText(QCoreApplication.translate("demo", "H2 Text", None))
        self.label_2.setProperty("tag", QCoreApplication.translate("demo", "H2", None))
        self.label_3.setText(QCoreApplication.translate("demo", "normal text", None))
        self.pushButton_2.setText(QCoreApplication.translate("demo", "NormalButton", None))
        self.pushButton.setText(QCoreApplication.translate("demo", "ImportantButton", None))
        self.pushButton.setProperty("status", QCoreApplication.translate("demo", "important", None))
        self.checkBox.setText(QCoreApplication.translate("demo", "CheckBox", None))

    # retranslateUi
