import time
import uuid

import requests
from bs4 import BeautifulSoup

import json

from datetime import datetime


def chek_ecb():
    with open('ecb_news.json') as file:
        news_dict = json.load(file)
    url = requests.get('https://www.ecb.europa.eu/rss/press.html')
    soup = BeautifulSoup(url.text, 'xml')
    aticles_card = soup.find_all('item')
    ecb_news = {}
    fresh_ecb = {}
    for article in aticles_card:
        article_title = article.find('title').text
        article_link = article.find('guid').text
        article_data_time = article.find('pubDate').text
        ecb_news[article_link] = {
            'article_title': article_title,
            'article_link': article_link,
            'article_data_time': article_data_time.replace(' +0100', '')
        }
        if article_link not in news_dict:
            fresh_ecb[article_link] = {
                'article_title': article_title,
                'article_link': article_link,
                'article_data_time': article_data_time.replace(' +0100', '')
            }
    with open('ecb_news.json', 'w') as file:
        json.dump(ecb_news, file, indent=4, ensure_ascii=False)
    return fresh_ecb


def check_forcklog():
    with open('forklog_news.json') as file:
        news_dict = json.load(file)
    url = requests.get('https://forklog.com/news')
    soup = BeautifulSoup(url.text, 'xml')
    article_card = soup.find_all('div', class_='cell')
    forklog_news = {}
    fresh_forklog = {}
    for articles in article_card:
        post_link = articles.find('div', class_='post_item')
        article_link = post_link.find('a').get('href')
        article_title = articles.find('div', class_='text_blk').text
        article_date_time = post_link.get('data-full_datetime')
        forklog_news[article_link] = {
            'article_title': article_title,
            'article_link': article_link,
            'article_data_time': article_date_time
        }
        if article_link not in news_dict:
            fresh_forklog[article_link] = {
                'article_title': article_title,
                'article_link': article_link,
                'article_data_time': article_date_time
            }
    with open('forklog_news.json', 'w') as file:
        json.dump(forklog_news, file, indent=4, ensure_ascii=False)
    return fresh_forklog


def check_reuters():
    with open('reuters_news.json') as file:
        news_dict = json.load(file)
    url = requests.get('https://www.reuters.com/world/')
    soup = BeautifulSoup(url.text, 'lxml')
    article_card = soup.find_all('li', class_='story-collection__story__LeZ29')
    reuters_news = {}
    fresh_reuters = {}
    for article in article_card:
        data_time = article.find('time').get('datetime')
        date_from_iso = datetime.fromisoformat(data_time.replace('Z', ''))
        article_data_time = str(date_from_iso)

        article_title = article.find_next('span').find_next('span').find_next('span').text
        article_link = 'https://www.reuters.com' + article.find('a').get('href')
        reuters_news[article_link] = {
            'article_title': article_title,
            'article_link': article_link,
            'article_data_time': article_data_time
        }
        if article_link not in news_dict:
            fresh_reuters[article_link] = {
                'article_title': article_title,
                'article_link': article_link,
                'article_data_time': article_data_time
            }
    with open('reuters_news.json', 'w') as file:
        json.dump(reuters_news, file, indent=4, ensure_ascii=False)
    return fresh_reuters


def main():
    chek_ecb()
    check_reuters()
    check_forcklog()


if __name__ == '__main__':
    main()
