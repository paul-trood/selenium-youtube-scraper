from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
"""Error with extracting all the videos.
Time command allows for the web page to completely load, and extract all elements"""
import time

import pandas as pd

# YouTube webpage url for the top trending videos
youtube_url = "https://www.youtube.com/feed/trending"


# Chromium driver options
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_videos(driver):
    video_div_tag = "ytd-video-renderer"
    driver.get(youtube_url)

    # Time command set to 5 seconds for proper webpage loading
    time.sleep(5)

    videos = driver.find_elements(By.TAG_NAME, video_div_tag)
    return videos


# Parse all the videos of top trending youtube
def parse_video(video):
    title_tag = video.find_element(By.ID, "video-title")
    title = title_tag.text
    url = title_tag.get_attribute("href")

    thumbnail_tag = video.find_element(By.TAG_NAME, "img")
    thumbnail_url = thumbnail_tag.get_attribute("src")

    channel_div = video.find_element(By.CLASS_NAME, "ytd-channel-name")
    channel_name = channel_div.text

    description = video.find_element(By.ID, "description-text").text

# Iterate through videos to extract the views and the date posted
    views = video.find_element(By.XPATH,'.//*[@id="metadata-line"]/span[1]').text
    post_date = video.find_element(By.XPATH,'.//*[@id="metadata-line"]/span[2]').text


# Return a dictionary of the scraped elements
    return {
        "title": title,
        "url": url,
        "thumbnail_url": thumbnail_url,
        "channel": channel_name,
        "description": description,
        "views": views,
        "post_date": post_date
    }

if __name__ == "__main__":
    print("Creating driver")
    driver = get_driver()

    print("Fetching the trending videos")

    videos = get_videos(driver)

    print("Get the video divs")

    print(f"Found {len(videos)} videos")

    print("Parsing the top 10 videos")
    # title, url, thumbnail_url, url, channel
    videos_data = [parse_video(video) for video in videos[:10]]

    print(videos_data)

    # Save the dictionary to a pandas dataframe
    print("Save data to csv using pandas")
    videos_dataframe = pd.DataFrame(videos_data)
    print(videos_dataframe)
    videos_dataframe.to_csv("trending.csv", index=None)
