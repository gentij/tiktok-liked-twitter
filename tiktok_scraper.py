from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TikTokScraper:
    def __init__(self):
        self.PATH = "chromedriver.exe"
        self.driver = webdriver.Chrome(self.PATH)
        self.text = ""

    def get_user_liked_videos(self, url):
        self.driver.get(url)

        liked_button_switcher = self.driver.find_element(By.CSS_SELECTOR,  '.e1jjp0pq2')
        liked_button_switcher.click()

        time.sleep(5)

        videos = self.driver.find_elements(By.CSS_SELECTOR, '.e19c29qe7')

        print("length ", len(videos))

        video_urls = []

        for video in videos:
            video_url = video.find_element(By.CSS_SELECTOR, 'a')
            video_urls.append(video_url.get_attribute("href"))

        self.driver.close()
        
        return video_urls