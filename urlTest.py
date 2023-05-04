#%%
import requests
from bs4 import BeautifulSoup
import json
import os
#%%
url = "https://spdf.gsfc.nasa.gov/pub/data/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

dirs = []
for link in soup.find_all("a"):
    if link.get("href").endswith("/"):
        dirs.append(link.get("href"))

with open("dirs.json", "w") as f:
    json.dump(dirs, f)
# %%
url = "https://spdf.gsfc.nasa.gov/pub/data/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

dirs = []
for link in soup.find_all("a"):
    if link.get("href").endswith("/"):
        dirs.append(link.get("href"))

with open("dirsw.json", "w") as f:
    json.dump(dirs, f)
# %%
