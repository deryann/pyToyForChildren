# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # 這是一個寫給小朋友玩的玩具
#     - 希望可以聽見一些小朋友的指令，做些搜尋相關的事情
#     - 未來希望可以做到一些網路圖片識字卡、學說話等的相關功能
#     - 網路 Py 點讀筆取代用?

from IPython.display import display_html
from IPython.core.display import display, HTML
import datetime, pytz
dt = datetime.datetime.now(tz=pytz.utc)
str_time_stamp = dt.astimezone(datetime.timezone(offset=datetime.timedelta(hours=8))).strftime('%Y%m%d_%H%M%S')

display(HTML("<style>.container { width:100% !important; }</style>"))
display_html("""
<div style="text-align:center; margin: 20px 0;">
<button onclick="$('.input, .prompt, .output_stderr, .output_error').toggle();">Toggle Code</button>
<hr/>
</div>
""", raw=True)

# +
import speech_recognition
import time
import os
import pyaudio
import wave              

# 將聲音轉成文字的fun 只需要這一小段code 
from gtts import gTTS
from pygame import mixer
def say_text(str_text):
    str_time_stamp = dt.astimezone(datetime.timezone(offset=datetime.timedelta(hours=8))).strftime('%Y%m%d_%H%M%S')
    file_name_audio = ".\cache_{}.mp3".format(str_time_stamp)
    tts=gTTS(text=str_text, lang='zh-tw')
    tts.save(file_name_audio)

    mixer.init()
    mixer.music.load(file_name_audio)
    mixer.music.play()

def Voice_To_Text():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source: 
     ## 介紹一下 with XXX as XX 這個指令
     ## XXX 是一個函數或動作 然後我們把他 的output 放在 XX 裡
     ## with 是在設定一個範圍 讓本來的 source 不會一直進行
     ## 簡單的應用，可以參考
     ## https://blog.gtwang.org/programming/python-with-context-manager-tutorial/
                                      # print 一個提示 提醒你可以講話了
        r.adjust_for_ambient_noise(source)     # 函數調整麥克風的噪音:
#         say_text("請開始說話")
#         sleep(1000)
        print("請開始說話:") 
        
        audio = r.listen(source,timeout=2)
        print("聽完了") 
     ## with 的功能結束 source 會不見 
     ## 接下來我們只會用到 audio 的結果
    try:
        Text = r.recognize_google(audio, language="zh-TW")     
              ##將剛說的話轉成  zh-TW 繁體中文 的 字串
              ## recognize_google 指得是使用 google 的api 
              ## 也就是用google 網站看到的語音辨識啦~~
              ## 雖然有其他選擇  但人家是大公司哩 當然優先用他的囉
    except r.UnknowValueError:
        Text = "無法翻譯"
    except sr.RequestError as e:
        Text = "無法翻譯{0}".format(e)
              # 兩個 except 是當語音辨識不出來的時候 防呆用的 

    return Text


### fun定義結束

##讓我們實際利用看看吧~
Text = Voice_To_Text()
print(Text)
print("end!")

# +
str_text = "你說的是"+Text+"，"
str_text+= (Text+"是不是掌這個樣子")

say_text(str_text)
import requests
import urllib.request
from bs4 import BeautifulSoup
import os
import time

from IPython.display import Image
from IPython.core.display import HTML 

str_search = Text
url = "https://www.google.com/search?q={}"
url = url.format(str_search)
photolimit = 5
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url,headers = headers) #使用header避免訪問受到限制
soup = BeautifulSoup(response.content, 'html.parser')
items = soup.find_all('img')
folder_path ='./photo/'
if (os.path.exists(folder_path) == False): #判斷資料夾是否存在
    os.makedirs(folder_path) #Create folder
for index , item in enumerate (items):

    if (item and index < photolimit ):

        html = requests.get(item.get('src')) # use 'get' to get photo link path , requests = send request

        img_name = folder_path+str_time_stamp + str(index + 1) + '.png'
        with open(img_name,'wb') as file: #以byte的形式將圖片數據寫入
            file.write(html.content)
            file.flush()

        print('第 %d 張' % (index + 1))
        display(Image(url= img_name))
        time.sleep(1)
print('Done')
# -


