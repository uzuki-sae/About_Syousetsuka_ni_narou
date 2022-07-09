
import csv
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

interval=1

file_name="syuppan.csv"

#ページ数の指定(調べて打ち込む、大きく取っておいてあとで重複分を消した方が楽かも)
all_page_num=277

#requestsの設定ユーザーエージェントの設定（設定必須）
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15"}
cookie = {'over18': 'yes'}  # Xサイト用のクッキー

#書き出し用
all_list=[]
columns_name=["書籍名","著者","イラストレーター","出版社","レーベル","出版形態",
              "発売日","発売年","ISBN","「電子」の記載","「コミック」の記載","ユーザID","ユーザ名","作者マイページ",
              "書報ページURL","アマゾンURL"]

#スクレイピング
def get_data():
    for page in tqdm(range(201, all_page_num )):
        page=page+1
        url="https://syosetu.com/syuppan/list/?p=%s"%page
        print(url)

        response = requests.get(url=url, headers=headers, cookies=cookie)
        html = response.content
        soup = BeautifulSoup(html, "lxml")
                
        title_list=[]
        title_url_list=[]
        
        sp1=soup.find_all("a",class_="p-syuppan-list__title")
        
        for i in range(len(sp1)):            
            title_list.append(sp1[i].text)#タイトル
            title_url_list.append("https://syosetu.com"+sp1[i].get("href"))#個別ページURL
            
        #個別ページの取得
        for i in range(len(title_url_list)):
                        
            response = requests.get(url=title_url_list[i], headers=headers, cookies=cookie)
            html = response.content
            soup = BeautifulSoup(html, "lxml")
            
            temp_list=[]
            
            book_author=""
            illustration=""
            publisher=""
            label=""
            pub_type=""
            publish_date=""
            publish_year=""
            isbn=""
            userid=""
            user_name=""
            user_mypage=""
            amazon_url=""
            is_densi=0
            is_comincs=0
                
            #著者名
            try:
                sp = soup.find("div",class_="p-syuppan-detail__info-author").text

                if "(著)"in sp:               
                    index1=sp.find("(著)")
                    book_author=sp[1:index1]
                else:
                    book_author=sp

                #イラストレータ名
                if "(イラスト"in sp:               
                    index2=sp.find("(イラスト")
                    index3=sp[0:index2].rfind(",")
                    illustration=sp[index3+2:index2]
            except:
                pass
            
            #出版社名など
            table_text=soup.find("table",class_="c-table").text

            if "出版社" in table_text:
                publisher=soup.find("th",string="出版社").find_next("td").text[1:-1]
                
            if "レーベル" in table_text:   
                label=soup.find("th",string="レーベル").find_next("td").text
                
            #出版形態
            type_exist=len(soup.find_all("span",class_="p-syuppan-detail__info-binding"))
            
            if 0 != type_exist:
                pub_type=soup.find_all("span",class_="p-syuppan-detail__info-binding")[0].text
                    
            if "発売日" in table_text:
                publish_date=soup.find("th",string="発売日").find_next("td").text
                publish_year=int(publish_date[0:4])
                   
            if "ISBN" in table_text:
                isbn=soup.find("th",string="ISBN").find_next("td").text
                isbn=int(isbn)

            #ユーザ情報
            user=soup.find_all("div",class_="c-panel__body-headline")
            
            if user[-1].text in "小説家になろう登録情報":
                userid=soup.find("th",string="ユーザID").find_next("td").text
                userid=int(userid)
                user_name=soup.find("th",string="ユーザ名").find_next("td").text
                user_mypage="https://mypage.syosetu.com/%s/"%userid
            
            #アマゾンURL
            ama_exist=len(soup.find_all("div",class_="p-syuppan-detail__purchase"))
            
            if 0 != ama_exist:
                try:
                    amazon_url=soup.find("a",class_="c-button c-button--half c-button--lg c-button--primary").get("href")
                except:
                    pass
                    

            #電子の記載
            if "電子" in soup.find("div",class_="c-panel").text:
                is_densi=1
                
            #コミックの記載
            if "コミック" in soup.find("div",class_="c-panel").text:
                is_comincs=1
                    
            #書き出し
            temp_list.append(title_list[i])
            temp_list.append(book_author)
            temp_list.append(illustration)
            temp_list.append(publisher)
            temp_list.append(label)
            temp_list.append(pub_type)
            temp_list.append(publish_date)
            temp_list.append(publish_year)
            temp_list.append(isbn)
            temp_list.append(is_densi)
            temp_list.append(is_comincs)
            temp_list.append(userid)
            temp_list.append(user_name)
            temp_list.append(user_mypage)
            temp_list.append(title_url_list[i])
            temp_list.append(amazon_url)
                
            all_list.append(temp_list)
            time.sleep(interval)

def export_data():
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
#        writer.writerow(columns_name)
        for i in all_list:
            writer.writerow(i)




#    df = pd.DataFrame(all_list,columns=columns_name)#pandasのデータフレームに収納
#    with pd.ExcelWriter(file_name,options={'strings_to_urls': False}) as writer:
#        df.to_excel(writer, sheet_name="Sheet1")#Writerを通して書き込み
    
#タスクの実行    
get_data()
export_data()
print("end")
