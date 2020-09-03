import pandas as pd

df = pd.read_json('book1900k-2000k.json')
df.to_csv('book1900k-2000k.csv' , index = False , encoding = 'utf-8')

