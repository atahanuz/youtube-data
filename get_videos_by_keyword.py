from googleapiclient.discovery import build

from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

API_KEY = 'AIzaSyCzVwAMXER7FEdDmeU8U_jbZETSlXFZSWw'
youtube = build('youtube', 'v3', developerKey=API_KEY)

from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

def get_like_count(video_id):
    video_response = youtube.videos().list(
        part='statistics',
        id=video_id
    ).execute()

    if 'items' in video_response and video_response['items']:
        return int(video_response['items'][0]['statistics']['likeCount'])
    else:
        return None


def get_video_description(video_id):
    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    if 'items' in video_response and video_response['items']:
        return video_response['items'][0]['snippet']['description']
    else:
        return None




def get_data_from_id(video_id):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    video = YouTube(video_url)

    result = YouTubeTranscriptApi.get_transcript(video_id, languages=['tr'])
    title, view_count, date, rating, channel = video.title, video.views, video.publish_date, video.rating, video.author
    thumbnail= video.thumbnail_url
    description = video.description

    text = " ".join(i["text"] for i in result)

    return {
        'title': title,
        'view_count': view_count,
        'date': date,
        'rating': rating,
        'channel': channel,
        'thumbnail': thumbnail,
        'transcript_text': text,
    }

def search_youtube_videos(keyword, max_results=2,truncate=False):
    search_response = youtube.search().list(
        q=keyword,
        type='video',
        part='id,snippet',
        maxResults=max_results,
        relevanceLanguage='tr'
    ).execute()

    videos = []
    for search_result in search_response.get('items', []):
        video_id = search_result['id']['videoId']
        like_count = get_like_count(video_id)
        description = get_video_description(video_id)

        video = {
            'video_id': video_id,

            'description': description,
            'like_count': like_count,


            # 'video_url': f"https://www.youtube.com/watch?v={video_id}",
            # 'title': search_result['snippet']['title'],
            # 'thumbnail_url': search_result['snippet']['thumbnails']['default']['url'],
            # 'channel_title': search_result['snippet']['channelTitle'],
            # 'publish_date': search_result['snippet']['publishedAt'],

        }
        externaldata=get_data_from_id(video_id)
        video.update(externaldata)
        video['link']=f"https://www.youtube.com/watch?v={video_id}"

        video['title'] = video.pop('title')
        video['video_id'] = video.pop('video_id')
        video['link'] = video.pop('link')
        video['channel_title'] = video.pop('channel')
        video['view_count'] = video.pop('view_count')
        video['publish_date'] = video.pop('date')
        video['like_count'] = video.pop('like_count')
        video['description'] = video.pop('description')
        video['thumbnail_url'] = video.pop('thumbnail')
        video['rating'] = video.pop('rating')
        video['transcript_text'] = video.pop('transcript_text')

        videos.append(video)



    if truncate:
        for result in videos:
            for key, value in result.items():
                if isinstance(value, str):
                    result[key] = value[:100] + '...' if len(value) > 100 else value

    return videos


def print_result(results):
    for result in results:
        print("------")
        for key, value in result.items():
            print(f"{key}: {value}")

def save_result(results,filename):
    import json
    with open(filename, 'w',encoding='utf-8') as outfile:
        json.dump(results, outfile,default=str,ensure_ascii=False,indent=4)


if __name__ == '__main__':


    results = search_youtube_videos('Felsefe', 2)
    save_result(results,"results.json")
