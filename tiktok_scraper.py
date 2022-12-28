from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TikTokScraper:
    def __init__(self):
        self.PATH = "chromedriver.exe"
        self.driver = webdriver.Chrome(self.PATH)
        self.text = ""
        self.tiktok_user_page_url = "https://www.tiktok.com/@"

    def get_user_liked_videos(self, username):
        url = self.tiktok_user_page_url + username
        self.driver.get(url)

        time.sleep(5)

        liked_button_switcher = self.driver.find_element(By.CSS_SELECTOR,  '.e1jjp0pq2')
        liked_button_switcher.click()

        time.sleep(5)

        videos = self.driver.find_elements(By.CSS_SELECTOR, '.e19c29qe7')

        print("length ", len(videos))

        video_urls = []

        for video in videos:
            video_url = video.find_element(By.CSS_SELECTOR, 'a')
            video_urls.append(video_url.get_attribute("href"))
        
        return video_urls

    def get_liked_video_url(self, tiktok_link):
        print("tiktoklink ", tiktok_link)
        self.driver.get(tiktok_link)

        time.sleep(5)

        video_link = self.driver.find_element(By.CSS_SELECTOR, 'video')

        print(video_link.get_attribute("src"))

        return video_link.get_attribute("src")

    def close(self):
        self.driver.close()
