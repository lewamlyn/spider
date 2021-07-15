# -*-coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

def get_new(name):
    url = 'https://copymanga.net/comic/' + name
    req = requests.get(url = url)
    req.encoding = 'utf-8'
    html = req.text
    bf = BeautifulSoup(html, 'html.parser')
    texts = bf.find_all('title')
    return str(texts).split('-')[1] + '-' + str(texts).split('-')[2]

def get_back(file_name):
    old = []
    try:
        with open(file_name, mode='r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                old.append(line)
    except:
        with open(file_name, mode='w') as f:
            print('无本地存储信息')
    return old

if __name__ == '__main__':

    spider_lists = ['modujingbingdenuli','beicandeqilingzhe','zhongmodenvwushen']
    old_lists = get_back('./back.txt')
    update_lists = []
    print(old_lists)

    # 获取信息，更新信息
    flag = False
    f = open('./back.txt','w+')
    fu = open('./update.txt','w+')
    for i in range(len(spider_lists)):
        new = get_new(spider_lists[i])
        f.write(str(new)+'\n')
        if i >= len(old_lists):
            flag = True
            fu.write(str(new)+'\n')
        elif new != old_lists[i]:
            flag = True
            fu.write(str(new)+'\n')           
    f.close()
    fu.close()

    # 更新状态
    fs = open('./update','w+')
    if flag:
        fs.write('true')
    else:
        fs.write('false')
    fs.close()
