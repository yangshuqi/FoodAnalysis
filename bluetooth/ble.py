from bluepy import btle
from bluepy.btle import DefaultDelegate
import time
import datetime
import sqlite3
import threading
import os
import pygatt
import bluetooth
import pexpect
from signal import pause
from gpiozero import Button
from aiy.pins import BUTTON_GPIO_PIN

class NotifyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleNotification(self,cHandle,data):
        print("notify from "+str(cHandle)+str(data)+"\n")


def dev_piezo(Series_Id,Id):
	for ser in dev_0.getServices():
		for chara in ser.getCharacteristics():

			if(chara.supportsRead()):
				if(chara.getHandle()==14):
					while(True):
						test=chara.read()
						print(test[0:len(test)-1])
						now_time=datetime.datetime.now()
						print(str(now_time))
						print(Series_Id)
						Sensor_Id=1
                        cur.execute("INSERT INTO Events(Id,Time,Value,Sensor_Id,Series_Id) VALUES(?,?,?,?,?);",(Id,str(now_time),value,Sensor_Id,Series_Id))
						conn.commit()
						break
			break	
		break		

def dev_accel(Series_Id,Id):
	for ser in dev_1.getServices():
		for chara in ser.getCharacteristics():
			if(chara.supportsRead()):
				if(chara.getHandle()==14):
					while(True):
						test=chara.read()
						print(test[0:len(test)-1])
						now_time=datetime.datetime.now()
						print(str(now_time))
						print(Series_Id)
						Sensor_Id=2
						cur.execute("INSERT INTO Events(Id,Time,Value,Sensor_Id,Series_Id) VALUES(?,?,?,?,?);",(Id,str(now_time),value,Sensor_Id,Series_Id))
						conn.commit()
						break
			break
		break				

def get_sensor_data(Series_Id,Start_Time,Id):
	button=Button(BUTTON_GPIO_PIN)
	dev_0=btle.Peripheral("EC:9E:B0:C2:9F:B3","random").withDelegate(NotifyDelegate())
	time.sleep(3)
	dev_1=btle.Peripheral("D8:47:8F:00:48:CE","random").withDelegate(NotifyDelegate())
	time.sleep(3)
	conn=sqlite3.connect("/home/pi/sensordata.db")
	cur=conn.cursor()
	End_Time=datatime.datetime.now()
	while(True):
		dev_piezo(Series_Id,Id)
		dev_accel(Series_Id,Id)
		if button.is_pressed:
                    return "123"
	cur.execute("INSERT INTO Series_Events VALUES(?,?,?)",(Series_Id,Start_Time,End_Time))
	cur.close()
	conn.close()

#test the bluetooth
button=Button(BUTTON_GPIO_PIN)
dev_0=btle.Peripheral("EC:9E:B0:C2:9F:B3","random").withDelegate(NotifyDelegate())
time.sleep(0.5)
dev_1=btle.Peripheral("D8:47:8F:00:48:CE","random").withDelegate(NotifyDelegate())
time.sleep(0.5)
conn=sqlite3.connect("/home/pi/sensordata.db")
cur=conn.cursor()
while(True):
	dev_piezo(0,0)
	dev_accel(1,0)
	if button.is_pressed:
		pause()