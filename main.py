import requests
from bs4 import BeautifulSoup
import lxml
from time import sleep
from os import path
from random import randint
import json
import csv

HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
          'Accept': '*/*'}
URL = 'https://openkart.ru/sitemap'
time_sleep = randint(2, 4)


def get_html(URL, HEADER=HEADER, time_sleep=time_sleep):
    print(URL)
    req = requests.get(URL, HEADER)
    if req.status_code == 200:
        sleep(time_sleep)
        return req.text


def pars_map(src):
    soup = BeautifulSoup(src, 'lxml')
    data = soup.body.find('div', id='information-sitemap').find('div', id='content').find('div', class_='row').find_all(
        'div', class_='col-sm-6')
    temp = data[0].ul.find_all('a')
    url_map = {}
    for t in temp:
        url_map[t.get('href')] = ''
    return url_map


def get_cards_urls(src):
  soup = BeautifulSoup(src, 'lxml')

  line_3 = soup.find('div', class_='row').find_all('div', class_='product-thumb transition')
  print(line_3)
  url_line_3 = []
  for l in line_3:
    url_line_3.append(l)
  return url_line_3


def for_json_first(url, name = 'data.json', data = '0'):
    data_row = {url: data}
    if path.exists(name):
        with open(name) as file:
            data_row = json.loads(file.read())
            data_row[url] = data
            with open(name, 'w') as file:
                json.dump(data_row, file, indent=4, ensure_ascii=False)
    else:
        with open(name, 'w') as file:
            json.dump(data_row, file, indent=4, ensure_ascii=False)

def pars_card(scr, url):

    soup = BeautifulSoup(scr, 'lxml')

    name = soup.find('h1', class_='product-product-h1').text
    if len(name) == 0:
        name = 'NOT_FIND!'

    data = soup.find_all('ul', class_='list-unstyled')

    maider = data[0].find_all('li')[0].text.split(':')[1].replace(' ', '')
    if len(maider) == 0:
        maider = 'NOT_FIND!'

    articul = data[0].find_all('li')[1].text.split(':')[1].replace(' ', '')
    if len(articul) == 0:
        articul = 'NOT_FIND!'

    info_procuct = soup.find('div', class_='product-description').text
    if len(info_procuct) == 0:
        info_procuct = 'NOT_FIND!'

    product_price = soup.find('div', class_='product-price').text.replace(' ', '').replace('\n', '')[:-2]
    if len(product_price) == 0:
        product_price = 'NOT_FIND!'

    pic = str(soup.find('ul', class_='thumbnails').contents[1]).split('=')[2].split(' ')[0].replace('"', '')

    return {url: {'art': articul,
                      'mider': maider, 'name': name,
                      'price': product_price, 'content': info_procuct,
                      'pic_url': pic, 'url': url}}

def main():
  '''
    text = get_html(URL, HEADER, time_sleep)
    url_map = pars_map(text)
    temp_row = {}
    for i,j in url_map.items():
        soup = BeautifulSoup(get_html(i, HEADER, time_sleep), 'lxml')

        temp = soup.find('div', class_='col-md-6 text-right category-results').text.split()

        data = []

        for t in temp:
            if t.isdigit():
                data.append(t)
        pages = data[-1]
        #temp_row[i] = pages
        #print(temp_row)
        for_json_first(i, 'data_first.json', pages)
  '''
  with open('data_first.json') as file:
    src = json.load(file)

  for i, j in src.items():
    pass

  URL_TEST = 'https://openkart.ru/tm-kz-inlet-gasket'
  text = get_html(URL_TEST, HEADER, time_sleep)
  data =  get_cards_urls(text)
  print(data)

#main()



"""
with open('data_first.json') as file:
    data_row = json.loads(file.read())
data_row_add = {}
for i,j in data_row.items():
    if int(j) > 1:
        k = 2
        while k<=int(j):
            url = i + f'?page={k}'
            k += 1
            data_row_add[url] = 1
    else:
        data_row_add[i] = 1
with open('data_second.json', 'w') as file:
    json.dump(data_row_add, file, indent=4, ensure_ascii=False)
"""

"""
with open('data_second.json') as file:
    data = json.load(file)
k = 0
for i, j in data.items():
    src = get_html(i, HEADER, time_sleep)
    with open(f'data_html/{k}.html', 'w') as file:
        file.write(src)
    k += 1
"""
"""
data = {}
i = 61
while i >= 0:
    with open(f'data_html/{i}.html') as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    line_3 = soup.find_all('div', class_='product-thumb transition')
    for l in line_3:
        data[l.h4.find('a').get('href')] = {}
    i -= 1
with open('data_3.json', 'w') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
"""

"""
def pars_card(scr, url):

    soup = BeautifulSoup(scr, 'lxml')

    name = soup.find('h1', class_='product-product-h1').text
    if len(name) == 0:
        name = 'NOT_FIND!'

    data = soup.find_all('ul', class_='list-unstyled')

    maider = data[0].find_all('li')[0].text.split(':')[1].replace(' ', '')
    if len(maider) == 0:
        maider = 'NOT_FIND!'

    articul = data[0].find_all('li')[1].text.split(':')[1].replace(' ', '')
    if len(articul) == 0:
        articul = 'NOT_FIND!'

    info_procuct = soup.find('div', class_='product-description').text
    if len(info_procuct) == 0:
        info_procuct = 'NOT_FIND!'

    product_price = soup.find('div', class_='product-price').text.replace(' ', '').replace('\n', '')[:-2]
    if len(product_price) == 0:
        product_price = 'NOT_FIND!'

    pic = str(soup.find('ul', class_='thumbnails').contents[1]).split('=')[2].split(' ')[0].replace('"', '')

    return {url: {'art': articul,
                      'mider': maider, 'name': name,
                      'price': product_price, 'content': info_procuct,
                      'pic_url': pic, 'url': url}}
"""


#text = get_html('https://openkart.ru/tm-kz-inlet-gasket')
with open('index.html') as file:
  src = file.read()

soup = BeautifulSoup(src, 'lxml')

line_3 = soup.find('div', class_='product-thumb transition')
data = str(line_3).split("\"")

print('*'*70)
temp = []
for d in data:
  temp.append(d.split('\''))
f = []
for t in temp:
  for i in t:
    if i.find('https://openkart.ru/') == 0:
      f.append(i)
    break
print(f[0]) 