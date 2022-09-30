import sys
import serial
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from clock_setting import *
from thread_func import TimeHandler, STM_Board_Ports


class Clock(QMainWindow, Ui_Form):

    def __init__(self):
        super(Clock, self).__init__()
        self.setupUi(self)
        self.buttonHourUp.clicked.connect(self.press_hour_up)
        self.buttonHourDown.clicked.connect(self.press_hour_down)
        self.buttonMinuteUp.clicked.connect(self.press_minute_up)
        self.buttonMinuteDown.clicked.connect(self.press_minute_down)
        self.buttonSecondUp.clicked.connect(self.press_second_up)
        self.buttonSecondDown.clicked.connect(self.press_second_down)
        self.buttonConnect.clicked.connect(self.connect)
        self.tmh = TimeHandler(self)
        self.ports = STM_Board_Ports(self)
        self.start_prin_time_now()
        self.get_ports()

    def start_prin_time_now(self):
        self.tmh.signal.connect(self.print_time_now)
        self.tmh.start()

    @pyqtSlot(str)
    def print_time_now(self, t):
        self.timeDisplay.setPlaceholderText(t)

    def get_ports(self):
        self.ports.signal.connect(self.set_ports)
        self.ports.start()

    @pyqtSlot(list)
    def set_ports(self, ports):
        if len(ports) > 0:
            self.comPortBox.addItems(ports)
            self.buttonConnect.setEnabled(True)
            self.buttonAply.setEnabled(True)

    def closeEvent(self, event):
        self.tmh.signal.disconnect()
        self.ports.signal.disconnect()

    def connect(self):
        self.buttonConnect.setDisabled(True)
        self.comPortBox.setDisabled(True)
        com = serial.Serial(self.comPortBox.currentText())
        self.tmh.signal.disconnect()
        self.timeDisplay.setPlaceholderText(com.read(8).decode())
        com.close()

    def press_hour_up(self):
        self.timeDisplay.clear()
        self.timeDisplay.setPlaceholderText("H Up")

    def press_hour_down(self):
        self.timeDisplay.clear()
        self.timeDisplay.setPlaceholderText("H Down")

    def press_minute_up(self):
        self.timeDisplay.clear()
        self.timeDisplay.setPlaceholderText("M Up")

    def press_minute_down(self):
        self.timeDisplay.clear()
        self.timeDisplay.setPlaceholderText("M Down")

    def press_second_up(self):
        self.timeDisplay.clear()
        self.timeDisplay.setPlaceholderText("S Up")

    def press_second_down(self):
        self.timeDisplay.clear()
        self.timeDisplay.setPlaceholderText("S Down")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = Clock()
    myapp.show()
    sys.exit(app.exec_())