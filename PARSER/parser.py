import json
import re
import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
import time as bot_delay
from transliterate import translit


now = datetime.now()
time = now.strftime("%d/%m/%Y %H:%M").replace('/', '.').replace(':', '.')

# site = 'https://proftorg.kz/'
# source_site = 'PROFTORG'
# all_prods_url = 'cs-product-groups-gallery__title'
# prod_page_url = 'cs-product-gallery'
# one_prod_url = 'cs-product-gallery__image-link'
# prod_image_url = 'cs-product-image__img csjs-image'

site = 'https://dedtrade.kz/'
source_site = 'DEDTRADE'
all_prods_url = 'cs-product-groups-gallery__title'
prod_page_url = 'cs-product-gallery'
one_prod_url = 'cs-image-holder__image-link'
prod_image_url = 'cs-image-holder__image csjs-image'


def prod_parser(main_url):
    bot_delay.sleep(1.5)
    # GETTING ONE PRODUCT PAGE
    main_r = requests.get(main_url)

    main_soup = BeautifulSoup(main_r.content, 'html.parser')
    all_lis = main_soup.find('ul', class_=f'{prod_page_url}').find_all('li')

    title = main_soup.find(
        'h1', class_='cs-title').find('span').text.replace(',', ' ').replace('.', ' ').replace('"', '').replace('/', '.')
    title = title.split()


    sub_categoty = ''
    for word in title:
        sub_categoty += ' ' + word
        sub_categoty = sub_categoty.strip()

    tmp = 0
    for li in all_lis:
        bot_delay.sleep(0.7)
        # GETTING EXACT PRODUCT PAGE
        url = f"{site}{li.find('a', class_=f'{one_prod_url}')['href']}"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        # PRODUCT NAME
        prod_name = soup.find('span', attrs={'data-qaid': 'product_name'}).text

        # PRODUCT CODE
        prod_code = soup.find('span', attrs={'data-qaid': 'product_code'})
        if prod_code is None:
            prod_code = soup.find(
                'span', attrs={'data-qaid': 'product_name'}).text
        else:
            prod_code = soup.find(
                'span', attrs={'data-qaid': 'product_code'}).text

        # PRODUCT DESCRIPTION
        stats = ''

        try:
            prod_stat = soup.find(
            'table', class_="b-product-info").text
            stats = prod_stat
        except:
            prod_desk = soup.find(
                'div', attrs={'data-qaid': 'product_description'})
            if prod_desk is None:
                try:
                    stats = soup.find(
                        'div', attrs={'data-qaid': 'product_description'}).text
                except:
                    stats = 'PUSTO'
            elif prod_desk.find('ul') is None:
                try:
                    stats = soup.find(
                        'div', attrs={'data-qaid': 'product_description'}).text
                except:
                    stats = 'PUSTO'
            else:
                for li in prod_desk.find('ul').find_all('li'):
                    stats = stats + ' ' + li.text
                    
        stats =  stats.replace('\n', ' ')
        # PRICE

        try:
            price_tmp = ''

            prod_price_str = soup.find(
            'span', attrs={'data-qaid': 'product_price'}).text
            prod_price_list = re.findall(r'\d+', prod_price_str)
            for num in prod_price_list:
                price_tmp +=  str(num)

            prod_price = int(price_tmp)
            prof_price = prod_price
        except:
            prof_price = 0


        # PRODUCT PHOTO

        try:
            photo_url = soup.find(
                'img', class_=f"{prod_image_url}")['src']
        except:
            photo_url = 'https://via.placeholder.com/300.png'

        category = ''
        if sub_categoty in filter_dict['filter_category']['teplo']:
            category = 'teplo'
        elif sub_categoty in filter_dict['filter_category']['holod']:
            category = 'holod'
        elif sub_categoty in filter_dict['filter_category']['neitral']:
            category = 'neitral'
        elif sub_categoty in filter_dict['filter_category']['elecmeh']:
            category = 'elecmeh'


        prod_date = now.strftime("%d/%m/%Y %H:%M").replace('/', '.').replace(':', '.')
        prod_id = f"{translit(prod_code.replace('/', '').replace(':', '').replace('.', '').replace(' ', '').replace('-', ''), language_code='ru', reversed=True)}_{prod_date.replace('.', '').replace(' ', '')}"
        product_object = {
            "id": prod_id,
            "date": prod_date,
            "title": prod_name,
            "prodCode": prod_code,
            "imgLink": photo_url,
            "prodLink": url,
            "desc": stats,
            "price": prof_price,
            "sourceSite": source_site,
            "catergory": category,
            "subCategory": sub_categoty
        }

        all_products.append(product_object)

  
      
        print(f'{len(all_lis) - tmp} ЗАПИСЬ: {prod_name} {prod_code} ')
        tmp += 1
   
    # os.chdir("..")


prof_r = requests.get(f"{site}/")
prof_soup = BeautifulSoup(prof_r.content, 'html.parser')
prof_lis = prof_soup.find(
    'ul', class_='cs-product-groups-gallery').find_all('li')


tic = bot_delay.perf_counter()
incre = 1

all_products = []

with open("./filter.json", "r", encoding='utf-8') as filter:
    tmp = json.loads(filter.read())

filter_dict = tmp

for li in prof_lis:
    bot_delay.sleep(2)
    prod_url = f"{li.find('a', class_=f'{all_prods_url}')['href']}"
    print(f'{incre}/{len(prof_lis)}')
    incre += 1
    prod_parser(f"{site}{prod_url}?product_items_per_page=48")

toc = bot_delay.perf_counter()

secs = toc - tic

os.mkdir(os.path.join(f'{source_site} allprod {time}'))
os.chdir(os.path.join(f'{source_site} allprod {time}'))


with open(f"{source_site}.json", "w", encoding='utf-8') as final:
    json.dump(all_products, final, ensure_ascii=False)

print(f"DONE! Time: {secs/60} mins  {secs} secs")