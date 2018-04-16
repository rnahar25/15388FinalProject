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
translator = Translator()

numVids = 0
# search_videos = []
allWords = set()
while(numVids < numVideos):
  word = rw.random_word()
  while (word in allWords):
    word = rw.random_word()
  allWords.add(word) 
  randId = getRandomId()
  result = search_list_by_keyword(client,
      		part='snippet',
      		maxResults=1,
      		#q=randId,
          q=word,
      		type='',
          regionCode = 'US')

  vid = result['items'][0]
  try:
    #if (vid['id']['videoId'][:videoIdLen]) == randId:
    lang = translator.detect(vid['snippet']['title'])
    print("trying title", vid['snippet']['title'], lang.lang, lang.confidence > 0.50)
    if lang.lang == 'en' and lang.confidence > 0.50:
      # search_videos.append(vid['id']['videoId'])
      # print(vid['id']['videoId'])
      video_response = videos_list_by_id(client,
        id=vid['id']['videoId'],
        part='snippet, statistics')
      f.write(json.dumps(video_response['items'][0]))
      f.write('\n')
      numVids += 1
  except:
    pass
  # video_ids = ','.join(search_videos)
# print("BLAH")
# print(search_videos)
# print(video_ids)
# print(translator.detect('coco'))
# print(video_response)
		
	#print(type(result))
	#f.write(json.dumps(result))
f.close()