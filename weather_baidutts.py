# encoding='utf-8'
import requests
import os
from bs4 import BeautifulSoup
import re
import datetime
import time


def gethtml(url):
    s = requests.get(url)
    return s.text


def printinfo(s):
    soup = BeautifulSoup(s.text, "html.parser")
    pattenstr = '(?<=今天)*.'
    patten = re.compile(pattenstr)
    # print(s.text)
    print(patten.findall(s.text))
    print(patten.match(s.text).group())
    print(soup.title)


def retest(html):
    aqilevelpatten = 'src="https://h5tq.moji.com/tianqi/assets/images/aqi/(\d)'
    aqilevel = re.findall(aqilevelpatten, html)[0]
    print(aqilevel)

    aqipatten = '/aqi/' + aqilevel + '\.png"\s*alt="(\d* \w*)'
    aqi = re.findall(aqipatten, html)[0]
    print(aqi)

    aboutpatten = 'wea_about clearfix">\s*<span>(\w* \w*%)</span>\s*<em>(\w*)'
    about = re.findall(aboutpatten, html)  # [('湿度 8%', '北风3级')]
    humidity = about[0][0]
    windy = about[0][1]
    print(humidity)
    print(windy)

    tippatten = ' <div class="wea_tips clearfix">\s*<span>\w*</span>\s*<em>(\w*，?\w*)'
    tip = re.findall(tippatten, html)[0]
    print(tip)

    list_weather = [aqi, humidity, windy, tip]
    today = datetime.date.today()
    print(today)
    with open("weather.txt", 'a', encoding='utf-8')as f:
        f.write(str(today) + ':')
        f.write(str(list_weather)+"\n")

    return list_weather

def tts(weather):
    #+" 湿度"weather[1]
    text="强哥 早上好 该起床啦"+"今天空气质量指数 是"+str(weather[0])+" 风力 为"+str(weather[2])+" 肚子提醒你，"+str(weather[3])
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit'
                          '/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                          'i/537.36',
        }
    url='http://tts.baidu.com/text2audio?idx=1&tex=(%s)&cuid=baidu_speech_demo&cod=2&lan=zh&ctp=1&pdt=1&spd=5&per=4&vol=5&pit=5'%text
    #url = 'http://tts.baidu.com/text2audio?idx=1&tex=%E5%BC%BA%E5%93%A5%20%E6%97%A9%E4%B8%8A%E5%A5%BD%20%E8%AF%A5%E8%B5%B7%E5%BA%8A%E5%95%A6&cuid=baidu_speech&cod=2&lan=zh&ctp=1&pdt=1&spd=5&per=4&vol=4&pit=5'
    res = requests.get(url, headers=headers)
    with open('1.mp3', 'wb') as f:
        #print(res.content)
        f.write(res.content)
if __name__ == '__main__':
    #os.chdir('d:\\')
    url = 'http://tianqi.moji.com/'
    html = gethtml(url)
    weather = retest(html)
    tts(weather)
