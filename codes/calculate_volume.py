# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 14:15:38 2018

@author: shuqi
"""
import math
from math import sqrt

def calibrate_length(long, short, ref_length):
    x = ref_length / long 
    y = ref_length / short
    z = ref_length / sqrt(long*long - short*short)
    
    return x, y, z


def count_pixels(food):
    total = 0;
    for i in food.shape[0]:
        for j in food.shape[1]:
            if (food[i][j]):
                total = total + 1
    
    return total


def cal_volume_1(long, short, ref_length, area, height):
    x, y, z = calibrate_length(long, short, ref_length)
    # print(x, y, z)
    return area * x * y * height * z


def cal_volume_2(long, short, ref_length, food):
    x, y, z = calibrate_length(long, short, ref_length)
    total = count_pixels(food)
    #  area 4*pi*r^2 -> volume 4/3*pi*r^3
    area = total * x * y
    volume = math.sqrt(math.pi) * (area ** 1.5) / 6
    
    return volume


def cal_volume_3(long, short, ref_length, food):
    volume = cal_volume_2(long, short, ref_length, food) / 2
    return volume


def cal_volume_4(long, short, ref_length, food):
    x, y, z = calibrate_length(long, short, ref_length)
    l = 0
    c = 0
    for i in range(0, food.shape[0]):
        temp = 0
        for j in range(0, food.shape[1]):
            if (food[i][j]):
                temp += 1
        c = max(temp, c)
    
    for j in range(0, food.shape[1]):
        temp = 0
        for i in range(0, food.shape[0]):
            if (food[i][j]):
                temp += 1
        l = max(temp, l)
        
    c = c * x
    area = (c / 2)**2 * math.pi
    a = c * short / long
    b = math.sqrt(c**2 - a**2)
    # some formula for calculating the height of the cone; not very sure if I was correct
    height = (l-a)**2 + ((b**2+l**2-(l-a)**2)/(2*b))**2 + c**2/4
    height = math.sqrt(height)
    
    volume = area * height / 3
    
    return volume

def cal_volume_5(long, short, ref_length, food, height):
    x, y, z = calibrate_length(long, short, ref_length)
    total = count_pixels(food)
    volume = total * height * x * y * z
    
    return volume
    
def cal_volume_6(long, short, ref_length, food, ref_volume):
    x, y, z = calibrate_length(long, short, ref_length)
    total = count_pixels(food)
    area = total * x * y
    volume = area ** 1.5 * ref_volume
    
    return volume
    

