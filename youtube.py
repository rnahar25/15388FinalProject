from googleapiclient.discovery import build
from googletrans import Translator
import random
import string
import json
from random_words import RandomWords

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
f = open("rand_videos.txt","a")
allWords = set()

#initialize allWords
f3 = open("word_set.txt", "r")
lines = f3.readlines()
for line in lines:
	allWords.add(line.strip())
f3.close()

f2 = open("word_set.txt","a")
translator = Translator()
numVids = 0

while(numVids < numVideos):
  #get a random word
  word = rw.random_word()
  while (word in allWords):
    word = rw.random_word()
  f2.write(word)
  f2.write('\n')
  allWords.add(word) 
  result = search_list_by_keyword(client,
      		part='snippet',
      		maxResults=1,
            q=word,
      		type='',
          regionCode = 'US')

  vid = result['items'][0]
  try:
    lang = translator.detect(vid['snippet']['title'])
    if lang.lang == 'en' and lang.confidence > 0.50:
      video_response = videos_list_by_id(client,
        id=vid['id']['videoId'],
        part='snippet, statistics')
      f.write(json.dumps(video_response['items'][0]))
      f.write('\n')
      numVids += 1
  except:
    pass
f.close()
f2.close()

