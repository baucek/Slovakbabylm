import requests
import os
import pandas as pd
import time 


def download_file(i,url):
    # filename = url.split('/')[-1]
    query_parameters = {"downloadformat": "zip"}
    response = requests.get(url,params=query_parameters)
    if response.status_code == 200:
        with open(f'C:\\Users\\Dell\\Desktop\\Diplomovka\\Data\\fairytales\\fairytales\\links\\{i}', 'wb') as f:
            f.write(response.content)
    elif response.status_code == 429:
            time.sleep(200)
            return


def load_urls_from_csv(excel_file):
    df = pd.read_csv(excel_file)
    urls = df['URL'].tolist()
    return urls


csv_file= 'C:\\Users\\Dell\\Desktop\\Diplomovka\\Data\\fairytales\\fairytales\\First_links.csv'
urls = load_urls_from_csv(csv_file)

for i, url in enumerate(urls):
    download_file(i,url)