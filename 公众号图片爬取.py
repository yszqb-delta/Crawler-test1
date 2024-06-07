from tqdm import tqdm
import requests
import time
import bs4
import os

desk = os.path.join(os.path.expanduser('~'), "Desktop")
url = str(input("请输入公众号网址:"))
tit = "rich_media_title"
class_ = "rich_pages wxw-img"

page = requests.get(url)
bs = bs4.BeautifulSoup(page.text, 'lxml')

title = bs.find("h1", attrs={"class":tit})
title = str(title.text)[14:37]
print("TITLE:", title)
print("FILE PATH:", desk)

path = os.path.join(desk, title)
try:
    os.mkdir(path)
except FileExistsError as e:
    print("文件夹已存在，内容会直接覆盖")

os.chmod(path, 0o777)

img = bs.find_all("img", attrs={"class": class_})

# print(img)

img_links = []
for i in img:
    img_links.append(i["data-src"])

# print(img_links)
progress_bar = tqdm(total=len(img_links), desc="完成进度", unit="item")

for index, img_url in enumerate(img_links):
    progress_bar.update(1)
    response = requests.get(img_url)
    file_name = f'image_{index}.jpg'
    file_path = os.path.join(path, file_name)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    time.sleep(0.1)

progress_bar.close()

"""
#这是一个可以用于下载微信公众号图片的爬虫程序
#This is a crawler that can be used to download pictures of WeChat official accounts.

中文:

  ·这个程序可以用于爬取微信公众号内的图片
  ·适用于教材下载等
  ·第三方库: tqdm、requests、bs4

English:
  ·This program can be used to crawl images from WeChat official accounts.
  ·It is suitable for downloading textbooks, etc.
  ·Third-party libraries: tqdm、requests、bs4
"""
