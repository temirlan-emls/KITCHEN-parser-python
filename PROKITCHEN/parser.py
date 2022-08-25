from ast import Try
import json
import os
from selenium import webdriver
from selenium_stealth import stealth
import time
from selenium.webdriver.common.by import By
from datetime import datetime
from transliterate import translit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time as bot_delay

now = datetime.now()
time_name = now.strftime("%d/%m/%Y %H:%M").replace('/', '.').replace(':', '.')


def pro_parser():
    func_tmp = 0
    for link in pro_links:
        print(f'{len(pro_links) - func_tmp}')
        func_tmp += 1
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")

        # options.add_argument("--headless")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options, executable_path=r"./helpers/chromedriver.exe")

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        url = f"{link}"
        driver.get(url)

        driver.minimize_window()

        bot_delay.sleep(15)
        product_container = driver.find_element(By.CLASS_NAME, "product-subcategory__content")
        products = product_container.find_elements(By.CLASS_NAME, "pitem")
        tmp = 0
        for item in products:
            bot_delay.sleep(3)
            # IMG
            try:
                tmp_img = item.find_element(By.CLASS_NAME, "pitem__image")
                img = tmp_img.get_attribute('src')
            except:
                img = 'https://via.placeholder.com/300.png'
            # TITLE
            try:
                prod_title = item.find_element(By.CLASS_NAME, "pitem__title").get_attribute('innerText')
            except:
                prod_title = 'aaa'
            # PRODUCT CODE
            try:
                prod_code = item.find_element(By.CLASS_NAME, "pitem__articul").get_attribute('innerText')
            except:
                prod_code = 'aaa'
            # STATS
            try:
                prod_stats = item.find_element(By.CLASS_NAME, "pitem__info").get_attribute('innerText')
            except:
                prod_stats = 'aaa'
            # PRICE
            try:
                prod_price = item.find_element(By.CLASS_NAME, "basket-form__maincost").text
            except:
                prod_price = 0
            # CATEGORY AND SYBCATEGORY
            path_list = []
            try:
                app_path_container = driver.find_element(By.CLASS_NAME, "app-path")
                app_path = app_path_container.find_elements(By.CLASS_NAME, "app-path__text")
            except:
                app_path = ['asfasf', 'asfasdfas']

            try:
                for i in app_path:
                    path_list.append(i.get_attribute('innerText'))
                if (path_list[-2] == 'Электромеханическое оборудование'):
                    category = 'elecmeh'
                elif (path_list[-2] == 'Тепловое оборудование'):
                    category = 'teplo'
                elif (path_list[-2] == 'Холодильное оборудование'):
                    category = 'holod'
                elif (path_list[-2] == 'Нейтральное оборудование'):
                    category = 'neitral'
                else:
                    category = 'teplo'
                sub_category = path_list[-1]
            except:
                category = 'unknow'
                sub_category = 'unknow'

            prod_date = now.strftime("%d/%m/%Y %H:%M").replace('/', '.').replace(':', '.')
            prod_id = f"{translit(prod_code.replace('/', '').replace(':', '').replace('.', '').replace(' ', '').replace('-', ''), language_code='ru', reversed=True)}_{prod_date.replace('.', '').replace(' ', '')}"
            product_object = {
                "id": prod_id,
                "date": prod_date,
                "title": prod_title,
                "prodCode": prod_code,
                "imgLink": img,
                "prodLink": url,
                "desc": prod_stats,
                "price": prod_price[:-3],
                "sourceSite": "PROKITCHEN",
                "catergory": category,
                "subCategory": sub_category
            }

            all_products.append(product_object)
            print(f'{len(products) - tmp} ЗАПИСЬ: {prod_title} {prod_code} ')
            tmp += 1
        driver.quit()


all_products = []

with open("./prokitchen_links.json", "r", encoding='utf-8') as links:
    pro_links = json.loads(links.read())

tic = bot_delay.perf_counter()

pro_parser()

toc = bot_delay.perf_counter()

secs = toc - tic
os.mkdir(os.path.join(f'PROKITCHEN allprod {time_name}'))
os.chdir(os.path.join(f'PROKITCHEN allprod {time_name}'))


with open(f"PROKITCHEN.json", "w", encoding='utf-8') as final:
    json.dump(all_products, final, ensure_ascii=False)

print(f"DONE! Time: {secs/60} mins  {secs} secs")