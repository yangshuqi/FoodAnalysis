# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 13:11:48 2018

@author: shuqi
"""
from segment_food import *
from calculate_volume import *
from get_food_region import *

from skimage import data, color, transform, feature, morphology
from skimage import io



def get_volume_main(filepath, plate_color, ref_len, shape_type, additional_info = 0, debug = False, showing = False):
    
    """
    shape type:
        1: cube (e.g. cake)
        2: ball (e.g. apple)
        3: half-ball (e.g. bun)
        4: cone (e.g. fried rice in the plate)
        5: fixed-height (e.g. pizza)
        6: irregular but nearly fixed shape (e.g. banana)
        
    additional_info:
        height, for type 5
        volume per unit area, for type 6
    """
    
    image_rgb = io.imread(filepath) 
    if (image_rgb.shape[2] == 4):
        image_rgb = color.rgba2rgb(image_rgb)
    image_rgb = transform.resize(image_rgb, (int(100*image_rgb.shape[0]/image_rgb.shape[1]), 100))
    food, plate_long, plate_short = get_food_region(image_rgb, plate_color)
    
    if showing:
        io.imsave('original_image.jpg', image_rgb)
        
    if debug:    
        f, ((ax0, ax1, ax2, ax3), (ax4, ax5, ax6, ax7)) = plt.subplots(ncols=4, nrows=2, figsize=(22, 8))
        ax0.set_title('food')
        ax0.imshow(image_rgb)

    if shape_type == 1:           
        labels, labels2 = segment_food (image_rgb, food)
        area, height = get_height_and_area(labels2)
        volume = cal_volume_1(plate_long, plate_short, ref_len, area, height)
        
        if debug:
            ax2.set_title('segment')
            ax2.imshow(labels)
    
            ax3.set_title('segment2')
            ax3.imshow(labels2)
        
    if shape_type == 2:
        volume = cal_volume_2(plate_long, plate_short, ref_len, food)
    
    if shape_type == 3:
        volume = cal_volume_3(plate_long, plate_short, ref_len, food)
    
    if shape_type == 4:
        volume = cal_volume_4(plate_long, plate_short, ref_len, food)
        
    if shape_type == 5:
        volume = cal_volume_5(plate_long, plate_short, ref_len, food, additional_info)
    
    
    if shape_type == 6:
        volume = cal_volume_6(plate_long, plate_short, ref_len, food, additional_info)
    
    if debug:
        print('The estimated volume is', volume, 'cm^3.\n(Plate size:', ref_len, 'cm; type of shape: #', shape_type, '.)')
      
        for i in range(0, image_rgb.shape[0]):
            for j in range(0, image_rgb.shape[1]):
                if (food[i][j] == 0):
                    image_rgb[i][j] = [0,0,0]    
                
        ax1.set_title('food')
        ax1.imshow(image_rgb)
            
    
    if showing:
        if shape_type == 1:
            io.imsave('mid_result.jpg', labels2)
        else:
            io.imsave('mid_result.jpg', food)
    
    return volume  


if (__name__ == '__main__'):
    v = get_volume_main('../images/test.jpg', [140/225, 175/255, 160/255], 20, 1, debug = False, showing = True)
    print(v)