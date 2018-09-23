# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 15:57:10 2018

@author: shuqi
"""

from get_volume_main import *
from socket_service import *
from image_classification import *
from get_food_info import *
import os
import time
import string
import json

def image_process_main(file_path, disp = False):
    category = classify(file_path)
    print(category)
    category = string.capwords(category.replace("_", " "))
    with open("configs.json",'r') as f:
        configs = json.load(f)
    volume = get_volume_main(file_path, configs['plate_color'], configs['plate_size'], 1, debug = configs['debug'], showing = configs['showing'])
    print(volume)
    ip = configs['ip']
    port = configs['port']
    sending_list = 'image;image;info;info;info;'
    image_path = ['original_image.jpg', 'mid_result.jpg']
    info = get_nutrients_data_from_usda(category)
    print(info)
    infos = [category, str(volume)+' cm^3', info]    
    if disp:
        os.system('sudo ./switchwifi_temp')
        time.sleep(60)
        socket_service(ip, port, sending_list, image_path, infos)
    
                    