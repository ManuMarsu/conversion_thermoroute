# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\manuel.collongues\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\cvthermo\CVThermo_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CVThermoDialogBase(object):
    def setupUi(self, CVThermoDialogBase):
        CVThermoDialogBase.setObjectName("CVThermoDialogBase")
        CVThermoDialogBase.resize(594, 170)
        self.button_box = QtWidgets.QDialogButtonBox(CVThermoDialogBase)
        self.button_box.setGeometry(QtCore.QRect(170, 100, 341, 32))
        self.button_box.setLocale(QtCore.QLocale(QtCore.QLocale.French, QtCore.QLocale.France))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.button_box.setObjectName("button_box")
        self.line_fichier_re0 = QtWidgets.QLineEdit(CVThermoDialogBase)
        self.line_fichier_re0.setGeometry(QtCore.QRect(150, 50, 271, 20))
        self.line_fichier_re0.setObjectName("line_fichier_re0")
        self.label = QtWidgets.QLabel(CVThermoDialogBase)
        self.label.setGeometry(QtCore.QRect(30, 50, 121, 16))
        self.label.setObjectName("label")
        self.pushButton_convertir = QtWidgets.QPushButton(CVThermoDialogBase)
        self.pushButton_convertir.setGeometry(QtCore.QRect(440, 50, 75, 23))
        self.pushButton_convertir.setObjectName("pushButton_convertir")

        self.retranslateUi(CVThermoDialogBase)
        self.button_box.accepted.connect(CVThermoDialogBase.accept)
        self.button_box.rejected.connect(CVThermoDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(CVThermoDialogBase)

    def retranslateUi(self, CVThermoDialogBase):
        _translate = QtCore.QCoreApplication.translate
        CVThermoDialogBase.setWindowTitle(_translate("CVThermoDialogBase", "Conversion thermoroute"))
        self.label.setText(_translate("CVThermoDialogBase", "Sélectionner fichier re0"))
        self.pushButton_convertir.setText(_translate("CVThermoDialogBase", "..."))