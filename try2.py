import requests
import json
import pandas as pd

specs = requests.get('https://api.hh.ru/specializations')
specs = specs.json()
lst = []
for i in range(28):
    specs[i] = specs[i]['specializations']
    lst += specs[i]
df = pd.DataFrame(lst)
df = df.drop(['laboring'], axis=1)
times = df.shape[0]
mean = '{'
for i in range(times):
    mean += f'''"{df.loc[i]['id']}":"{df.loc[i]['name']}", '''
mean = mean.rstrip(', ')
mean += '}'
print(mean)
d = json.loads(mean)
print(d['1.395'])