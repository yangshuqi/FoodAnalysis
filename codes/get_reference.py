# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 11:24:30 2018

@author: shuqi
"""

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm

from skimage.transform import hough_line, hough_line_peaks, hough_ellipse
from skimage.draw import line, ellipse_perimeter
from skimage import data, color, transform, feature
from skimage import io
from skimage.feature import canny

import math 
 
# import cv2


def get_longest_line(image, meta_ref, rgb = False):
    image_gray = color.rgb2gray(image)
    edges = feature.canny(image_gray, sigma=2.0,
                     low_threshold=0.1, high_threshold=0.2)
    
    h, theta, d = hough_line(edges)
    
    for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
        y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
        y1 = (dist - image.shape[1] * np.cos(angle)) / np.sin(angle)
        x0 = (dist - 0 * np.sin(angle)) / np.cos(angle)
        x1 = (dist - image.shape[0] * np.sin(angle)) / np.cos(angle)
    
        xy = [];
        xy.append([0, y0])
        xy.append([image.shape[1], y1])
        xy.append([x0, 0])
        xy.append([x1, image.shape[0]])
      
        print(xy[0], xy[1], xy[2], xy[3])
    
        idx = 0
        for i in range(0,4):
            if 0 <= xy[i][0] and xy[i][0] < image.shape[1] and 0 <= xy[i][1] and xy[i][1] < image.shape[0]:
                xy[idx] = xy[i]
                idx = idx+1

        
        def is_inside(x, y, x0, y0):
            return 0 <= x and x < x0 and 0 <= y and y < y0
        
        def is_valid(x, y, edges, x0, y0): 
            for i in range(-4, 5):
                for j in range(-4, 5):
                    xx = x + i;
                    yy = y + j;
                    if is_inside(xx, yy, x0, y0) and edges[yy][xx]:
                        return True
                    
            return False;
        start = (0, 0)
        end = (0, 0)
        if abs(xy[0][0] - xy[1][0]) > abs(xy[0][1] - xy[1][1]):
            if (xy[0][0] > xy[1][0]):
                xy[0][0], xy[1][0] = xy[1][0], xy[0][0]
                xy[0][1], xy[1][1] = xy[1][1], xy[0][1]
                                
            lx = int(xy[0][0])
            ly = int(xy[0][1])
            while not is_valid(lx, ly, edges, image.shape[1], image.shape[0]):
                lx = lx + 1
                ly = int((dist - lx * np.cos(angle)) / np.sin(angle))
                if (lx >= image.shape[1]) :
                    break
            lx = lx - 1;
            start = (lx, int((dist - lx * np.cos(angle)) / np.sin(angle)))
            lx = lx + 1;
            
            while is_valid(lx, ly, edges, image.shape[1], image.shape[0]):
                lx = lx + 1
                ly = int((dist - lx * np.cos(angle)) / np.sin(angle))
                if (lx >= image.shape[1]) :
                    break
            lx = lx - 1;
            end = (lx, int((dist - lx * np.cos(angle)) / np.sin(angle)))
            
        else:
            if (xy[0][1] > xy[1][1]):
                xy[0][0], xy[1][0] = xy[1][0], xy[0][0]
                xy[0][1], xy[1][1] = xy[1][1], xy[0][1]
                                
            lx = int(xy[0][0])
            ly = int(xy[0][1])
            while not is_valid(lx, ly, edges, image.shape[1], image.shape[0]):
                ly = ly + 1
                lx = int((dist - ly * np.sin(angle)) / np.cos(angle))
                if (ly >= image.shape[0]) :
                    break
            ly = ly - 1;
            start = (int((dist - ly * np.sin(angle)) / np.cos(angle)), ly)
            ly = ly + 1;
            
            while is_valid(lx, ly, edges, image.shape[1], image.shape[0]):
                ly = ly + 1
                lx = int((dist - ly * np.sin(angle)) / np.cos(angle))
                if (ly >= image.shape[0]) :
                    break
            ly = ly - 1;
            end = (int((dist - ly * np.sin(angle)) / np.cos(angle)), ly)
    
        print(start, end)
    
    fig2, (ax0, ax1, ax2) = plt.subplots(ncols=3, nrows=1, figsize=(10, 6))

    ax0.set_title('edges')
    ax0.imshow(edges)

    
    
if (__name__ == '__main__'):
    image_rgb = io.imread('../images/test-00.jpg') # data.coffee()[0:220, 160:420] #   
    if (image_rgb.shape[2] == 4):
        image_rgb = color.rgba2rgb(image_rgb)
    image_rgb = transform.resize(image_rgb, (100, 160))
    get_longest_line(image_rgb, 18, True)