# -*- coding:utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup
from contextlib import closing
from multiprocessing.dummy import Pool as ThreadPool

def download(url,name,dir_name):
    dn_url = url
    filename = './'+ dir_name + '/' + name + '.mp4'
    if os.path.exists(filename):
        print(name + '已存在')
    else:
        print(name + '开始下载')
        with closing(requests.get(dn_url, stream=True)) as response:
            chunk_size = 1024   
            if response.status_code == 200:
                with open(filename, "wb") as file:  
                    for data in response.iter_content(chunk_size=chunk_size):  
                        file.write(data)  
            else:
                print('链接异常')
        print(name + '完成')

def getVedioAddr(de_url):    
    detail_url = de_url
    r = requests.get(url = detail_url)
    r.encoding = 'utf-8'
    detail_bf = BeautifulSoup(r.text, 'lxml')
    flag = 0
    link = ''
    for each_url in detail_bf.find('div',class_= 'bofang'):   
        if flag == 0:
            link = each_url.get('data-vid')
            link = link[:-4]
            flag = 1
    return link

if __name__ == '__main__':
    search_keyword = '黄金神威 OAD'
    search_url = 'http://www.yhdm.io/search'
    search_url = search_url + '/' + search_keyword
    serach_params = {
        'm': 'search'
    }
    serach_headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Mobile Safari/537.36',
        'Referer': 'http://www.yhdm.io/search/',
        'Origin': 'http://www.yhdm.io',
        'Host': 'www.yhdm.io'
    }


    video_dir = ''

    r = requests.post(url=search_url, params=serach_params, headers=serach_headers)

    r.encoding = 'utf-8'
    server = 'http://www.yhdm.io'
    search_html = BeautifulSoup(r.text, 'html.parser')
    search_lists = search_html.find('div', class_='lpic')
    search_lists = search_lists.find('ul')
    search_lists = search_lists.find_all('a')

    for search_list in search_lists:
        if search_list.text == '':
            flag = 1
        if flag == 1 and search_list.text != '':
            search_url = server + search_list.get('href')
            search_name = search_list.text
            print(search_name)
            video_dir = search_name
            if search_name not in os.listdir('./'):
                os.mkdir(search_name)

            detail_url = search_url
            r = requests.get(url = detail_url)
            r.encoding = 'utf-8'
            detail_bf = BeautifulSoup(r.text, 'lxml')
            detail_lists = detail_bf.find('div', class_='movurl')
            detail_lists = detail_lists.find_all('a')

            for detail_list in detail_lists:
                number_name = detail_list.text
                number_url = server + detail_list.get('href')
                link = getVedioAddr(number_url)
                download(link,number_name,search_name)
            
            flag = 0

    print('全部下载完成')
