import json
import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time as bot_delay


now = datetime.now()
time = now.strftime("%d/%m/%Y %H:%M").replace('/', '.').replace(':', '.')
site = "https://proftorg.kz/"


def prod_parser(main_url):
    bot_delay.sleep(1.5)
    # GETTING ONE PRODUCT PAGE
    main_r = requests.get(main_url)

    main_soup = BeautifulSoup(main_r.content, 'html.parser')
    all_lis = main_soup.find('ul', class_='cs-product-gallery').find_all('li')

    title = main_soup.find(
        'h1', class_='cs-title').find('span').text.replace(',', ' ').replace('.', ' ').replace('"', '').replace('/', '.')
    title = title.strip()


    tmp = 1
    for li in all_lis:
        # GETTING EXACT PRODUCT PAGE
        url = f"{site}{li.find('a', class_='cs-product-gallery__image-link')['href']}"
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
            pass

        # PRODUCT PHOTO

      
        photo_url = soup.find(
            'img', class_="cs-product-image__img csjs-image")['src']
 


        product_object = {
            "title": prod_name,
            "imgLink": photo_url,
            "desc": stats,
            "price": prof_price,
            "source_site": "proftorg",
            "catergory": "elecmeh",
            "subCategory": title
        }

        all_products.append(product_object)

  
      
        print(f'{len(all_lis) - tmp } ЗАПИСЬ: {prod_name} {prod_code} ')
        tmp += 1

        
    
   


all_products = []
prod_parser('https://proftorg.kz/g1283073-blendery-dlya-koktejlej')
print('DONE!')

os.mkdir(os.path.join(f'allprod {time}'))
os.chdir(os.path.join(f'allprod {time}'))


with open("mydata.json", "w", encoding='utf-8') as final:
    json.dump(all_products, final, ensure_ascii=False)

