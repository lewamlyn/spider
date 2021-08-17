# -*-coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urllib import parse

def get_new(name):
    url = 'https://copymanga.net/comic/' + name
    req = requests.get(url = url)
    req.encoding = 'utf-8'
    html = req.text
    bf = BeautifulSoup(html, 'html.parser')
    texts = bf.find_all('title')
    return str(texts).split('-')[1][:-2] + '-' + str(texts).split('-')[2]

def get_back(file_name):
    old = []
    try:
        with open(file_name, 'r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                old.append(line)
    except:
        with open(file_name, 'w') as f:
            print('无本地存储信息')
    return old

if __name__ == '__main__':

    spider_lists = ['modujingbingdenuli','beicandeqilingzhe','zhongmodenvwushen', 'nvyouchengshuang', 'zaiyishijiemigongkaihougong','satanophany','hydxjxrwgb','yaosanjiao','grandblue','guaishou8hao']
    old_lists = get_back('./back.txt')
    print(old_lists)

    # 获取信息，更新信息
    f = open('./back.txt','w+')
    fu = open('./update.txt','w+')
    for i in range(len(spider_lists)):
        try:
            new = get_new(spider_lists[i])
        except:
            new = old_lists[i]
            print('get new unsuccessfully')
        url = parse.quote(str(new))
        f.write(url+ '\n')
        if i >= len(old_lists):
            fu.write(url + '\n')
        elif url != old_lists[i]:
            fu.write(url + '\n')           
    f.close()
    fu.close()

    with open("./runtimes.txt", "r", encoding="utf-8") as f:
        x = f.read()
    x = str(int(x) + 1)
    with open("./runtimes.txt", "w", encoding="utf-8") as f:
        f.write(x)
    f.close()
    print("successfully")
