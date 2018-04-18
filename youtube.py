from googleapiclient.discovery import build
from googletrans import Translator
import random
import string
import json
import csv
import pandas as pd

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

def checkField(vid, fieldType, first, second):
    if (second in vid[first]):
        return vid[first][second]
    else:
        if (fieldType == "str"):
            return ""
        elif (fieldType == "int"):
            return 0
        else:
            return []

client = get_authenticated_service()
f = open("rand_videos.txt","a")
translator = Translator()
csv_file = open('video_data.csv', 'w', newline = "", encoding='utf-8')
fieldnames = ['id', 'title', 'description', 'channelTitle', 'commentCount', 'viewCount', 'favoriteCount', 'dislikeCount', 'likeCount', 'tags', 'topics']
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writeheader()

f_ids = open("videoIdsAndLabels.txt", "r")
vocab = pd.read_csv("vocabulary.csv")

for line in f_ids:
    parts = line.split()
    vidId = parts[0]
    labels = parts[1:]
    
    video_response = videos_list_by_id(client,
        id = vidId,
        part = 'snippet, statistics')
    newVideo = {}
    try:  
        if (len(video_response['items']) == 0):
            continue
        vid = video_response['items'][0]
        title = vid['snippet']['title']
        lang = translator.detect(title)
        if lang.lang == 'en' and lang.confidence > 0.50:
            topics = []
            for label in labels:
                label_fix = label.replace('[','').replace(']','').replace(',','')
                topic = vocab['Name'][int(label_fix)]
                topics.append(topic)
            newVideo['topics'] = topics
            newVideo['id'] = vidId
            newVideo['title'] = title 
            newVideo['description'] = checkField(vid, "str", "snippet", "description")
            newVideo['channelTitle'] = checkField(vid, "str", "snippet", "channelTitle")
            newVideo['commentCount'] = checkField(vid, "int", "statistics", "commentCount")
            newVideo['viewCount'] = checkField(vid, "int", "statistics", "viewCount")
            newVideo['favoriteCount'] = checkField(vid, "int", "statistics", "favoriteCount")
            newVideo['dislikeCount'] = checkField(vid, "int", "statistics", "dislikeCount")
            newVideo['likeCount'] = checkField(vid, "int", "statistics", "likeCount")
            newVideo['tags'] = checkField(vid, "list", "snippet", "tags")
            writer.writerow(newVideo)
            f.write(json.dumps(vid))
            f.write('\n')
    except Exception as e:
        print("in except")
        print(e)
        print(newVideo)

f.close()
f_ids.close()
csv_file.close()

