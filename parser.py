import time
import uuid

import requests
from bs4 import BeautifulSoup

import json

from datetime import datetime
from db_conncetion import DataBase


def chek_ecb():
    url = requests.get('https://www.ecb.europa.eu/rss/press.html')
    soup = BeautifulSoup(url.text, 'xml')
    aticles_card = soup.find_all('item')
    ecb_news = {}
    for article in aticles_card:
        article_title = article.find('title').text
        article_link = article.find('guid').text
        article_data_time = article.find('pubDate').text.replace(' +0100', '')
        ecb_news[uuid.uuid4()] = {
            'article_link': article_link,
            'article_title': article_title,
            'article_data_time': article_data_time,
        }
    return ecb_news


def check_forcklog():
    url = requests.get('https://forklog.com/news')
    soup = BeautifulSoup(url.text, 'xml')
    article_card = soup.find_all('div', class_='cell')
    forklog_news = {}
    for articles in article_card:
        post_link = articles.find('div', class_='post_item')
        article_link = post_link.find('a').get('href')
        article_title = articles.find('div', class_='text_blk').text
        article_data_time = post_link.get('data-full_datetime')
        forklog_news[uuid.uuid4()] = {
            'article_link': article_link,
            'article_title': article_title,
            'article_data_time': article_data_time,
        }
    return forklog_news


def check_reuters():
    url = requests.get('https://www.reuters.com/world/')
    soup = BeautifulSoup(url.text, 'lxml')
    article_card = soup.find_all('li', class_='story-collection__story__LeZ29')
    reuters_news = {}
    for article in article_card:
        data_time = article.find('time').get('datetime')
        date_from_iso = datetime.fromisoformat(data_time.replace('Z', ''))
        article_data_time = str(date_from_iso)

        article_title = article.find_next('span').find_next('span').find_next('span').text
        article_link = 'https://www.reuters.com' + article.find('a').get('href')
        reuters_news = {
            'article_link': article_link,
            'article_title': article_title,
            'article_data_time': article_data_time,
        }
        return reuters_news


def check_news():
    ecb = chek_ecb()
    forklog = check_forcklog()
    reuters = check_reuters()
    newses = {**ecb, **forklog, **reuters}
    for k, v in newses.items():
        article_link = v['article_link']
        article_title = v['article_title']
        article_data_time = v['article_data_time']
        with DataBase() as db:
            db.execute(f'INSERT INTO news VALUES ("{article_title}", "{article_link}", "{article_data_time}")')

        try:
            with DataBase() as db:
                result = db.cur.execute(f'SELECT link FROM news WHERE link="{article_link}"').fetchone()
                if article_link in str(result):
                    continue
                else:
                    db.execute(f'INSERT INTO news VALUES ("{article_title}", "{article_link}", "{article_data_time}")')
                    fresh = {
                        'article_link': article_link,
                        'article_data_time': article_data_time
                    }
                    return fresh
        except Exception as err:
            return print(err)


def main():
    #chek_ecb()
    #check_forcklog()
    check_reuters()
    check_news()


if __name__ == '__main__':
    main()
