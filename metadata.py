import requests
import json
import time
import csv
from tqdm import tqdm


url = "http://api.syosetu.com/novelapi/api/"

# APIのパラメータをディクショナリで指定する
# この条件で、総合評価順でjson形式のデータを出力する
payload = {'of': 'n', 'order': 'impressioncnt','out':'json'}


def api():
    data = []
    with open('201ncode_list', 'r') as ls:
        ncode = ls.readlines()
    for n in tqdm(ncode):
        payload = {'out': 'json','ncode':n}
        r = requests.get(url,params=payload)
        time.sleep(1)
        x = r.json()
        data.extend(x[1:])
       
    return data

data = api()

print(data)

    
names = data[0].keys()
print(names)

with open('201_metadata.csv', 'w') as f:
    wr = csv.DictWriter(f, fieldnames = names)
    wr.writeheader()
    wr.writerows(data)
    print(wr)
    
with open('201_metadata.json', 'w') as j:
    wj = json.dump(data, j)
    wj

