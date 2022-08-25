import json
import os
import shutil
from datetime import datetime

targer_folder = 'PROFTORG 15.08.2022 16.25'

now = datetime.now()
time = now.strftime("%H:%M:%S").replace('/', '.').replace(':', '.')
folder_items = list(os.listdir(f'./{targer_folder}'))

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

with open("myfilter.json", "w", encoding='utf-8') as final:
    json.dump(category, final, ensure_ascii=False)

os.chdir('..')
filter_folder = os.path.join(os.getcwd(), f'filter {time}', "myfilter.json")
files_in_folder = os.path.join(os.getcwd(), f'{targer_folder}')
new_filtered_folder = os.path.join(os.getcwd(), f'{targer_folder}', f'filtered{time}')

os.mkdir(new_filtered_folder)
os.mkdir(os.path.join(new_filtered_folder, 'teplo'))
os.mkdir(os.path.join(new_filtered_folder, 'holod'))
os.mkdir(os.path.join(new_filtered_folder, 'neitral'))
os.mkdir(os.path.join(new_filtered_folder, 'elecmeh'))


with open(filter_folder, 'r', encoding='utf-8') as json_file:
        category = json.load(json_file)

for item in os.listdir(files_in_folder):
        if item[:-5] in category['teplo']:
                shutil.copyfile(os.path.join(files_in_folder, item), os.path.join(new_filtered_folder, 'teplo', item))
        elif item[:-5] in category['holod']:
                shutil.copyfile(os.path.join(files_in_folder, item), os.path.join(new_filtered_folder, 'holod', item))
        elif item[:-5] in category['neitral']:
                shutil.copyfile(os.path.join(files_in_folder, item), os.path.join(new_filtered_folder, 'neitral', item))
        elif item[:-5]in category['elecmeh']:
                shutil.copyfile(os.path.join(files_in_folder, item), os.path.join(new_filtered_folder, 'elecmeh', item))