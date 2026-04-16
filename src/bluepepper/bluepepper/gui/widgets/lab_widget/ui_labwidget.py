# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'labwidgetNSHnhe.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


class Ui_LabWidget(object):
    def setupUi(self, LabWidget):
        if not LabWidget.objectName():
            LabWidget.setObjectName(u"LabWidget")
        LabWidget.resize(840, 664)
        self.verticalLayout = QVBoxLayout(LabWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(LabWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 803, 1391))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setIndent(0)

        self.verticalLayout_2.addWidget(self.label)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_2.addWidget(self.label_5)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_2.addWidget(self.label_6)

        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_2.addWidget(self.label_7)

        self.radioButton = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton.setObjectName(u"radioButton")

        self.verticalLayout_2.addWidget(self.radioButton)

        self.comboBox = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.comboBox)

        self.doubleSpinBox = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        sizePolicy1.setHeightForWidth(self.doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.doubleSpinBox)

        self.spinBox = QSpinBox(self.scrollAreaWidgetContents)
        self.spinBox.setObjectName(u"spinBox")
        sizePolicy1.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy1)
        self.spinBox.setButtonSymbols(QAbstractSpinBox.UpDownArrows)

        self.verticalLayout_2.addWidget(self.spinBox)

        self.lineEdit = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy1.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.lineEdit)

        self.lineEdit_3 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        sizePolicy1.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.lineEdit_3)

        self.lineEdit_2 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        sizePolicy1.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.lineEdit_2)

        self.horizontalSlider = QSlider(self.scrollAreaWidgetContents)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.verticalLayout_2.addWidget(self.horizontalSlider)

        self.pushButton = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy1.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy1)
        self.pushButton.setCheckable(False)

        self.verticalLayout_2.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy1.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy1.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.pushButton_3)

        self.verticalSlider = QSlider(self.scrollAreaWidgetContents)
        self.verticalSlider.setObjectName(u"verticalSlider")
        self.verticalSlider.setMinimumSize(QSize(0, 50))
        self.verticalSlider.setOrientation(Qt.Vertical)

        self.verticalLayout_2.addWidget(self.verticalSlider)

        self.progressBar = QProgressBar(self.scrollAreaWidgetContents)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy1.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy1)
        self.progressBar.setValue(24)

        self.verticalLayout_2.addWidget(self.progressBar)

        self.progressBar_5 = QProgressBar(self.scrollAreaWidgetContents)
        self.progressBar_5.setObjectName(u"progressBar_5")
        sizePolicy1.setHeightForWidth(self.progressBar_5.sizePolicy().hasHeightForWidth())
        self.progressBar_5.setSizePolicy(sizePolicy1)
        self.progressBar_5.setValue(24)

        self.verticalLayout_2.addWidget(self.progressBar_5)

        self.progressBar_4 = QProgressBar(self.scrollAreaWidgetContents)
        self.progressBar_4.setObjectName(u"progressBar_4")
        sizePolicy1.setHeightForWidth(self.progressBar_4.sizePolicy().hasHeightForWidth())
        self.progressBar_4.setSizePolicy(sizePolicy1)
        self.progressBar_4.setValue(24)

        self.verticalLayout_2.addWidget(self.progressBar_4)

        self.progressBar_3 = QProgressBar(self.scrollAreaWidgetContents)
        self.progressBar_3.setObjectName(u"progressBar_3")
        sizePolicy1.setHeightForWidth(self.progressBar_3.sizePolicy().hasHeightForWidth())
        self.progressBar_3.setSizePolicy(sizePolicy1)
        self.progressBar_3.setValue(24)

        self.verticalLayout_2.addWidget(self.progressBar_3)

        self.progressBar_2 = QProgressBar(self.scrollAreaWidgetContents)
        self.progressBar_2.setObjectName(u"progressBar_2")
        sizePolicy1.setHeightForWidth(self.progressBar_2.sizePolicy().hasHeightForWidth())
        self.progressBar_2.setSizePolicy(sizePolicy1)
        self.progressBar_2.setValue(24)

        self.verticalLayout_2.addWidget(self.progressBar_2)

        self.progressBar_6 = QProgressBar(self.scrollAreaWidgetContents)
        self.progressBar_6.setObjectName(u"progressBar_6")
        sizePolicy1.setHeightForWidth(self.progressBar_6.sizePolicy().hasHeightForWidth())
        self.progressBar_6.setSizePolicy(sizePolicy1)
        self.progressBar_6.setValue(24)

        self.verticalLayout_2.addWidget(self.progressBar_6)

        self.checkBox = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout_2.addWidget(self.checkBox)

        self.tableWidget = QTableWidget(self.scrollAreaWidgetContents)
        if (self.tableWidget.columnCount() < 10):
            self.tableWidget.setColumnCount(10)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        if (self.tableWidget.rowCount() < 8):
            self.tableWidget.setRowCount(8)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, __qtablewidgetitem17)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy2)
        self.tableWidget.setMinimumSize(QSize(0, 200))

        self.verticalLayout_2.addWidget(self.tableWidget)

        self.treeWidget = QTreeWidget(self.scrollAreaWidgetContents)
        __qtreewidgetitem = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem1 = QTreeWidgetItem(__qtreewidgetitem)
        __qtreewidgetitem2 = QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem2)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        __qtreewidgetitem3 = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem4 = QTreeWidgetItem(__qtreewidgetitem3)
        QTreeWidgetItem(__qtreewidgetitem4)
        QTreeWidgetItem(__qtreewidgetitem4)
        QTreeWidgetItem(__qtreewidgetitem4)
        QTreeWidgetItem(__qtreewidgetitem3)
        __qtreewidgetitem5 = QTreeWidgetItem(__qtreewidgetitem3)
        QTreeWidgetItem(__qtreewidgetitem5)
        QTreeWidgetItem(self.treeWidget)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setMinimumSize(QSize(0, 200))
        self.treeWidget.setStyleSheet(u"")
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setUniformRowHeights(True)

        self.verticalLayout_2.addWidget(self.treeWidget)

        self.buttonBox = QDialogButtonBox(self.scrollAreaWidgetContents)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)

        self.frame = QFrame(self.scrollAreaWidgetContents)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 200))
        self.frame.setMaximumSize(QSize(16777215, 200))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_10 = QLabel(self.frame)
        self.label_10.setObjectName(u"label_10")
        sizePolicy1.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy1)

        self.verticalLayout_3.addWidget(self.label_10)

        self.label_12 = QLabel(self.frame)
        self.label_12.setObjectName(u"label_12")
        sizePolicy1.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy1)

        self.verticalLayout_3.addWidget(self.label_12)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setProperty("depth", 1)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_11 = QLabel(self.frame_2)
        self.label_11.setObjectName(u"label_11")
        sizePolicy1.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy1)

        self.verticalLayout_4.addWidget(self.label_11)

        self.label_13 = QLabel(self.frame_2)
        self.label_13.setObjectName(u"label_13")
        sizePolicy1.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy1)

        self.verticalLayout_4.addWidget(self.label_13)

        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_14 = QLabel(self.frame_3)
        self.label_14.setObjectName(u"label_14")

        self.verticalLayout_7.addWidget(self.label_14)


        self.verticalLayout_4.addWidget(self.frame_3)


        self.verticalLayout_3.addWidget(self.frame_2)


        self.verticalLayout_2.addWidget(self.frame)

        self.tabWidget = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_5 = QVBoxLayout(self.tab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_8 = QLabel(self.tab)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_5.addWidget(self.label_8)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_6 = QVBoxLayout(self.tab_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_9 = QLabel(self.tab_2)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_6.addWidget(self.label_9)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_8 = QVBoxLayout(self.tab_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_15 = QLabel(self.tab_3)
        self.label_15.setObjectName(u"label_15")

        self.verticalLayout_8.addWidget(self.label_15)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_9 = QVBoxLayout(self.tab_4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_16 = QLabel(self.tab_4)
        self.label_16.setObjectName(u"label_16")

        self.verticalLayout_9.addWidget(self.label_16)

        self.tabWidget.addTab(self.tab_4, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(LabWidget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(LabWidget)
    # setupUi

    def retranslateUi(self, LabWidget):
        LabWidget.setWindowTitle(QCoreApplication.translate("LabWidget", u"Form", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("LabWidget", u"This is a tooltip", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("LabWidget", u"TextLabelH1", None))
        self.label.setProperty("tag", QCoreApplication.translate("LabWidget", u"H1", None))
        self.label_2.setText(QCoreApplication.translate("LabWidget", u"TextLabelH2", None))
        self.label_2.setProperty("tag", QCoreApplication.translate("LabWidget", u"H2", None))
        self.label_3.setText(QCoreApplication.translate("LabWidget", u"TextLabelH3", None))
        self.label_3.setProperty("tag", QCoreApplication.translate("LabWidget", u"H3", None))
        self.label_4.setText(QCoreApplication.translate("LabWidget", u"TextLabelH4", None))
        self.label_4.setProperty("tag", QCoreApplication.translate("LabWidget", u"H4", None))
        self.label_5.setText(QCoreApplication.translate("LabWidget", u"TextLabelH5", None))
        self.label_5.setProperty("tag", QCoreApplication.translate("LabWidget", u"H5", None))
        self.label_6.setText(QCoreApplication.translate("LabWidget", u"TextLabelH6", None))
        self.label_6.setProperty("tag", QCoreApplication.translate("LabWidget", u"H6", None))
        self.label_7.setText(QCoreApplication.translate("LabWidget", u"sometext sometext sometext sometext sometext sometext sometext ", None))
        self.radioButton.setText(QCoreApplication.translate("LabWidget", u"RadioButton", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("LabWidget", u"pomme", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("LabWidget", u"poire", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("LabWidget", u"poulet", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("LabWidget", u"banane", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("LabWidget", u"chasuble", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("LabWidget", u"renault 5", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("LabWidget", u"poubelle", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("LabWidget", u"moisi", None))

        self.lineEdit.setText(QCoreApplication.translate("LabWidget", u"LineEdit", None))
        self.lineEdit_3.setText(QCoreApplication.translate("LabWidget", u"ok", None))
        self.lineEdit_3.setProperty("status", QCoreApplication.translate("LabWidget", u"ok", None))
        self.lineEdit_2.setText(QCoreApplication.translate("LabWidget", u"Error", None))
        self.lineEdit_2.setProperty("status", QCoreApplication.translate("LabWidget", u"error", None))
        self.pushButton.setText(QCoreApplication.translate("LabWidget", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("LabWidget", u"PushButton", None))
        self.pushButton_2.setProperty("status", QCoreApplication.translate("LabWidget", u"important", None))
        self.pushButton_3.setText(QCoreApplication.translate("LabWidget", u"PushButton", None))
        self.pushButton_3.setProperty("status", QCoreApplication.translate("LabWidget", u"danger", None))
        self.progressBar_5.setProperty("status", QCoreApplication.translate("LabWidget", u"in_progress", None))
        self.progressBar_4.setProperty("status", QCoreApplication.translate("LabWidget", u"done", None))
        self.progressBar_3.setProperty("status", QCoreApplication.translate("LabWidget", u"error", None))
        self.progressBar_2.setProperty("status", QCoreApplication.translate("LabWidget", u"stuck", None))
        self.progressBar_6.setProperty("status", QCoreApplication.translate("LabWidget", u"cancelled", None))
        self.checkBox.setText(QCoreApplication.translate("LabWidget", u"CheckBox", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtablewidgetitem8 = self.tableWidget.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtablewidgetitem9 = self.tableWidget.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtablewidgetitem10 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("LabWidget", u"New Row", None));
        ___qtablewidgetitem11 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("LabWidget", u"New Row", None));
        ___qtablewidgetitem12 = self.tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("LabWidget", u"New Row", None));
        ___qtablewidgetitem13 = self.tableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("LabWidget", u"New Row", None));
        ___qtablewidgetitem14 = self.tableWidget.verticalHeaderItem(4)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("LabWidget", u"New Row", None));
        ___qtablewidgetitem15 = self.tableWidget.verticalHeaderItem(5)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("LabWidget", u"New Row", None));
        ___qtablewidgetitem16 = self.tableWidget.verticalHeaderItem(6)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("LabWidget", u"New Row", None));
        ___qtablewidgetitem17 = self.tableWidget.verticalHeaderItem(7)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("LabWidget", u"New Row", None));
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(10, QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtreewidgetitem.setText(9, QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtreewidgetitem.setText(8, QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtreewidgetitem.setText(7, QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtreewidgetitem.setText(6, QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("LabWidget", u"New Column", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("LabWidget", u"1", None));

        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("LabWidget", u"Root Item 1", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("LabWidget", u"Subitem 11", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem2.child(0)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("LabWidget", u"Sub - Sub item 111", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem3.child(0)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("LabWidget", u"Sub - Sub - Sub item 1111", None));
        ___qtreewidgetitem5 = ___qtreewidgetitem2.child(1)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("LabWidget", u"Sub - Sub item 112", None));
        ___qtreewidgetitem6 = ___qtreewidgetitem2.child(2)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("LabWidget", u"Sub - Sub item 113", None));
        ___qtreewidgetitem7 = ___qtreewidgetitem2.child(3)
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("LabWidget", u"Sub - Sub item 114", None));
        ___qtreewidgetitem8 = self.treeWidget.topLevelItem(1)
        ___qtreewidgetitem8.setText(0, QCoreApplication.translate("LabWidget", u"Root Item 2", None));
        ___qtreewidgetitem9 = ___qtreewidgetitem8.child(0)
        ___qtreewidgetitem9.setText(0, QCoreApplication.translate("LabWidget", u"Subitem 21", None));
        ___qtreewidgetitem10 = ___qtreewidgetitem9.child(0)
        ___qtreewidgetitem10.setText(0, QCoreApplication.translate("LabWidget", u"Sub - Sub item 211", None));
        ___qtreewidgetitem11 = ___qtreewidgetitem9.child(1)
        ___qtreewidgetitem11.setText(0, QCoreApplication.translate("LabWidget", u"Sub - Sub item 212", None));
        ___qtreewidgetitem12 = ___qtreewidgetitem9.child(2)
        ___qtreewidgetitem12.setText(0, QCoreApplication.translate("LabWidget", u"Sub - Sub item 213", None));
        ___qtreewidgetitem13 = ___qtreewidgetitem8.child(1)
        ___qtreewidgetitem13.setText(0, QCoreApplication.translate("LabWidget", u"Subitem 22", None));
        ___qtreewidgetitem14 = ___qtreewidgetitem8.child(2)
        ___qtreewidgetitem14.setText(0, QCoreApplication.translate("LabWidget", u"Subitem 23", None));
        ___qtreewidgetitem15 = ___qtreewidgetitem14.child(0)
        ___qtreewidgetitem15.setText(0, QCoreApplication.translate("LabWidget", u"Sub - Sub item 231", None));
        ___qtreewidgetitem16 = self.treeWidget.topLevelItem(2)
        ___qtreewidgetitem16.setText(0, QCoreApplication.translate("LabWidget", u"Root Item 3", None));
        self.treeWidget.setSortingEnabled(__sortingEnabled)

        self.frame.setProperty("depth", QCoreApplication.translate("LabWidget", u"0", None))
        self.label_10.setText(QCoreApplication.translate("LabWidget", u"some text H1", None))
        self.label_10.setProperty("tag", QCoreApplication.translate("LabWidget", u"H1", None))
        self.label_12.setText(QCoreApplication.translate("LabWidget", u"ceci est un text de test ceci est un text de testceci est un text de testceci est un text de testceci est un text de testceci est un text de test", None))
        self.label_11.setText(QCoreApplication.translate("LabWidget", u"some text H2", None))
        self.label_11.setProperty("tag", QCoreApplication.translate("LabWidget", u"H2", None))
        self.label_13.setText(QCoreApplication.translate("LabWidget", u"bla bla bla bla bla bla bla bla bla bla bla bla bla bla ", None))
        self.frame_3.setProperty("depth", QCoreApplication.translate("LabWidget", u"2", None))
        self.label_14.setText(QCoreApplication.translate("LabWidget", u"TextLabel", None))
        self.label_8.setText(QCoreApplication.translate("LabWidget", u"Tab1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("LabWidget", u"Tab 1", None))
        self.label_9.setText(QCoreApplication.translate("LabWidget", u"Tab2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("LabWidget", u"Tab 2", None))
        self.label_15.setText(QCoreApplication.translate("LabWidget", u"tab 3", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("LabWidget", u"Tab 3 yolo yolo yolo", None))
        self.label_16.setText(QCoreApplication.translate("LabWidget", u"TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("LabWidget", u"Some other tab", None))
    # retranslateUi

