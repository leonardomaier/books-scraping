from bs4 import BeautifulSoup

import requests
import json

base_url = 'http://books.toscrape.com/'

get_ratings = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5
}

books = []


def request_and_parse(endpoint=''):

    response = requests.get(base_url + endpoint)

    return BeautifulSoup(response.text, 'html.parser')


soup = request_and_parse()

categories_div = soup.select('div.side_categories > ul > li > ul > li > a')

for category in categories_div:

    soup = request_and_parse(category['href'])

    products = soup.find_all('article', class_='product_pod')

    print('******* ' + category.text.strip() + ' *******')

    for product in products:

        name = product.find('h3').find('a').get('title')
        price = product.find('p', class_='price_color').text.replace('Â£', '')
        in_stock = product.find('p', class_='instock').find('i')['class'][0]
        rating = product.find('p', class_='star-rating')['class'][1].lower()

        print('   >>> ' + name)

        books.append({
            'name': name,
            'price': price,
            'in_stock': (in_stock == 'icon-ok'),
            'rating': get_ratings[rating] * '*',
            'category': category.text.lower().strip()
        })


with open('books.json', 'w', encoding='utf-8') as file:

    json.dump(books, file, indent=4)
