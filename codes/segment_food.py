# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 17:23:47 2018

@author: shuqi
"""
from sklearn.cluster import KMeans
import numpy as np
from skimage.morphology import disk
from skimage.filters.rank import median

def segment_food (img_rgbb, food):
    
    img_rgb = img_rgbb * 1.0
    for k in range(0,3):
        img_rgb[:,:,k] = median(img_rgbb[:,:,k], disk(3)) / 255
           
    sum = 0;
    for i in range(0, food.shape[0]):
        for j in range(0, food.shape[1]):
            if (food[i][j] == 1):
                sum = sum+1
    
    data = np.zeros((sum,5))
    idx = 0
    a = np.zeros([2, 5], float)
    # a[0][i]: min
    # a[1][i]: max
    for i in range(0, 5):
        a[0][i] = 1e9


    for i in range(0, food.shape[0]):
        for j in range(0, food.shape[1]):
            if (food[i][j] == 1):
                data[idx][0] = i
                data[idx][1] = j
                data[idx][2] = img_rgb[i][j][0]
                data[idx][3] = img_rgb[i][j][1]
                data[idx][4] = img_rgb[i][j][2]
                idx = idx + 1
    
    # normalize data
    for i in range(0, idx):
        for j in range(0, 5):
            a[0][j] = min(a[0][j], data[i][j])
            a[1][j] = max(a[1][j], data[i][j])
    
    weight_x = 1.5
    weight_y = 3
    for i in range(0, idx):
        for j in range(0, 5):
            data[i][j] = (data[i][j] - a[0][j]) / (a[1][j] - a[0][j])
        data[i][0] = data[i][0] * weight_y
        data[i][1] = data[i][1] * weight_x
    # print(data)
    kmeans = KMeans(n_clusters=2, random_state=0).fit(data)
    
    labels = food * 0 
    centers = kmeans.cluster_centers_
    
    # higher center: top part; lower center: side part
    l = [0, 1]
    if centers[0][0] > centers[1][0] :
        l = [1, 0]
        
    # assign lables to each pixel
    for i in range(0, kmeans.labels_.shape[0]):
        x = (data[i][0]/weight_y*(a[1][0]-a[0][0])+a[0][0])
        y = (data[i][1]/weight_x*(a[1][1]-a[0][1])+a[0][1])
        la = kmeans.labels_[i]
        
        # int(x+0.5): convert float to int
        labels[int(x+0.5)][int(y+0.5)]= (l[la]+1)*0.5
    
    # median filter, smoothing the result
    labels2 = median(labels, disk(3))
    
    return labels, labels2


def get_height_and_area(labels):      
    area = 0
    for i in range(labels.shape[0]):
        for j in range(labels.shape[1]):
            if (0 < labels[i][j] and labels[i][j] <= 128):
                area = area+1
    
    heights = []
    for j in range(labels.shape[1]):
        a = 0
        for i in range(labels.shape[0]):
            if (labels[i][j] > 128):
                a = a+1
        if a != 0:
            heights.append(a)
    
    idx1 = int(len(heights)*0.2)
    idx2 = int(len(heights)*0.8)
    height = sum(heights[idx1: idx2]) / (idx2 - idx1)
    
    return area, height