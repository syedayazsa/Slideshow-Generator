#--------------------------------------
# Importing Libraries
#--------------------------------------

import spacy
from textblob import TextBlob
nlp = spacy.load('en_core_web_sm')
import os,random


#--------------------------------------
# Gives you needed keywords
#--------------------------------------

def words2search(data):
  doc = nlp(data)
  for ent in doc.ents:
    return [(X.text, X.label_) for X in doc.ents]


#--------------------------------------
# Removes stopwords
#--------------------------------------

def stopwordsRemover(data):
  doc = nlp(data)
  token_list = [token for token in doc]
  filtered_tokens = [token for token in doc if not token.is_stop]
  return filtered_tokens


#--------------------------------------
# Tells you which music is more suited
#--------------------------------------


def labels(data):
  polarity = TextBlob(data).sentiment.polarity
  subjectivity = TextBlob(data).sentiment.subjectivity
  if polarity == 0.0:
    label_music = 'neutral_music'
  elif (polarity>0.0 and polarity<0.5):
    label_music = 'positive_music'
  elif (polarity>0.50):
    label_music = 'happy_music'
  elif (polarity<0.0 and polarity> -0.5 ):
    label_music = 'slightly_negative_music'
  elif (polarity < -0.5):
    label_music = 'negative_music'
  else:
    label_music = 'any_neutral_music'

  if (subjectivity > 0 and subjectivity<0.5):
    label_subject = 'factual data'
  elif (subjectivity >0.5):
    label_subject = 'personal toned data'
  else:
    label_subject = 'neutral toned'

  return [label_music,label_subject]


#--------------------------------------
# Gives you the path of audio file
#--------------------------------------


def music_gen(prediction):
  music_path = "audio/{0}/".format(prediction[0])+random.choice(os.listdir("audio/{0}".format(prediction[0])))
  return music_path










