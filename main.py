#%%
import requests
from bs4 import BeautifulSoup
import os
from time import sleep

albums_folders = []
# %%
site = input("site:")
# 321066 321881 322157
users = input("comma separated:").split(',')
for user in users:
    a = requests.get(f"https://{site}.com/album/user/{user}")
    html = BeautifulSoup(a.content, features="html.parser")

    album = html.find("div", {"class":"album-title"})
    if album:
        link = album.find('a')
        if link:
            href = link.get("href")
            albums_folders.append(f"https://{site}.com{href}")



# %%
images_links = set()
for alb in albums_folders:
    a = requests.get(alb)
    html = BeautifulSoup(a.content, features="html.parser")
    images = html.find_all("div", {"class":"image-block"})
    for img in images:
        img_link = img.find('a').get("data-src")
        images_links.add(img_link)

# %%
folder_path = 'images'

# Check if the folder exists, create it if not
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f'Created directory: {folder_path}')
else:
    print(f'Directory already exists: {folder_path}')

for i, image_url in enumerate(images_links):
    image_path = os.path.join(folder_path, f'image{str(i).zfill(2)}.jpg')
    response = requests.get('https:'+image_url)
    with open(image_path, 'wb') as f:
        # Write the content of the image to the file
        f.write(response.content)
    sleep(0.2)

# %%
