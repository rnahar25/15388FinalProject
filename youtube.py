from googleapiclient.discovery import build
from googletrans import Translator
import random
import string
import json
from random_words import RandomWords
import pandas as pd

rw = RandomWords()
global videoIdLen
videoIdLen = 3
numVideos = 3

def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.items():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def print_response(response):
  print(response)

def videos_list_by_id(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.videos().list(
    **kwargs
  ).execute()
  return response
  #return print_response(response)

def search_list_by_keyword(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.search().list(
    **kwargs
  ).execute()

  return response


def get_authenticated_service():
  api_key = open('api_key.txt', 'r').read()
  return build('youtube', 'v3', developerKey = api_key)

def getRandomId():
  videoId = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(videoIdLen)])
  #print(videoId)
  return videoId

client = get_authenticated_service()
f = open("rand_videos.csv","w+")
f_ids = open("sample_ids.txt", "r")  # <-- Change this!
vocab = pd.read_csv("vocabulary.csv")
translator = Translator()

for line in f_ids:
  parts = line.split()
  vidId = parts[0]
  labels = parts[1:]
  video_response = videos_list_by_id(client,
    id = vidId,
    part = 'snippet, statistics')['items'][0]
  # print(video_response)
  try:
    title = video_response['snippet']['title']
    # print(title)
    lang = translator.detect(title)
    # print(lang.lang, lang.confidence)
    if lang.lang == 'en' and lang.confidence > 0.50:
      # print("Writing to file")
      # f.write(json.dumps(video_response))  <-- Change this!
      for label in labels:
        label_fix = label.replace('[','').replace(']','').replace(',','')
        # print(label_fix)
        topic = vocab['Name'][int(label_fix)]
        # print(topic)
        f.write(','+ topic)
      f.write('\n')
  except:
    pass

f.close()
f_ids.close()

