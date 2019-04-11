# -*- coding: utf-8 -*-
import datetime
import os
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def GetFakeHeader(ref):
    headers = {
        'User-Agent': UserAgent().random,
        'Referer': ref
    }
    return headers


def GetCode(link, hed, cok):
    response = requests.get(link, headers=hed, cookies=cok)
    html = response.content.decode("utf-8")
    return html


cookie = {
    "p_ab_id": "8",
    "p_ab_id_2": "2",
    "p_ab_d_id": "1521913077",
    "_ga": "GA1.2.1805434725.1548209430",
    "user_lang": "zh"
}

url = 'https://www.pixivision.net/zh/c/illustration'  # 这是Page1,下一页为*/?p=2

#td = time.strftime('%Y.%m.%d',time.localtime(time.time()))
td = datetime.datetime.now().strftime('%Y.%m.%d')   #Get today
yd = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y.%m.%d')    #Get Yesterday
hreflist, titlelist = [], []
td_push_count, yd_push_count = 0, 0

soup = BeautifulSoup(GetCode(url, GetFakeHeader(''), cookie), 'lxml')
for a, ptime in zip(soup.find_all(name='a', attrs={'data-gtm-action': 'ClickTitle'}, limit=20), soup.find_all('time')):
    href = 'https://www.pixivision.net' + a.get('href')
    title = a.get_text()
    hreflist.append(href)
    titlelist.append(title)
    td_push_count = td_push_count + 1 if ptime.string == td else td_push_count
    yd_push_count = yd_push_count + 1 if ptime.string == yd else yd_push_count
if td_push_count:
    print('到目前为止Pixivision今日推送了%d篇文章' % td_push_count)
    for c in range(0, td_push_count):
        print(hreflist[c])
        print(titlelist[c])
        soup = BeautifulSoup(
            GetCode(hreflist[c], GetFakeHeader(''), cookie), 'lxml')
        folderpath = os.getcwd() + '\\' + titlelist[c] + '\\'
        is_exist = os.path.exists(folderpath)
        if not is_exist:
            os.mkdir(folderpath)
        for img in soup.find_all(name='img', attrs={"class": "am__work__illust"}):
            illustsrc = img.attrs['src'].replace(
                'https://i.pximg.net/c/768x1200_80/img-master/', 'https://i.pximg.net/img-original/')
            illustsrc = illustsrc.replace('_master1200.jpg', '.jpg')
            r = requests.get(
                illustsrc, headers=GetFakeHeader(url), cookies=cookie)
            if r.status_code == 404:
                illustsrc = illustsrc.replace('.jpg', '.png')
                r = requests.get(
                    illustsrc, headers=GetFakeHeader(url), cookies=cookie)
            print(illustsrc)
            with open(folderpath + os.path.basename(illustsrc), 'wb') as f:
                f.write(r.content)
            time.sleep(2.5)
else:
    anw = input('到目前为止Pixivision今日暂时没有推送,是否要下载昨日推送[Y/N]?\n')
    if anw in ('y', 'Y'):
        for cc in range(0, yd_push_count):
            print(hreflist[td_push_count + cc])
            print(titlelist[td_push_count + cc])
            soup = BeautifulSoup(
                GetCode(hreflist[td_push_count + cc], GetFakeHeader(''), cookie), 'lxml')
            folderpath = os.getcwd() + '\\' + \
                titlelist[td_push_count + cc] + '\\'
            is_exist = os.path.exists(folderpath)
            if not is_exist:
                os.mkdir(folderpath)
            for img in soup.find_all(name='img', attrs={"class": "am__work__illust"}):
                illustsrc = img.attrs['src'].replace(
                    'https://i.pximg.net/c/768x1200_80/img-master/', 'https://i.pximg.net/img-original/')
                illustsrc = illustsrc.replace('_master1200.jpg', '.jpg')
                r = requests.get(
                    illustsrc, headers=GetFakeHeader(url), cookies=cookie)
                if r.status_code == 404:
                    illustsrc = illustsrc.replace('.jpg', '.png')
                    r = requests.get(
                        illustsrc, headers=GetFakeHeader(url), cookies=cookie)
                print(illustsrc)
                with open(folderpath + os.path.basename(illustsrc), 'wb') as f:
                    f.write(r.content)
                time.sleep(2.5)
    else:
        print('程序即将退出...')
