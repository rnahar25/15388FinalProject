from googleapiclient.discovery import build
import random
import string
import json

def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.iteritems():
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
	videoId = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(11)])
	#print(videoId)
	return videoId

client = get_authenticated_service()
#f = open("surfind_videos.txt","w+")
result = search_list_by_keyword(client,
    		part='snippet',
    		maxResults=2,
    		q='dog',
    		type='')
maxLen = result['pageInfo']['totalResults']
result = search_list_by_keyword(client,
    		part='snippet',
    		maxResults=maxLen,
    		q='surfing',
    		type='')
		
	#print(type(result))
	#f.write(json.dumps(result))
#f.close()