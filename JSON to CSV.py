import pandas as pd
import glob
import os

os.chdir('JSON datasets')
os.mkdir('CSV datasets')
json_globe = glob.glob('*.json')
for item in json_globe:
    df = pd.read_json(item)
    item = item.replace('.json' , '')
    df.to_csv('CSV datasets/{}.csv'.format(item) , index = False , encoding = 'utf-8')
    print(item + ' Done!')
