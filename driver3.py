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
# Mixing audio and Video
#--------------------------------------
videoclip = VideoFileClip('/content/Slideshow-Generator/result/postprod.mp4')

audio_file = AudioFileClip(music_path)
time_video = videoclip.duration
if int(audio_file.duration) < time_video:
  audio = afx.audio_loop( audio_file, duration=time_video)
elif int(audio_file.duration)>time_video:
  audio = audio_file.subclip(0,time_video)
else:
  audio = audio_file

new_audioclip = CompositeAudioClip([audio])
videoclip.audio = new_audioclip
videoclip.write_videofile("/content/Slideshow-Generator/result/final_result.mp4")







