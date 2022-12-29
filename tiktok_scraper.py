from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path 

class TikTokScraper:
    chrome_options = webdriver.ChromeOptions()
    service_object = Service(binary_path)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--disable-dev-shm-usage')
    PATH = chromedriver_autoinstaller.install(cwd=True)

    def __init__(self):
        self.driver = webdriver.Chrome(self.PATH, options=self.chrome_options)
        self.text = ""
        self.tiktok_user_page_url = "https://www.tiktok.com/@"

    def get_user_liked_videos(self, username):
        url = self.tiktok_user_page_url + username
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
