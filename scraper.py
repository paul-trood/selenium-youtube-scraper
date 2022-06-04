# The file was created and runs from Replit
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

"""There is an error with extracting all the videos when not given enought time for the page to completely load.
Time module allows for the web page to completely load, and extract all elements"""
import time

import datetime
import pytz

import smtplib
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
    channel_div = video.find_element(By.CLASS_NAME, "ytd-channel-name")
    channel_name = channel_div.text

    description = video.find_element(By.ID, "description-text").text
  
# Iterate through videos to extract the views and the date posted
    views = video.find_element(By.XPATH,'.//*[@id="metadata-line"]/span[1]').text
    post_date = video.find_element(By.XPATH,'.//*[@id="metadata-line"]/span[2]').text

# Current time (local timezone) of the webscraping
    date_scraped = datetime.datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')

# Return a dictionary of the scraped elements
    return {
        "title": title,
        "url": url,
        "channel": channel_name,
        "description": description,
        "views": views,
        "post_date": post_date,
        "date_scraped":date_scraped
    }

def send_email(body):
  try:
    server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server_ssl.ehlo()   

    sender_email = "webscraperutube@gmail.com"
    receiver_email = "webscraperutube@gmail.com"
    sender_password = os.environ["my_password"]
    
    subject = "YouTube Trending Videos"
    
    email_text = f"""
    From: {sender_email}
    To: {receiver_email}
    Subject: {subject}
    
    {body}
    """

    server_ssl.login(sender_email, sender_password)
    server_ssl.sendmail(sender_email, receiver_email, email_text)
    server_ssl.close()

  except:
      print("Something went wrong...")
  

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
  videos_dataframe = pd.DataFrame(videos_data)
  
  # Format the date of scraping, local time is united states eastern timezone
  date = pd.Timestamp("today", tz ="US/Eastern").strftime('%Y-%m-%d')
  videos_dataframe.to_csv(f"trending_{date}.csv", index=None)

  print("Send an email with the results")
  body = json.dumps(videos_data, indent = 2)

  # Send email with json data of scraped videos
  send_email(body)
  print("Finished")