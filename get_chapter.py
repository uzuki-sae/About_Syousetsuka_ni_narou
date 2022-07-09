from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import os
import time
import datetime
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import url_lister

genre_list = [102, 202, 302, 303, 304, 305, 306, 307, 401, 402, 403, 404]

def main():
    """
    メイン処理
    """
    # --------------------------------------
    # 作品ページのURLを指定（コメントアウト・コメントインで指定できるようにしています）
    for genre in genre_list:
        print('Now entering genre:{}'.format(genre))
        os.makedirs(str(genre), exist_ok=True)
        ncode = []
#        url_lister.get_url(genre)

        with open('{}ncode_list'.format(genre), 'r') as nl:
            for lines in nl:
                line = lines[:-1]
                ncode.append(line)

        with ThreadPoolExecutor(max_workers=4) as executor:
            result = {executor.submit(ncode_task, genre, nc): nc for nc in ncode}
            print(result)
        getLogger().info("submit end")

def ncode_task(genre, nc):
    try:
        if not os.path.isfile('{}/{}-1.txt'.format(genre, nc)):

            url = 'https://ncode.syosetu.com/{}/'.format(nc)
            stories = ""
            bs_obj = make_bs_obj(url)
            url_list = ["https://ncode.syosetu.com" + a_bs_obj.find("a").attrs["href"] for a_bs_obj in bs_obj.findAll("dl", {"class": "novel_sublist2"})]
    # 各話の本文情報を取得
            for j in range(len(url_list)):
                    url = url_list[j]
                    bs_obj = make_bs_obj(url)
                    time.sleep(1)
                    stories = get_main_text(bs_obj)
                    f = open('{0}/{1}-{2}.txt'.format(genre, nc, j+1), 'w')
                    f.write(stories)
                    f.close()
                    print('{0}/{1}-{2}.txt is writen.'.format(genre, nc, j+1))
        else:
            print('{} is existed'.format(nc))
    except Exception as e:
        print(e)
        pass


    


def make_bs_obj(url):
    """
    BeautifulSoupObjectを作成
    """
    html = urlopen(url)
    logger.debug('access {} ...'.format(url))

    return BeautifulSoup(html,"html.parser")

def get_main_text(bs_obj):
    """
    各話のコンテンツをスクレイピング
    """
    text = ""
    text_htmls = bs_obj.findAll("div",{"id":"novel_honbun"})[0].findAll("p")

    for text_html in text_htmls:
        text = text + text_html.get_text() + "\n\n"

    return text


main()
