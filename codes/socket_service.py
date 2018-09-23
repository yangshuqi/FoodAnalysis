#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
file: service.py
socket service
"""


import socket
import threading
import time
import os
import sys
import struct


def socket_service(ip, port, sending_list, image_path, infos):
    print('???')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        time.sleep(1)
    except socket.error as msg:
        print (msg)
        sys.exit(1)
        
    print ('connected')

    # conn.send('Hi, Welcome to the server!')
    
    s.send(bytes(sending_list, 'utf-8'))
    time.sleep(5)
    img_idx = 0
    info_idx = 0
    sending_list = sending_list.split(';')
    for k in range(0, len(sending_list)):
        print(k)
        if sending_list[k] == 'image':
            filepath = image_path[img_idx]
            img_idx += 1
            if os.path.isfile(filepath):
                print(os.stat(filepath).st_size)
                s.send(bytes(str(os.stat(filepath).st_size), 'utf-8'))
                time.sleep(5)
                print ('filepath: {0}'.format(filepath))
                fp = open(filepath, 'rb')
                flag = 0
                buf_size = 1024
                while True:
                    print(flag)
                    flag += 1
                    data = fp.read(buf_size)
                    if not data:
                        print ('{0} file send over...'.format(filepath))
                        break
                    s.send(data)
                    time.sleep(5)
        if sending_list[k] == 'info':
            info = infos[info_idx]
            info_idx += 1
            s.send(bytes(info, 'utf-8'))
            time.sleep(5)
            
    s.close()




if __name__ == '__main__':
    
    ip = '192.168.43.100'
    port = 6666
    sending_list = 'image;image;info;info;info;'
    image_path = ['original_image.jpg', 'mid_result.jpg']
    info = """The nutrients for ndbno: 45145174 are: 
Energy : 400 kcal
Protein : 0.00 g
Total lipid (fat) : 20.00 g
Carbohydrate, by difference : 50.00 g
Fiber, total dietary : 0.0 g
Sugars, total : 40.00 g
Calcium, Ca : 0 mg
Iron, Fe : 0.00 mg
Sodium, Na : 0 mg
Vitamin C, total ascorbic acid : 0.0 mg
Vitamin A, IU : 0 IU
Fatty acids, total saturated : 10.000 g
Fatty acids, total trans : 0.000 g
Cholesterol : 50 mg
"""
    infos = ['food_type', '200 cm^3', info]    
    socket_service(ip, port, sending_list, image_path, infos)
    