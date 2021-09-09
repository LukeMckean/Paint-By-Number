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


font_size = 10 # font size for numbering
total_time = time.time()



img = plt.imread('Untitled.PNG')

#get the dimensions of the image
n,m,d = img.shape

all_colors = np.unique(img.reshape(-1, img.shape[2]), axis=0)
# get all colors from image and make a matrix for later

#blank image with the dims of the original
edges_img = np.full((n, m,3), 1.)

#Detect Edges and draw single black pxl
last_time = time.time()


print('\n',"STEP 1: Making outline")

# check for change of color horizontally then 'rotate' and check vertical
for row in range(0,n-1):
    for col in range(0, m-1):
        edge_score_c = (img[row, col]-img[row, col+1])
        edge_score_r = (img[row, col]-img[row+1, col])
        
        if np.any( edge_score_c != 0): 

            edges_img[row, col] = [0]*3        
        
        if np.any( edge_score_r != 0): 
            edges_img[row, col] = [0]*3   
        
        if time.time() - last_time > 2:
            last_time = time.time()
            print("Chewing on row " + str(row) + " out of " + str (n))
            #let the people know whats going on in your life


im = Image.fromarray((edges_img * 255).astype(np.uint8))
plt.imshow(im)
plt.show()

print ("(Time taken: {})".format(time.time() - total_time))

# count and index Zones


print('\n',"STEP 2: Counting Zones ")  

new_list = []
unchecked_pxls = []
img_2d = edges_img[:,:,0] 

#make unchecked pixel matrix for every point that isnt a black pxl
for row in range(0,n):
    for col in range(0, m):
        if img_2d[row,col] == 1:
            unchecked_pxls.append((row,col))
        

#flood fill algo https://en.wikipedia.org/wiki/Flood_fill#Moving_the_recursion_into_a_data_structure

zones_dict={}
i=0

#nested loops checks if the unchecked pixel is white,
#if yes, it makes it light blue (0,0,.1) then adds its N,S,E,W to the queue
#works until the queue is empty
# New_list var collects all the points that were changed and then dumps them in a dict

while bool(unchecked_pxls) == True :
    queue = [unchecked_pxls[0]]
    new_list = []
    while bool(queue) == True:
        temp = queue[0]
        del queue[0]
        if img_2d[temp] ==1:
            new_list.append(temp)
            img_2d[temp] = .1
            if temp[0]<n-1:
                queue.append((temp[0]+1,temp[1]))
            if temp[0]-1>0:
                queue.append((temp[0]-1,temp[1]))
            if temp[1]<m-1:    
                queue.append((temp[0],temp[1]+1))
            if temp[1]-1>0:
                queue.append((temp[0],temp[1]-1))

       
    
    unchecked_pxls = list(set(unchecked_pxls)- set(new_list))
    if len(new_list)>5:
            zones_dict[i] = new_list
    #to remove the new 'zone' from 'unchecked_pxls make them a SET first
    #I dont know why but this is like 10x faster then .remove
    
    
    i+=1
    
    plt.imshow(img_2d)
    plt.show()
    
   # x= input("sdF")
    
    if time.time() - last_time > 1:
        last_time = time.time()   

        plt.imshow(img_2d)
        plt.show()


#revert the light blue pxls back to white
edges_img[edges_img == .1] = 1

    
print('\n',"you have ", str(len(zones_dict)), " zones" )    
#let the people know whats going on in your life


print('\n',"STEP 3: Labeling Zones ")  
    





font = ImageFont.truetype('kovensky-small.ttf', font_size)

im = Image.fromarray((edges_img * 255).astype(np.uint8))
draw = ImageDraw.Draw(im)
bad_nums = 0
def cropper(zonesf):
    top,left = (random.choice(zonesf))
    right = left+font_size-1
    bottom = top+font_size-1
    return (top+1, left+1, right, bottom)


for zone in zones_dict:
    top, left, right, bottom = cropper(zones_dict[zone]) #random point in the zone
    imc = im.crop((left, top, right, bottom)) 
    i=0
    #check if the number placement is any good or if itll crash with lines
    
    while np.all((np.array(imc) == 255)) == False:  #for some reason this gives me a soft error
    # DeprecationWarning: elementwise comparison failed; this will raise an error in the future.
    #not sure what to do with that
        #top,left = zones_dict[zone][0]
        top, left, right, bottom = cropper(zones_dict[zone])
        imc = im.crop((left, top, right, bottom)) #crop the image to a small box
        #then while loop checks if there are black pxls in there
        i+=1
        if i>500: 
            #("couldnt find a good spot in zone: ", str(zone),
                  #"\n (", str(top), ", ", str(right), ")")
            bad_nums +=1
            break #if it cant find anything good it breaks
    
    
    color_index = np.where(np.all(img[top,left] == all_colors, axis=1))
    
    draw.text((left,top), str(int(''.join(map(str, color_index[0]))))+"(" +str(zone)+")" ,
                                              (0,0,255),font=font)

print('\n', "you got ", str(bad_nums), "bad number placements out of ", str(len(zones_dict)))
plt.imshow(im)
plt.show()



print('\n', "STEP 4: Making Ref colors ")
    
#make a separeate image with the reference colors from the original image

ref_colora=np.empty((font_size*2, len(all_colors)*font_size*2, 3))
block_x = range(font_size*2)
for col, color in enumerate(all_colors):
    for x in block_x:
        for y in block_x:
            ref_colora[y, x+(col*font_size*2)] = color

plt.imshow(ref_colora)
plt.show()   



print("STEP 5: Number Ref Colors ")

#Add ref numbers to the ref image

ref_color = Image.fromarray((ref_colora * 255).astype(np.uint8))
font = ImageFont.truetype('kovensky-small.ttf', font_size)

draw = ImageDraw.Draw(ref_color)
for col, color in enumerate(all_colors):
    draw.text(((col*font_size*2)+font_size , font_size),str(col),(0,0,0),font=font)
 
plt.imshow(ref_color)
plt.show()


print("STEP 6: Saving files")
  
ref_color.save('PBN Colors.png')
im.save('PBN sample_Numbered.png')


print ("Done! (Time taken: {})".format(time.time() - total_time))
