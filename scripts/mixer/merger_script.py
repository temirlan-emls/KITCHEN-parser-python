import os
import shutil


my_list = os.listdir('.')
current_folder = os.getcwd()

# os.chdir(os.path.join(os.getcwd()))


df = []
for i in my_list:
    if (i == os.path.basename(__file__)):
        pass
    else:
        os.chdir(os.path.join(os.getcwd()))
        for file in os.listdir(os.path.join(os.getcwd(), i)):
            if file.endswith('.xlsx'):
                src = f'{os.path.join(os.getcwd(), i, str(file))}'
                dest = f'{os.getcwd()}'
                path = shutil.copy(src,dest)
                print(path)

