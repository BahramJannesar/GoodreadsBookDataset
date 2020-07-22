import pandas as pd
import glob
import os


df = pd.read_json('book1700k-1800k.json')
df.to_csv('book1700k-1800k.csv' , index = False , encoding = 'utf-8')

