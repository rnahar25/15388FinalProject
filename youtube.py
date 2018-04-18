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

f_ids = open("ids.txt", "r")

for line in f_ids:
	vidId = line.split()[0]
	result = videos_list_by_id(client,
		id = vidId,
		part = 'snippet, statistics')
	try:
		lang = translator.detect(vid['snippet']['title'])
	    if lang.lang == 'en' and lang.confidence > 0.50:
	    	f.write(json.dumps(video_response['items'][0]))
	    	f.write('\n')
	except:
		pass

f.close()
f_ids.close()

