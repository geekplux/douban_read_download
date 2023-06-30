import pandas as pd
import requests
import re

books = pd.read_csv('./books.csv')
books = books.rename(columns={
    'title': 'Title',
    'rating': 'My Rating',
    'pub': 'Publisher',
    'read_date': 'Date Read',
    'comment': 'My Review',
})

books_urls = books['url'].tolist()

headers = {
   'User-Agent': 'M',
}

for i, url in enumerate(books_urls):
    print(f'[{i}/{len(books_urls)}]', "Scraping: ", url)
    r = requests.get(url, headers=headers)
    matched = re.search(r'<meta property="book:isbn" content="(\d+)" />', r.text)
    isbn = matched.group(1).strip() if matched else ''
    print("ISBN: ", isbn)
    books.loc[books['url'] == url, 'ISBN'] = isbn

books.to_csv('./goodreads_books.csv')
