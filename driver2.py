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

#--------------------------------------
# Selecting music
#--------------------------------------

predictions = mp.labels(description)
music_path = mp.music_gen(predictions)
print(music_path)

#--------------------------------------
# Video text placement
#--------------------------------------
video_original = "/content/Slideshow-Generator/result/prod.mp4" #input video to be morphed
cap = cv2.VideoCapture(video_original)

length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print("DETECTED LENGTH IN FRAMES: {0}".format(length))
fps= int(cap.get(cv2.CAP_PROP_FPS))
print("DETECTED FPS: {0}".format(fps))
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
size = (frame_width, frame_height)
fourcc = cv2.VideoWriter_fourcc(*"MP4V")
output_video = "/content/Slideshow-Generator/result/postprod.mp4"
writer = cv2.VideoWriter(output_video, fourcc, fps,size, True)
frame_number = 0

#########################################JSON DATA EXTRACTION###############################################################

json_file = open('/content/Slideshow-Generator/Json/tagline1.json','r')
data = json.load(json_file)

print(len(data.get("data")))

for document in range(0,len(data.get("data"))):
  print("I am at this iteration : {0}".format(document))
  start_time = data.get("data")[document].get("startTime")
  end_time = data.get("data")[document].get("endTime")

  pointer_start = int(fps*start_time)
  pointer_end = int(fps*end_time)
  print(pointer_start)
  print(pointer_end)

  

  
  

  
  for i in tqdm(range(0,length),desc="progress per frame"):
    
    ret, img = cap.read()
    
    if img is None:
      
      break
    
    position = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    #print("my position in the beg of for itqdm : {0}".format(position))
    if position in range(pointer_start,pointer_end+1):
      
      imgPil = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      im_pil = Image.fromarray(imgPil)
      
      
      TextOverlay = ImageDraw.Draw(im_pil)
      fontHindi = ImageFont.truetype('/content/Slideshow-Generator/font/Magnolia Script.otf', 36)
      mask = Image.new('L', im_pil.size, 0)
      draw = ImageDraw.Draw(mask)
      x = 0
      y = frame_height//2
      w = 500
      h = y+50
      draw.rectangle([(x,y), (w,h)], fill=255)
      blurred = im_pil.filter(ImageFilter.GaussianBlur(52))
      im_pil.paste(blurred, mask=mask)
      img1 = ImageDraw.Draw(im_pil)
     
      img1.text((x,y),data.get("data")[document].get('displayText'),fill=(255,255,255),font=fontHindi)
      im_pil.convert('RGB')
      open_cv_image = np.array(im_pil)
      open_cv_image = open_cv_image[:, :, ::-1].copy()
      writer.write(open_cv_image)
      
    


    else:
      if position == pointer_end+1:
        print("I am in else pointer: {0}".format(pointer_end+1))
        cap.set(cv2.CAP_PROP_POS_FRAMES,pointer_end)
        break
      else:
        print("I have not yet achieved end, so I am still writing")
        writer.write(img)









writer.release()
cv2.destroyAllWindows()




