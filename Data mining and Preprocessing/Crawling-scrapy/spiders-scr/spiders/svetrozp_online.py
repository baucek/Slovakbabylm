
from bs4 import BeautifulSoup
import requests
import json



list_fair=[]

for i in range(1,7):
    page=f'https://rozpravky.online/page/{i}/'
    print(page)
    response = requests.get(page)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', class_='blog-card-more-link')
    hrefs = [link.get('href') for link in links]
    for fair_url in hrefs:
        response = requests.get(fair_url)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.findAll('div',class_="entry themeform")
        final_text=[]
        for x in table:
            for p in x.find_all(['p', 'h1', 'h2']):
                text=p.text.replace('\xa0',' ')
                final_text.append(text)
        if '        Ako sa vám páčila rozprávka?      ' in final_text:
            index = final_text.index('        Ako sa vám páčila rozprávka?      ')
            final_text = final_text[:index]
        data = {'url':fair_url,'page':final_text}
        list_fair.append(data)

with open('C:/Users/Dell/Desktop/Diplomovka/Data/Fairytales/rozpravky_online.json', 'w', encoding='utf-8') as json_file:
    json.dump(list_fair, json_file,indent=2,ensure_ascii=False)
