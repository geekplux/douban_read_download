import scrapy

class DoubanSpider(scrapy.Spider):
  name = 'douban_spider'
  start_url = 'https://book.douban.com/mine?status=collect'
  headers = {
    'cookie': 'TODO',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
  }

  def start_requests(self):
    yield scrapy.Request(url=self.start_url, callback=self.parse_list, headers=self.headers)

  def parse_list(self, response):
    print('Read book list: ', response.url)
    detail_url = response.css('#content div.article ul > li:nth-child(1) > div.info > h2 > a::attr(href)').get()
    yield scrapy.Request(url=detail_url, callback=self.parse_detail, headers=self.headers)

  def parse_detail(self, response):
    print('book detail page url: ', response.url)
    book = {
      'title': response.css('#wrapper > h1 > span::text').get()
    }

    print(book)
