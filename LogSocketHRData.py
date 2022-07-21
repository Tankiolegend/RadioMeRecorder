# python3 C:\Python38\Programs\LogSocketHRData.py

#https://pythonprogramming.net/sockets-tutorial-python-3/

import socket
from datetime import date
import os

LOGPATH =  os.path.dirname(os.path.abspath(__file__))+'/data/WatchLog_'
# create the socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((socket.gethostname(),3579))
s.bind(("192.168.137.1",3579))
#192.168.137.1
hostname = socket.gethostname()
#Comnputername
#print(hostname)
#IP Address
print(socket.gethostbyname(hostname))
s.listen(5)

while True:
	clientsocket, address = s.accept()
	msg = clientsocket.recv(1024)
	print(msg.decode("utf-8"))
	with open (LOGPATH+str(date.today())+".csv", 'a') as logFile: logFile.write(msg.decode("utf-8")+'\n')