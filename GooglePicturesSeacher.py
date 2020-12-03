# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import requests
import urllib.request
from bs4 import BeautifulSoup
import os
import time

from IPython.display import Image
from IPython.core.display import HTML 
# -

# # 爬圖機
#     - 網路 Google 後，將前 k 名的資料存下來

# +
lst = ['大象',
      '犀牛',
      '狗',
      '貓',
      '臘腸狗',
      '紅貴賓',
      '黃金獵犬',      ]

def save_data_into_folder(lst_name):
    for str_text_item in lst_name:
        str_search = str_text_item
        url = "https://www.google.com/search?q={}&source=lnms&tbm=isch"
        url = url.format(str_search)
        photolimit = 3
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url,headers = headers) #使用 header 避免訪問受到限制
        print(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('img')
        
        folder_path ='./photo_cache/'
        
        if (os.path.exists(folder_path) == False): #判斷資料夾是否存在
            os.makedirs(folder_path) #Create folder
        
        for index , item in enumerate (items):
            if (item and index < photolimit ):
                if not 'http'  in item.get('src') :
                    continue
                html = requests.get(item.get('src')) # use 'get' to get photo link path , requests = send request
                img_name = folder_path+str_text_item+'_' + str(index + 1) + '.png'
                with open(img_name,'wb') as file: #以byte的形式將圖片數據寫入
                    file.write(html.content)
                    file.flush()
                display(Image(url= img_name))
                time.sleep(1)
    print('Done')


# -

save_data_into_folder(lst)

lst = ['亞洲女藝人', 
      '亞洲女明星',
      '亞洲女明星 全身照']

save_data_into_folder(lst)
