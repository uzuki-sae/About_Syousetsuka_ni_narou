import requests
import json
import time

url = "http://api.syosetu.com/novelapi/api/"

# APIのパラメータをディクショナリで指定する
# この条件で、総合評価順でjson形式のデータを出力する
payload = {'of': 'n', 'order': 'impressioncnt','out':'json'}

genre_list = [101, 102, 202, 302, 303, 304, 305, 306, 307, 401, 402, 403, 404]

def api(genre):
    data = []
    for st in [1, 501, 1001, 1501]:
        payload = {'of': 'n', 'order': 'impressioncnt', 'out': 'json', 'lim': 500, 'st': st, 'genre': genre}
        r = requests.get(url,params=payload)
        time.sleep(1)
        x = r.json()
        data.extend(x[1:])
       
    return data

def get_url(genre):
    ncode = []
    data = []
    data = api(genre)
    for v in data:
        nc = v['ncode']
        ncode.append(nc)
            
    listname = str(genre) + 'ncode_list'
    f = open(str(listname), 'w')
    for line in ncode:
        f.write(str(line) + "\n")
    f.close()


    

if __name__ == "__main__":
    get_url()


