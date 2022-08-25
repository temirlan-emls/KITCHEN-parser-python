import json
import os
from datetime import datetime


now = datetime.now()
time = now.strftime("%H:%M:%S").replace('/', '.').replace(':', '.')
folder_items = list(os.listdir('./PROFTORG 15.08.2022 16.25'))

category = {
    "teplo": [],
    "holod": [],
    "neitral": [],
    "elecmeh": []
}


for item in folder_items:
    item = item.strip()
    item_name = item[:-5]
    print(item_name)
    print('1)TEPLO 2)HOLOD 3)NEITRALKA 4)ELECMEH')
    ipt = int(input())
    if ipt == 1:        
        category['teplo'].append(str(item_name))
    elif ipt == 2:        
        category['holod'].append(str(item_name))
    elif ipt == 3:
        category['neitral'].append(str(item_name))
    elif ipt == 4:
        category['elecmeh'].append(str(item_name))
    
os.mkdir(os.path.join(f'filter {time}'))
os.chdir(os.path.join(f'filter {time}'))

with open("mydata.json", "w", encoding='utf-8') as final:
    json.dump(category, final, ensure_ascii=False)
