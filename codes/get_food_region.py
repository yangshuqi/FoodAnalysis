# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 14:23:20 2018

@author: shuqi
"""

import numpy as np

#  import matplotlib.pyplot as plt
#  from matplotlib import cm

from skimage.transform import hough_line, hough_line_peaks, hough_ellipse
from skimage.draw import line, ellipse_perimeter
from skimage import data, color, transform, feature, morphology
from skimage import io
from skimage.feature import canny
import json


import math 

import sys
sys.setrecursionlimit(10000)

def get_plate(img, rgb, threshold, siz = 2):
    img_binary = color.rgb2gray(img)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if abs(img[i][j][0] - rgb[0]) > threshold or abs(img[i][j][1] - rgb[1]) > threshold or abs(img[i][j][2] - rgb[2]) > threshold:
                img_binary[i][j] = 0
            else:
                img_binary[i][j] = 1
    
    res1 = morphology.dilation(morphology.erosion(img_binary, morphology.disk(siz)) , morphology.disk(siz))
    
    res2 = res1*1.0
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if (res1[i][j] != 1):
                res2[i][j] = -1
                
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if (res2[i][j] == 1):
                search(img, res2, i, j, 0.1)
                
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if (res2[i][j] != 1):
                res2[i][j] = 0
    
    return img_binary, res1, res2
                

def search(img, background, x, y, threshold):
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]
    for i in range(0, 4):
        xx = x + dx[i]
        yy = y + dy[i]
        if (0 <= xx and xx < background.shape[0] and 0 <= yy and yy < background.shape[1]):
            if (background[xx][yy] == -1) :
                if sum(abs(img[xx][yy] - img[x][y])) < threshold: #(abs(img[xx][yy][0] - img[x][y][0]) < threshold and abs(img[xx][yy][1] - img[x][y][1]) < threshold and abs(img[xx][yy][2] - img[x][y][2]) < threshold):
                    background[xx][yy] = 1
                    search(img, background, xx, yy, threshold)
                else:
                    background[xx][yy] = 0


def get_background(img, plate, threshold, siz = 2):
    background = plate-1
    
    search(img, background, 0, 0, 0.1)
    search(img, background, 0, img.shape[1]-1, 0.1)
    search(img, background, img.shape[0]-1, 0, 0.1)
    search(img, background, img.shape[0]-1, img.shape[1]-1, 0.1)
    
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if (background[i][j] != 1):
                background[i][j] = 0
    
    return background
   
    
def get_plate_size(plate):
    long = 0;
    long_idx = 0;
    for i in range(0, plate.shape[0]):
        a = 0
        while a < plate.shape[1]:
            if plate[i][a] == 1:
                break
            a = a+1
        b = plate.shape[1] - 1
        while b >= 0:
            if plate[i][b] == 1:
                break
            b = b-1
        if (b-a) > long:
            long = b-a
            long_idx = i
    
    short = 0
    bottom = plate.shape[0]-1
    flag = 0
    while flag == 0:
        for j in range(0, plate.shape[1]):
            if plate[bottom][j] == 1:
                flag = 1
                break
        bottom = bottom-1
    short = bottom - long_idx
    
    return long, short*2
        
            
def get_food_region(image_rgb, plate_color):
    with open("configs.json",'r') as f:
        configs = json.load(f)
    img, res1, res2 = get_plate(image_rgb, plate_color, configs['food_thre'])
    plate = res2
    background = get_background(image_rgb, plate, 0.2, configs['background_thre'])
    not_food = plate + background
    siz = 3
    not_food1 = morphology.erosion(morphology.dilation(not_food, morphology.disk(siz)) , morphology.disk(siz))
    a, b = get_plate_size(plate)
    
#    f, ((ax0, ax1, ax2, ax3), (ax4, ax5, ax6, ax7)) = plt.subplots(ncols=4, nrows=2, figsize=(22, 8))
#     
#    ax0.set_title('image0')
#    ax0.imshow(image_rgb)
#    
#    ax1.set_title('plate')
#    ax1.imshow(img)
#    
#    ax2.set_title('plate-morphology')
#    ax2.imshow(res1)
#    
#    ax3.set_title('plate-dfs')
#    ax3.imshow(res2)
#    
#    ax4.set_title('background')
#    ax4.imshow(background)
#
#    ax5.set_title('not food')
#    ax5.imshow(not_food)
#    
#    
#    ax6.set_title('not food-1')
#    ax6.imshow(not_food1)
#    
#    
#    for i in range(0, image_rgb.shape[0]):
#        for j in range(0, image_rgb.shape[1]):
#            if (not_food1[i][j] == 1):
#                image_rgb[i][j] = [0,0,0]    
#                
#    ax7.set_title('food')
#    ax7.imshow(image_rgb)
#    
#    print(a, b)
    
    return abs(not_food1 - 1), a, b
