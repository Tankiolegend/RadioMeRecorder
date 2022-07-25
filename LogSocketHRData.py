# python3 C:\Python38\Programs\LogSocketHRData.py

#https://pythonprogramming.net/sockets-tutorial-python-3/

import socket
from datetime import date
import os
import csv

LOGPATH =  os.path.dirname(os.path.abspath(__file__))+'/data/WatchLog_'
# create the socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((socket.gethostname(),3579))
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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

	files_path = os.path.join(LOGPATH, (str(date.today())+".csv"))
	files_exists = os.path.exists(files_path)

	if not files_exists:
		with open(files_path, 'w', newline='') as f:
        
			writer = csv.writer(f)
      
			writer.writerow(['Time', 'HR']) 
	
	with open (LOGPATH+str(date.today())+".csv", 'a') as logFile: logFile.write(msg.decode("utf-8")+'\n')
