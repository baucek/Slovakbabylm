
from langdetect import detect
from bs4 import BeautifulSoup
import requests
import json
from bs4.dammit import EncodingDetector
import time
import re
save=[]
# sub_pages=['https://referaty.aktuality.sk/pedagogika','https://referaty.aktuality.sk/pravo','https://referaty.aktuality.sk/psychologia']
# sub_pages=['https://referaty.aktuality.sk/socialna-praca','https://referaty.aktuality.sk/osobnosti']
# sub_pages=['https://referaty.aktuality.sk/maturita-odborne-predmety','https://referaty.aktuality.sk/maturita-historia','https://referaty.aktuality.sk/maturita-nauka-o-spolocno']
# sub_pages=['https://referaty.aktuality.sk/umenoveda','https://referaty.aktuality.sk/tahaky-informatika','https://referaty.aktuality.sk/tahaky-prirodne-vedy']
# sub_pages=['https://referaty.aktuality.sk/tahaky-slovensky-jazyk','https://referaty.aktuality.sk/tahaky-spolocenske-vedy','https://referaty.aktuality.sk/ostatne-osobnosti','https://referaty.aktuality.sk/sport']
# sub_pages=['https://referaty.aktuality.sk/tahaky-informatika','https://referaty.aktuality.sk/ekonomia','https://referaty.aktuality.sk/filozofia','https://referaty.aktuality.sk/nabozenstvo','https://referaty.aktuality.sk/nabozenstvo']
# sub_pages=['https://referaty.aktuality.sk/slovenske-dejiny','https://referaty.aktuality.sk/svetove-dejiny','https://referaty.aktuality.sk/autori','https://referaty.aktuality.sk/citatelsky-dennik','https://referaty.aktuality.sk/gramatika','https://referaty.aktuality.sk/literatura','https://referaty.aktuality.sk/slohy']
# sub_pages=['https://referaty.aktuality.sk/biologia','https://referaty.aktuality.sk/chemia','https://referaty.aktuality.sk/fyzika','https://referaty.aktuality.sk/geografia']
# sub_pages=['https://referaty.aktuality.sk/maturita-slovensky-jazyk','https://referaty.aktuality.sk/maturita-fyzika']
# sub_pages=['https://referaty.aktuality.sk/maturita-chemia','https://referaty.aktuality.sk/maturita-biologia','https://referaty.aktuality.sk/medicina','https://referaty.aktuality.sk/politologia-sociologia']
# sub_pages=[]
# sub_pages=[]

for sub_page in sub_pages:
    for i in range(0,100):
        sub_page_n = f'{sub_page}/strana-{i+1}'
        response=requests.get(sub_page_n)
        if response.status_code == 200:
            list_main_pages=[]
            soup = BeautifulSoup(response.content, 'html.parser')
            if  not soup.find('div', class_='upozornenie'):
                div_content = soup.find('tbody')
                a_elements = div_content.find_all('a')
                for element in a_elements:
                    href=element.get('href')
                    list_main_pages.append(href)
                for page in list_main_pages:
                    response = requests.get(page)
                    encoding = EncodingDetector.find_declared_encoding(response.content, is_html=True) 
                    soup = BeautifulSoup(response.text, 'lxml')

                    # decoded_content = response.content.decode('iso-8859-1')  # Or whatever encoding is detected
                    # soup = BeautifulSoup(decoded_content, 'lxml')
                    # soup= BeautifulSoup(response.text, 'lxml', from_encoding=encoding)



                    # encoding = detect(response.content)['encoding']
                    # response.encoding = encoding
                    # decoded_content = response.content.decode(encoding)
                    # soup = BeautifulSoup(decoded_content, 'lxml')


                    #preprocessing:
                    obsah= soup.find_all("div", class_="obsah")
                    text= obsah[0].get_text()
                    # Regex pattern to remove text starting from specified phrases
                    pattern = r"\n\s*(?:Zdroje:|Použitá literatúra:|internetové zdroje:).*"
                    text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)
                    text= re.sub(r"\[\d+\]", "", text)
                    text= text.replace('\xa0',' ')
                    text= text.replace('\r\n\r\n',' ')
                    text= re.sub(r'\s+', ' ', text)
                    if len(text) > 0:
                        if detect(text) == 'sk':
                                save.append({'url':response.url,'page': text})
            else:
                print(f'end of page {sub_page}')
                time.sleep(5)
                break
        else:
            print(f'end of page {sub_page}')
            time.sleep(5)
            break
with open('C:/Users/Dell/Desktop/Diplomovka/Data/educational/tahaky_referaty_2.json', 'a',encoding='utf-8') as f:
    json.dump(save, f,indent=2,ensure_ascii=False) 
print('It is done')