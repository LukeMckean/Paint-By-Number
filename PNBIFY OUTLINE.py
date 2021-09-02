# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 17:45:01 2021

@author: 409182
"""
from PIL import ImageFont
from PIL import ImageDraw 
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random, time



grid_size = 15 # Grid size for numbering

font_size = 10 # font size for numbering


total_time = time.time()
#read in the pinwheel image
img = plt.imread('out.PNG')

#get the dimensions of the image
n,m,d = img.shape


#Detect Edges and draw ingle black pxl

edges_img = np.full((n, m,3), 1.)

#edges_img = img.copy()
last_time = time.time()
all_colors = np.unique(img.reshape(-1, img.shape[2]), axis=0)


print("STEP 1: detecting edges")

for row in range(0,n-1):
    for col in range(0, m-1):
        edge_score_c = (img[row, col]-img[row, col+1])
        edge_score_r = (img[row, col]-img[row+1, col])
        
        if np.all( edge_score_c == 0): 
            edges_img[row, col] = [1]*3
        else: 
            edges_img[row, col] = [0]*3        
        
        if np.any( edge_score_r != 0): 
            edges_img[row, col] = [0]*3   
        
        if time.time() - last_time > 5:
            last_time = time.time()
            print("Chewing on row " + str(row) + " out of " + str (n))
            


# Add Ref colors in the top corner

    
block_x = range(font_size*2)
font = ImageFont.truetype('kovensky-small.ttf', font_size)

print("STEP 2: Making Ref colors ")

for col, color in enumerate(all_colors):
    for x in block_x:
        for y in block_x:
            edges_img[y, x+(col*font_size*2)] = color
    

im = Image.fromarray((edges_img * 255).astype(np.uint8))
draw = ImageDraw.Draw(im)

print("STEP 3: Label Ref Colors ")

# label color ref
for col, color in enumerate(all_colors):
    draw.text(((col*font_size*2)+font_size , font_size),str(col+1),(0,0,0),font=font)





# Add Numbers Zones


print("STEP 4: Numbering Zones ")  

for row in range(1,int(np.trunc(n/grid_size))):
    for col in range(1, int(np.trunc(m/grid_size))):
        
        left = col*grid_size
        top = row*grid_size
        right = col*grid_size+font_size+1
        bottom = row*grid_size+font_size+1
       
        imc = im.crop((left, top, right, bottom))
               
       
        
        if np.all(np.array(imc) == [255,255,255])==True:
            
             color_index = np.where(np.all(img[row*grid_size, col*grid_size]
                                           == all_colors, axis=1))
             draw.text((col*grid_size+(font_size/2) , row*grid_size+(font_size/2) ),str(int(color_index[0])+1)
                       ,(0,0,0),font=font) # this will draw text with Blackcolor and 16 size

plt.imshow(im)
plt.show()

im.save('sample_Numbered.png')