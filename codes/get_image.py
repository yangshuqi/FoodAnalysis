# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 17:40:01 2018

@author: shuqi
"""


import requests
import os
import time

def get_image(file_name):
	 os.system('sudo ./switchwifi_eyeglasses')
	 time.sleep(10)
	 image_url = 'http://192.168.10.1/media/?action=snapshot'
	 r=requests.get(image_url, auth=('admin', ''))
	 img = r.content
	 with open(file_name,"wb") as f:
	 	 f.write(img)       
	 os.system('sudo ./switchwifi_original')
	 time.sleep(10)
	 
if __name__ == '__main__':
    get_image('test.jpg')