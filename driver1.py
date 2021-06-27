#--------------------------------------
# Importing Libraries
#--------------------------------------

import numpy as np
import math
from PIL import Image, ImageDraw,ImageFont,ImageFilter
import cv2
import json 
from tqdm import tqdm
import cv2
import numpy as np
import glob
import os
import random
from PIL import Image
import requests
import json
import glob 
from PIL import ImageFont
from PIL import ImageDraw
import music as mp
from moviepy.editor import *



#--------------------------------------
# Read JSON
#--------------------------------------



print('--------------------------------------')
print('Enter the JSON File Path(Full Path): ')
print('--------------------------------------')
json_file = input()

with open(json_file) as f:
    data = json.load(f)

tagline = str(data['data'][0]['tagLine'])
description  = str(data['description'])



keywords = []
for i in range(len(data['data'])):
    keywords.append(data['data'][i]['keyword'])

#--------------------------------------
# Get & Edit Images
#--------------------------------------



print('Downloading Images.....')
print('--------------------------------------')
#font = ImageFont.truetype("/Users/ayaz/Desktop/Misc/times-ro.ttf", 188)

os.chdir("/content/Slideshow-Generator/pics")
from pexelsPy import API
PEXELS_API = "563492ad6f91700001000001f71c408e552945e58a9c8a4a68bc5333"
api = API(PEXELS_API)

for keyword in keywords:
    api.search_photos(keyword,page=1, results_per_page=1)    
    photos = api.get_photos()

    for data in photos:
        #Saving the Image
        response = requests.get(data.original)
        fname = keyword + '.png'
        file = open(fname, "wb")
        file.write(response.content)
        
        #Editing the Image
        #img = Image.open(fname)
        #draw = ImageDraw.Draw(img)
        #draw.text((900, 900),keyword,(237, 21, 21),font=font, fontsize = 188)
        #img.save(fname)
        
file.close()

print('Images Downloaded Successfully!')
print('--------------------------------------')



#--------------------------------------
# Video writer initialisation
#--------------------------------------

size = (500,500) #as in aspect ratio
fps = 40 

time_video = 10 #enter time in seconds
counter = int((time_video*fps)/100)
# Below VideoWriter object will create
# a frame of above defined The output 
# is stored in 'filename.mp4' file.
video_path = '/content/Slideshow-Generator/result/prod.mp4'
result = cv2.VideoWriter(video_path, 
                         cv2.VideoWriter_fourcc(*'MP4V'),
                         fps, size)


#--------------------------------------
# Generating slideshow
#--------------------------------------



print('Creating & Launching Slideshow.....')
print('--------------------------------------')
os.chdir("/content/Slideshow-Generator")
class Image:
    def __init__(self, filename, time=500, size=500):
        self.size = size
        self.time = time
        self.shifted = 0.0
        self.img = cv2.imread(filename)
        self.height, self.width, _ = self.img.shape
        if self.width < self.height:
            self.height = int(self.height*size/self.width)
            self.width = size
            self.img = cv2.resize(self.img, (self.width, self.height))
            self.shift = self.height - size
            self.shift_height = True
        else:
            self.width = int(self.width*size/self.height)
            self.height = size
            self.shift = self.width - size
            self.img = cv2.resize(self.img, (self.width, self.height))
            self.shift_height = False
        self.delta_shift = self.shift/self.time

    def reset(self):
        if random.randint(0, 1) == 0:
            self.shifted = 0.0
            self.delta_shift = abs(self.delta_shift)
        else:
            self.shifted = self.shift
            self.delta_shift = -abs(self.delta_shift)

    def get_frame(self):
        if self.shift_height:
            roi = self.img[int(self.shifted):int(self.shifted) + self.size, :, :]
        else:
            roi = self.img[:, int(self.shifted):int(self.shifted) + self.size, :]
        self.shifted += self.delta_shift
        if self.shifted > self.shift:
            self.shifted = self.shift
        if self.shifted < 0:
            self.shifted = 0
        return roi

def process():
    path = "pics" #path to image folder
    filenames = glob.glob(os.path.join(path, "*"))
    fps_count = 0

    cnt = 0
    images = []
    for filename in filenames:
        print(filename)

        img = Image(filename)

        images.append(img)
        if cnt > 300:
            break
        cnt += 1

    prev_image = images[random.randrange(0, len(images))]
    prev_image.reset()

    while fps_count<counter:
        while True:
            img = images[random.randrange(0, len(images))]
            if img != prev_image:
                break
        

        for i in range(100):
          if fps_count<counter:
            alpha = i/100
            beta = 1.0 - alpha
            dst = cv2.addWeighted(img.get_frame(), alpha, prev_image.get_frame(), beta, 0.0)

            result.write(dst)
          else:
            break


        prev_image = img
        if fps_count < counter:
          fps_count+=1
            


process()



result.release()
cv2.destroyAllWindows()



