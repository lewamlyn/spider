import requests
from urllib import parse
import sys
from xpinyin import Pinyin

def send2wechat(send_key,content):
    api = "https://sc.ftqq.com/" + send_key + ".send"
    title = u"漫画更新"
    data = {
      "text":title,
      "desp":content
    }
    req = requests.post(api,data = data)

def get_update(file_name):
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

def get_url(update):
    p = Pinyin() 
    name = parse.unquote(update).split('-')[0]
    url = 'https://copymanga.net/comic/' + p.get_pinyin(name,'')
    return url

if __name__ == '__main__':
    update_lists = get_update('update.txt')
    print(update_lists)
    content = ''
    if len(update_lists) > 0:
        for update in update_lists:
            content =  content + '## ' +  '[' +  parse.unquote(update) + '](' + get_url(update)  + ')\n'
        print(content)
        try:
            send2wechat(str(sys.argv[1]),content)
            print('已向微信发送更新信息')
        except:
            print(content)
            print('发送失败')
    else:
        print('无更新')        
