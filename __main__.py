import os
from dotenv import load_dotenv
import tweepy
import time
import tiktok_scraper

load_dotenv()

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

twitter_api = tweepy.API(auth)

def main():
    starttime = time.time()
    last_uploaded_video = ''

    twitter_api.verify_credentials()
    print("Authentication OK")

    while True:
        try:
            scraper = tiktok_scraper.TikTokScraper();
            video_urls = scraper.get_user_liked_videos("https://www.tiktok.com/@gentij1")

            last_video_index = video_urls.index(last_uploaded_video) if last_uploaded_video in video_urls else 0

            if last_video_index != 0:
                new_liked_videos = video_urls[:last_video_index]

                print(new_liked_videos)

                for video_url in reversed(new_liked_videos):
                    twitter_api.update_status(video_url)
                
            last_uploaded_video = video_urls[0]
            time.sleep(60.0 - ((time.time() - starttime) % 60.0))
        except error:
            print(error)

main()
