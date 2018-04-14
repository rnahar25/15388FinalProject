from googleapiclient.discovery import build
from googletrans import Translator
import random
import string
import json

global videoIdLen
videoIdLen = 5

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
f = open("rand_videos.txt","w+")
translator = Translator()

numVids = 0
search_videos = []
while(numVids < 3):
  randId = getRandomId()
  result = search_list_by_keyword(client,
      		part='snippet',
      		maxResults=50,
      		q=randId,
      		type='',
          relevanceLanguage = 'in')

  for vid in result['items']:
    if 'videoId' in vid['id'].keys():
      try:
        lang = translator.detect(vid['snippet']['title'])
        print("trying title", vid['snippet']['title'])
        if (vid['id']['videoId'][:videoIdLen]) == randId and (lang.lang == 'en' and lang.confidence > 0.50):
          search_videos.append(vid['id']['videoId'])
          # print(vid['id']['videoId'])
          numVids += 1
      except:
        pass
  video_ids = ','.join(search_videos)
# print("BLAH")
# print(search_videos)
# print(video_ids)
video_response = videos_list_by_id(client,
  id=video_ids,
  part='snippet, statistics')
f.write(json.dumps(video_response))
# print(translator.detect('coco'))
# print(video_response)
		
	#print(type(result))
	#f.write(json.dumps(result))
f.close()