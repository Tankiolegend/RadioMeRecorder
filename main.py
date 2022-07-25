from datetime import datetime, date
import time
import schedule
import os
from PyQt5.QtWidgets import * #(QWidget, QToolTip, QPushButton, QApplication,QDesktopWidget)
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import subprocess
import sys
import numpy as np
import pickle
import pandas as pd
import csv

class the_gui(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Radio Me Watch Log Recorder')
        path = os.path.dirname(os.path.abspath(__file__))+'/data'
        if not os.path.exists(path):
            os.mkdir(path)

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

        stress_txt = "Stress: not started recording"
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
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setEnabled(True)
        self.date_to_use = date.today()

    def start_recording(self):

        self.start_button.setStyleSheet("background-color: gray; font-color: black;")
        self.start_button.setEnabled(False)
        self.stop_button.setStyleSheet("background-color: blue; font-color: black;")
        self.stop_button.setEnabled(True)
        #Starts watch recording
        self.p = subprocess.Popen('python LogSocketHRData.py')
        #subprocess.call('start python LogSocketHRData.py', shell=True)
        self.timer = QTimer()
        self.timeout = 120000
        self.timer.timeout.connect(self.tick)

        self.timer.setInterval(100)
        self.tick()
        self.timer.start()

    def tick(self):
        self.timeout -= 100
        if date.today() != self.date_to_use:

            self.timeout = 120000
            self.date_to_use = date.today()

        if self.timeout <= 0:
            self.timeout = 10000
            self.run_ml_Alg()

    def stop_recording(self):
        self.stop_button.setStyleSheet("background-color: gray; font-color: black;")
        self.stop_button.setEnabled(False)
        self.start_button.setStyleSheet("background-color: blue; font-color: black;")
        self.start_button.setEnabled(True)
        self.p.kill()
        self.timer.stop()

    def run_ml_Alg(self):
        path = os.path.dirname(os.path.abspath(__file__))+'/data/'
        LOGPATH = path + 'WatchLog_' +str(self.date_to_use)
        print("running ml")
        HR = pd.read_csv(LOGPATH+'.csv')['HR']
        HR = HR[-60:]
        HR_feature = pd.DataFrame(index=range(1), columns=['Std','Range_99','Std_diff'])
        HR_feature['Std'][0] = np.nanstd(HR)
        HR_feature['Std_diff'][0] = np.nanstd(abs(np.diff(HR)))
        Q25 = np.nanquantile(HR,0.25); Q75 = np.nanquantile(HR,0.75); IQR = Q75-Q25;
        HR[HR < Q25-3*IQR] = float("nan"); HR[HR > Q75+3*IQR] = float("nan")
        HR_feature['Range_99'][0] = np.nanquantile(HR,0.99) - np.nanquantile(HR,0.01)

        file     = open('one-minute_model.pkl', 'rb')
        LR_model = pickle.load(file)
        scaler   = pickle.load(file)

        X_scaled = scaler.transform(HR_feature)
        Y_pred   = LR_model.predict(X_scaled)
        prediction = [time.strftime("%Y/%m/%d-%H:%M:%S"), Y_pred[0]]

        with open(path+'_Stress.csv', 'a', newline='') as f:
        
            writer = csv.writer(f)
        
            writer.writerow(prediction)

        if Y_pred[0] == 1:
            stress_txt = "Stress: Participant stressed"
        else:
            stress_txt = "Stress: Participant is not stressed"
        
        self.stress_lbl.setText(stress_txt)


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


