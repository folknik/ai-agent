import requests
from typing import List
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from settings.config import HABR_URL


def get_content_from_url(url: str) -> str:
    ua = UserAgent()
    headers = {
        'accept': 'application/json, text/plain, */*',
        'User-Agent': ua.google
    }
    req = Request(url=url, headers=headers)
    with urlopen(req) as response:
        html = BeautifulSoup(response.read(), 'html.parser')
        html_content = html.get_text()
    return html_content


def get_articles_from_last_day() -> List[dict]:
    ua = UserAgent()
    headers = {
        'accept': 'application/json, text/plain, */*',
        'user-Agent': ua.google,
    }
    response = requests.get(
        url=HABR_URL,
        headers=headers
    )
    articles = []
    soup = BeautifulSoup(response.text, 'lxml')
    all_hrefs_articles = soup.find_all(
        name='a',
        class_='tm-title__link'
    )
    all_datetime_published = soup.find_all(
        name='a',
        class_='tm-article-datetime-published tm-article-datetime-published_link'
    )
    for article, published_ts in zip(all_hrefs_articles, all_datetime_published):
        name = article.find('span').text
        link = f'https://habr.com{article.get("href")}'
        dt = published_ts.find('time')['datetime']
        articles.append(
            {
                'name': name,
                'link': link,
                'dt': datetime.fromisoformat(dt).replace(tzinfo=None)
            }
        )
    start = datetime.combine(
        date=datetime.now().date() - timedelta(days=1),
        time=datetime.min.time()
    )
    end = datetime.now()
    return [art for art in articles if start <= art['dt'] < end][::-1]
