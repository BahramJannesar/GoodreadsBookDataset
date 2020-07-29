import pandas as pd
import glob
import os


df = pd.read_json('book1800k-1900k.json')
df.to_csv('book1800k-1900k.csv' , index = False , encoding = 'utf-8')

