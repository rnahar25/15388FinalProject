from googleapiclient.discovery import build
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
	api_key = 'AIzaSyAvTpcReN0T7ID4OAkxbOLvC1FeoFS_SQg'
	return build('youtube', 'v3', developerKey = api_key)

def getRandomId():
	videoId = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(videoIdLen)])
	#print(videoId)
	return videoId

client = get_authenticated_service()
#f = open("surfind_videos.txt","w+")

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
      if (vid['id']['videoId'][:videoIdLen]) == randId:
        search_videos.append(vid['id']['videoId'])
        print(vid['id']['videoId'])
        numVids += 1
  video_ids = ','.join(search_videos)
# print("BLAH")
# print(search_videos)
# print(video_ids)
video_response = videos_list_by_id(client,
  id=video_ids,
  part='snippet, statistics')

print(video_response)
		
	#print(type(result))
	#f.write(json.dumps(result))
#f.close()