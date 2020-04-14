from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
import MainCode as MC


class Worker(QRunnable):

    @pyqtSlot()
    def run(self):
        print("Thread start")

        MC.StartKinect()
        MC.disconnectStatus = 0

        print("Thread complete")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        # Worker thread setup
        self.threadpool = QThreadPool()
        print("Multi-Threading with maximum %d threads" % self.threadpool.maxThreadCount())

        # GUI Design Code Goes here:
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

        # Self Design Editions
        self.conButton.setEnabled(True)
        self.disButton.setEnabled(False)

        #### Signal Connection ####
        self.conButton.pressed.connect(self.connectKinect)
        self.disButton.pressed.connect(self.disconnectKinect)

        ###########################

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        # Also add design code here
        MainWindow.setWindowTitle(_translate("MainWindow", "Kinect GUI v1"))
        self.conButton.setText(_translate("MainWindow", "Connect"))
        self.disButton.setText(_translate("MainWindow", "Disconnect"))

    def connectKinect(self):
        # Worker thread handles Kinect Code
        worker = Worker()
        self.threadpool.start(worker)
        self.conButton.setEnabled(False)
        self.disButton.setEnabled(True)

    def disconnectKinect(self):
        print("Disconnected")
        self.conButton.setEnabled(True)
        self.disButton.setEnabled(False)
        MC.disconnectStatus = 1


# GUI Execution:
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
