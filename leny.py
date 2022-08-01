import pandas as pd


df = pd.read_csv('all.csv', encoding='utf-8', header=0)
print(df.shape[0])
del df
frame = pd.read_csv('parsedData.csv', encoding='utf-8', header=0)
print(frame.shape[0])