# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 14:02:34 2018

@author: shuqi
"""

"""
if you want change some parameters,
change the values below, and
run this script before running the main script 

"""

import json
def write_json():
    configs = {
            'ip': '192.168.43.100', # ip address of the server 
            'port': 6666, # port of the server
            'plate_color': [40/225, 140/255, 200/255], # predefined plate color (rgb, (0, 1)) 
            'plate_size': 20,  # predefined plate size (cm)
            'debug': False,  # if debug: show some mid-result images using matplotlib on the devide
            'showing': True, # if show: send some data to the remote server and show them on the server
            'food_thre': 0.25, # threshold for food region
            'background_thre': 0.2 # threshold for background
                }
    with open("configs.json","w") as f:
        json.dump(configs, f)
    
write_json()

with open("configs.json",'r') as f:
    configs = json.load(f)
print(configs['ip'])