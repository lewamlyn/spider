# -*-coding:utf-8 -*-
import requests
import os
import re
import math
from bs4 import BeautifulSoup
from contextlib import closing
from tqdm import tqdm
import time

# 初始化
search_name = '电锯人'
search_uid = '169573'

# 创建保存目录
save_dir = search_name
if save_dir not in os.listdir('./'):
    os.mkdir(save_dir)

# search 
server = 'https://www.acfun.cn/'
search_url = 'https://www.acfun.cn/u/' + search_uid
search_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    'accept-language': 'zh-CN,zh;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'referer': search_url,
    'accept': '*/*'}

# 获取文章总数目
sess = requests.Session()
r = sess.get(url=search_url, headers=search_headers)
html = BeautifulSoup(r.text, 'html.parser')
tags = html.find('ul',class_='tags')
counts = tags.find_all('span')
temp = 0
for count in counts:
    temp += 1
    if temp == 2:
        article_count = int(count.text)
        break
print('共 ' + count.text + ' 篇文章\n')

# 获取漫画标题和链接
print('获取漫画标题和链接中\n')
pageSize = 100
pageTotal = math.ceil(article_count/pageSize)
chapter_names = []
chapter_urls = []
for page in range(1, pageTotal + 1):    
    search_params = {'page': page,
                    'pageSize': pageSize,
                    "ajaxpipe": 1,
                    'quickViewId': 'ac-space-article-list',
                    'order': 'newest',
                    'type': 'article'}
    r = sess.get(url=search_url, headers=search_headers, params=search_params, verify=False)
    bs = BeautifulSoup(r.text, 'lxml')
    cartoon_list = bs.find_all('a')

    for cartoon in cartoon_list:      
        name = cartoon.text
        if name.find(search_name) > 0 :
            href = cartoon.get('href')
            url = server + href[3:-2]
            chapter_names.insert(0, name)
            chapter_urls.insert(0, url) 
    
    # 找到第一章，中断获取
    if chapter_names:
        if chapter_names[0].find('#01') > 0:
            break

print('\n获取漫画标题和链接完成\n')
time.sleep(0.1)

# 下载漫画 
for i, url in enumerate(tqdm(chapter_urls)):
    name = chapter_names[i]
    chapter_save_dir = os.path.join(save_dir, name)
    if name not in os.listdir(save_dir):
        os.mkdir(chapter_save_dir)
        r = sess.get(url=url, headers=search_headers)
        html = BeautifulSoup(r.text, 'lxml')
        script = html.find('div',class_='main')
        script_info = script.find('script')
        pics = re.findall(r'parts.*?superUbb', str(script_info))

        pics = re.findall(r'imgs.*?\\',str(pics))   
        pic_url =[]
        for pic in pics:
            url = 'https://' + pic[:-1]
            pic_url.append(url)
        
        for idx, pic in enumerate(pic_url):
            url = pic
            pic_name = '%03d.png' % (idx + 1)
            pic_save_path = os.path.join(chapter_save_dir, pic_name)
            with closing(requests.get(url, stream = True)) as response:  
                chunk_size = 1024  
                content_size = int(response.headers['content-length'])  
                if response.status_code == 200:
                    with open(pic_save_path, "wb") as file:  
                        for data in response.iter_content(chunk_size=chunk_size):  
                            file.write(data)  
                else:
                    print(name + ' ' +pic_name + ' 链接异常')
        time.sleep(10)
