# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_setting(object):
    def setupUi(self, setting):
        setting.setObjectName("setting")
        setting.resize(319, 354)
        self.groupBox = QtWidgets.QGroupBox(setting)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 271, 81))
        self.groupBox.setObjectName("groupBox")
        self.webcomBox = QtWidgets.QComboBox(self.groupBox)
        self.webcomBox.setGeometry(QtCore.QRect(100, 30, 121, 22))
        self.webcomBox.setObjectName("webcomBox")
        self.webcomBox.addItem("")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 30, 54, 21))
        self.label.setObjectName("label")
        self.groupBox_2 = QtWidgets.QGroupBox(setting)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 100, 271, 211))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(30, 110, 54, 21))
        self.label_3.setObjectName("label_3")
        self.ipLine = QtWidgets.QLineEdit(self.groupBox_2)
        self.ipLine.setGeometry(QtCore.QRect(100, 30, 113, 20))
        self.ipLine.setObjectName("ipLine")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(30, 150, 41, 21))
        self.label_4.setObjectName("label_4")
        self.portLine = QtWidgets.QLineEdit(self.groupBox_2)
        self.portLine.setGeometry(QtCore.QRect(100, 70, 113, 20))
        self.portLine.setObjectName("portLine")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(30, 30, 41, 16))
        self.label_2.setObjectName("label_2")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(30, 70, 31, 16))
        self.label_5.setObjectName("label_5")
        self.dbLine = QtWidgets.QLineEdit(self.groupBox_2)
        self.dbLine.setGeometry(QtCore.QRect(100, 110, 113, 20))
        self.dbLine.setObjectName("dbLine")
        self.collLine = QtWidgets.QLineEdit(self.groupBox_2)
        self.collLine.setGeometry(QtCore.QRect(100, 150, 113, 20))
        self.collLine.setObjectName("collLine")
        self.OkButton = QtWidgets.QPushButton(setting)
        self.OkButton.setGeometry(QtCore.QRect(130, 320, 75, 23))
        self.OkButton.setObjectName("OkButton")
        self.CancelButton = QtWidgets.QPushButton(setting)
        self.CancelButton.setGeometry(QtCore.QRect(220, 320, 75, 23))
        self.CancelButton.setObjectName("CancelButton")

        self.retranslateUi(setting)
        QtCore.QMetaObject.connectSlotsByName(setting)

    def retranslateUi(self, setting):
        _translate = QtCore.QCoreApplication.translate
        setting.setWindowTitle(_translate("setting", "设置"))
        self.groupBox.setTitle(_translate("setting", "爬虫"))
        self.webcomBox.setItemText(0, _translate("setting", "www.jb39.com"))
        self.label.setText(_translate("setting", "爬取网站"))
        self.groupBox_2.setTitle(_translate("setting", "数据库"))
        self.label_3.setText(_translate("setting", "数据库名"))
        self.ipLine.setText(_translate("setting", "127.0.0.1"))
        self.label_4.setText(_translate("setting", "集合名"))
        self.portLine.setText(_translate("setting", "27017"))
        self.label_2.setText(_translate("setting", "IP地址"))
        self.label_5.setText(_translate("setting", "端口"))
        self.dbLine.setText(_translate("setting", "test"))
        self.collLine.setText(_translate("setting", "coll"))
        self.OkButton.setText(_translate("setting", "确定"))
        self.CancelButton.setText(_translate("setting", "取消"))

