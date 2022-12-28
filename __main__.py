import os
from dotenv import load_dotenv
import tweepy
import time
import tiktok_scraper
import requests
import base64
import moviepy.editor as mp
import video_tweet

load_dotenv()

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

print(BEARER_TOKEN)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

twitter_api = tweepy.API(auth)

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)

    file_bytes = bytes(r.text, 'utf-8')

    # print("request ", r.text)

    with open("video.mp4", 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
                
    return file_bytes

def main():
    starttime = time.time()
    last_uploaded_video = ''

    twitter_api.verify_credentials()
    print("Authentication OK")
    scraper = tiktok_scraper.TikTokScraper()

    while True:
        try:
            video_urls = scraper.get_user_liked_videos("gentij1")

            last_video_index = video_urls.index(last_uploaded_video) if last_uploaded_video in video_urls else 0

            if last_video_index != 0:
                new_liked_videos = video_urls[:last_video_index]

                for video_url in reversed(new_liked_videos):
                    video_link = scraper.get_liked_video_url(video_urls[0])

                    download_file(video_link)

                    clip = mp.VideoFileClip("video.mp4")
                    clip_resized = clip.resize(height=1280) 
                    clip_resized.write_videofile("video_resized.mp4", temp_audiofile='temp-audio.m4a', remove_temp=True, codec="libx264", audio_codec="aac")

                    VideoTweet = video_tweet.VideoTweet("video_resized.mp4")
                    VideoTweet.upload_init()
                    VideoTweet.upload_append()
                    VideoTweet.upload_finalize()
                    VideoTweet.tweet()
                
            last_uploaded_video = video_urls[0]

            time.sleep(60.0 - ((time.time() - starttime) % 60.0))
        except error:
            print("something went wrong ", error)
            exit()

main()

def upload():
    media = twitter_api.media_upload("video.mp4")
    twitter_api.update_status("im gonna cry", media_ids=[media.media_id])

    # VideoTweet = video_tweet.VideoTweet("video_resized.mp4")
    # VideoTweet.upload_init()
    # VideoTweet.upload_append()
    # VideoTweet.upload_finalize()
    # VideoTweet.tweet()


# upload()
