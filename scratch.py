print("testing")

import requests
from bs4 import BeautifulSoup

# Requests library doesn't execute JavaScript
response = requests.get(youtube_url)
print("Status Code", response.status_code)
#print("Output", response.text[:1000])

# with open("trending.html", "w") as f:
#   f.write(response.text)

doc = BeautifulSoup(response.text, "html.parser")

print("Page title", doc.title.text)

# Find all video divs
video_divs = doc.find_all("div", class_= "ytd-video-renderer")

print(f"Found {len(video_divs)} videos")