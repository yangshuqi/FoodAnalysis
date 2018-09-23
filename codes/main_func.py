# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 19:52:23 2018

@author: shuqi
"""

import datetime
from gpiozero import Button
from aiy.pins import BUTTON_GPIO_PIN
from get_image import *
from image_process_main import *

def main_func():
    print("begins")
    file_name = str(datetime.datetime.now()) + '.jpg'
    get_image(file_name)
	
    # file_name = '000.jpg'
	
    image_process_main(file_name, True)


button=Button(BUTTON_GPIO_PIN)

flag = True
while True:
    if button.is_pressed:
        if flag:
            main_func()
            flag = False
        else:
            flag = True

#print("12")   
#button = Button(BUTTON_GPIO_PIN)
#button.when_pressed = main_func
# main_func()