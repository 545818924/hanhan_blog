# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

def getPage(url):
    try:
        r = requests.get(url)
        r.encoding = 'utf-8'
        r.raise_for_status()
        return r.text
    except:
        print('爬取失败')


def getPageDetail(url):
    html = getPage(url)
    soup = BeautifulSoup(html, 'lxml')
    dt = datetime.strptime(soup.select('.time')[0].text,'(%Y-%m-%d %H:%M:%S)')  #获取时间
    date = dt.strftime('%Y-%m-%d')  #格式化时间
    title = soup.select('title')[0].text #获取标题
    content = ''.join([i for i in soup.select('.articalContent')[0].text.split()])  #获取正文
    dict = {'date': date, 'title': title, 'content': content}
    return dict


def getUrlList(url): 
    html = getPage(url)
    soup = BeautifulSoup(html,'lxml')
    regex = re.compile("http://blog.sina.com.cn/s/blog_4701280b(.*?).html")
    return [i['href'] for i in soup.findAll('a',attrs={'href':regex})]



def main():
    page_list = 'http://blog.sina.com.cn/s/articlelist_1191258123_0_{}.html'
    result = []
    for t in range(1,8):  # 博客总7页
        urlList = getUrlList(page_list.format(t))
        for i in urlList:
            result.append(getPageDetail(i))
    return result

if __name__ == '__main__':
	main()
	result = main()
	result.sort(key=lambda x:x['date'])
	with open('hanhan.txt', 'a', encoding='utf-8') as f:
		if json.dump(result,f, indent=4, ensure_ascii=False):
			print("保存成功", f)


# import pandas
# df = pandas.DataFrame(result)
# df.head()


# df.to_excel('hanhan.xlsx')


# import sqlite3
# with sqlite3.connect('hanhan.sqlite') as db:
#     df.to_sql('hanhan', con=db)

# with sqlite3.connect('hanhan.sqlite') as db:
#     df2 = pandas.read_sql_query('SELECT * FROM hanhan', con=db)
# df2

# import pymongo
# client = pymongo.MongoClient('localhost')
# db = client['hanhan']
# table = db['hanhan']

# def save_to_mongo(result):
#     if table.insert_many(result):
#         print('保存到Mongo成功')
#     else:
#         return False
# save_to_mongo(result)

