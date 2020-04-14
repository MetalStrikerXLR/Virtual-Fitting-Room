# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Projects\Python\fyp-virtual-dressing-room\GUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 648)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.imageDisplay = QtWidgets.QLabel(self.centralwidget)
        self.imageDisplay.setText("")
        self.imageDisplay.setPixmap(QtGui.QPixmap("killua.jpg"))
        self.imageDisplay.setScaledContents(True)
        self.imageDisplay.setObjectName("imageDisplay")
        self.verticalLayout.addWidget(self.imageDisplay)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.conButton = QtWidgets.QPushButton(self.centralwidget)
        self.conButton.setObjectName("conButton")
        self.horizontalLayout.addWidget(self.conButton)
        self.disButton = QtWidgets.QPushButton(self.centralwidget)
        self.disButton.setObjectName("disButton")
        self.horizontalLayout.addWidget(self.disButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Kinect GUI v1"))
        self.conButton.setText(_translate("MainWindow", "Connect"))
        self.disButton.setText(_translate("MainWindow", "Disconnect"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
