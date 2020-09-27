import scrapy
import pandas as pd
from environs import Env


env = Env()
env.read_env()
cookies = env("COOKIES")


def _s(s):
    return ''.join(s) if s else ''


class DoubanSpider(scrapy.Spider):
    name = 'douban_spider'
    start_url = 'https://book.douban.com/mine?status=collect'
    headers = {
        'cookie': cookies,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }

    df = pd.DataFrame(columns=['title', 'url', 'pub',
                               'rating', 'read_date', 'tags', 'comment'])

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        print('Read book list: ', response.url)
        book_list = response.css('#content div.article ul li.subject-item')
        for item in book_list:
            title = item.css('div.info > h2 > a::text').get().strip()
            print('Is scraping: ', title)
            try:
                rating = _s(item.css(
                    'div.info div.short-note > div:nth-child(1) > span:nth-child(1)::attr(class)').get()).strip()
                rating = int(_s(filter(str.isdigit, rating))
                             ) if rating.startswith('rating') else ''
                book = {
                    'title': title,
                    'url': _s(item.css('div.info > h2 > a::attr(href)').get()),
                    'pub': _s(item.css('div.info > div.pub::text').get()).strip(),
                    'rating': rating,
                    'read_date': _s(item.css('div.info div.short-note > div:nth-child(1) > span.date::text').get()).replace('读过', '').strip(),
                    'tags': _s(item.css('div.info div.short-note > div:nth-child(1) > span.tags::text').get()).replace('标签:', '').strip(),
                    'comment': _s(item.css('div.info div.short-note > p.comment::text').get()).strip(),
                }
                self.df = self.df.append(book, ignore_index=True)
            except Exception as error:
                print('error on: ', title, error)

        next_page = response.css(
            '#content div.article div.paginator > span.next > a::attr(href)').get()
        if next_page:
            url = response.urljoin(next_page)
            print("next page: ", url)
            yield scrapy.Request(url, callback=self.parse_list, headers=self.headers)
        else:
            self.df.to_csv('./books.csv')
