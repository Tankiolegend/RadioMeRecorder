#import schedule
import os
from PyQt5.QtWidgets import * #(QWidget, QToolTip, QPushButton, QApplication,QDesktopWidget)
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import subprocess
import sys

class the_gui(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Radio Me Watch Log Recorder')

        layout = QGridLayout
        screen_size = QDesktopWidget().screenGeometry(0)
        #self.showMaximized()

        side_margin = 100
        top_margin = 200

        txt = "This is the RadioMe heart rate and stress recorder, push start to begin recording. <br> \
        Once recording has been started keep this window open. Stop recording safely with the stop button. <br> \
        You can leave the computer on and the window open to automatically record everyday once the start button <br>has been pushed until the stop button is used."
        self.description_lbl = QLabel(self)
        self.description_lbl.setText(txt)
        self.description_lbl.setFont(QFont("Arial", 20, QFont.Bold))
        self.description_lbl.move(side_margin, top_margin)

        stress_txt = "Stress: not recording"
        self.stress_lbl = QLabel(self)
        self.stress_lbl.setText(stress_txt)
        self.stress_lbl.setFont(QFont("Arial", 20, QFont.Bold))
        self.stress_lbl.move(side_margin, 400)

        self.start_button = QPushButton("Start", self)
        self.start_button.setFont(QFont("Arial", 38, QFont.Bold))
        self.start_button.move(int(side_margin + self.start_button.width()), int(screen_size.height() - top_margin - self.start_button.height()))
        self.start_button.setStyleSheet("background-color: blue; font-color: black;") #  width: " + str(2*side_margin) + ";")
        self.start_button.clicked.connect(self.start_recording)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setFont(QFont("Arial", 38, QFont.Bold))
        self.stop_button.move(int(screen_size.width() - 2*side_margin - self.stop_button.width()), int(screen_size.height() - top_margin - self.stop_button.height()))
        self.stop_button.setStyleSheet("background-color: gray; font-color: black;") #  width: " + str(2*side_margin) + ";")
        

    def start_recording(self):
        #Starts watch recording
        subprocess.call('start python LogSocketHRData.py', shell=True)

class Controller():


    def __init__(self):
        super(Controller, self).__init__()

    def show_the_gui(self):
        self.the_gui = the_gui()
        self.the_gui.showMaximized()

def main():

    app = QApplication(sys.argv)
    gui = Controller()
    gui.show_the_gui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


