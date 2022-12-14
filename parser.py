import requests
from bs4 import BeautifulSoup


from datetime import datetime
from db_conncetion import DataBase


def chek_ecb():
    url = requests.get('https://www.ecb.europa.eu/rss/press.html')
    soup = BeautifulSoup(url.text, 'xml')
    aticles_card = soup.find_all('item')
    for article in aticles_card:
        article_title = article.find('title').text
        article_link = article.find('guid').text
        article_data_time = article.find('pubDate').text.replace(' +0100', '')
        split_list = article_link.split('://')
        with DataBase('news.db') as db:
            try:
                check = db.execute(f'select link from news where link = ("{split_list[1]}")').fetchone()
                if check is None:
                    db.execute(f'INSERT INTO news(title, url, link, data_time) VALUES ("{article_title}",'
                               f' "{split_list[0]}",'
                               f'"{split_list[1]}",'
                               f'"{article_data_time}")')
                for test in check:
                    if split_list[1] in test:
                        print('Yes')
                    else:
                        print('No')
                        db.execute(f'INSERT INTO news(title, url, link, data_time) VALUES ("{article_title}",'
                                   f' "{split_list[0]}",'
                                   f'"{split_list[1]}",'
                                   f'"{article_data_time}")')
            except Exception as err:
                print(f' FAILED :{err}')


def check_forcklog():
    url = requests.get('https://forklog.com/news')
    soup = BeautifulSoup(url.text, 'xml')
    article_card = soup.find_all('div', class_='cell')
    for articles in article_card:
        post_link = articles.find('div', class_='post_item')
        article_link = post_link.find('a').get('href')
        article_title = articles.find('div', class_='text_blk').text
        article_data_time = post_link.get('data-full_datetime')
        split_list = article_link.split('://')
        with DataBase('news.db') as db:
            try:
                check = db.execute(f'select link from news where link = ("{split_list[1]}")').fetchone()
                if check is None:
                    db.execute(f'INSERT INTO news(title, url, link, data_time) VALUES ("{article_title}",'
                               f' "{split_list[0]}",'
                               f'"{split_list[1]}",'
                               f'"{article_data_time}")')
                for test in check:
                    if split_list[1] in test:
                        print('Yes')
                    else:
                        print('No')
                        db.execute(f'INSERT INTO news(title, url, link, data_time) VALUES ("{article_title}",'
                                   f' "{split_list[0]}",'
                                   f'"{split_list[1]}",'
                                   f'"{article_data_time}")')
            except Exception as err:
                print(f' FAILED :{err}')


def check_reuters():
    url = requests.get('https://www.reuters.com/world/')
    soup = BeautifulSoup(url.text, 'lxml')
    article_card = soup.find_all('li', class_='story-collection__story__LeZ29')
    for article in article_card:
        data_time = article.find('time').get('datetime')
        date_from_iso = datetime.fromisoformat(data_time.replace('Z', ''))
        article_data_time = str(date_from_iso)
        article_title = article.find_next('span').find_next('span').find_next('span').text
        article_link = 'https://www.reuters.com' + article.find('a').get('href')
        split_list = article_link.split('://')
        # check update in
        with DataBase('news.db') as db:
            try:
                check = db.execute(f'select link from news where link = ("{split_list[1]}")').fetchone()
                if check is None:
                    db.execute(f'INSERT INTO news(title, url, link, data_time) VALUES ("{article_title}",'
                               f' "{split_list[0]}",'
                               f'"{split_list[1]}",'
                               f'"{article_data_time}")')
                for test in check:
                    if split_list[1] in test:
                        print('Yes')
                    else:
                        print('No')
                        db.execute(f'INSERT INTO news(title, url, link, data_time) VALUES ("{article_title}",'
                                   f' "{split_list[0]}",'
                                   f'"{split_list[1]}",'
                                   f'"{article_data_time}")')
            except Exception as err:
                print(f' FAILED :{err}')

def check_news():
    chek_ecb()
    check_forcklog()
    check_reuters()
    list_news = []
    with DataBase('news.db') as db:
        test = db.execute('select * from news order by rowid desc limit 1').fetchone()
        for news in test:
            if news in list_news:
                continue
            else:
                list_news.append(news)
            return list_news



def main():
    print(check_news())


if __name__ == '__main__':
    main()
