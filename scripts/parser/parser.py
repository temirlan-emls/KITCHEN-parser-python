from fileinput import filename
import requests
import re
from bs4 import BeautifulSoup
import openpyxl



book = openpyxl.open("OLX.xlsx", read_only=True)
book2 = openpyxl.open("OLX2.xlsx", read_only=False)
sheet = book.active
sheet2 = book2.active


for row in range(2, 24):
    for column in range(1, 21):
        rowN = sheet[row][0].value
        columnN = sheet[1][column].value
        print(rowN, columnN)
        url = f'https://www.olx.kz/d/uslugi/dlya-biznesa/oborudovanie/{rowN}/q-{columnN}'
        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'lxml')
        res = soup.find(
            'h3', class_='css-pqvw3x-Text eu5v0x0').find('div').text

        pattern = "[0-9]+"
        sheet2[row][column].value = re.findall(pattern, res)[0]
        print(re.findall(pattern, res)[0])
book2.save(filename="OLX2.xlsx")
