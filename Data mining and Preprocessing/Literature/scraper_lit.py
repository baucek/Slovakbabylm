from bs4 import BeautifulSoup
import requests
import json
import regex as re 
import os
from langdetect import detect
import pymupdf




### greenie work with links###


file_name='C:/Users/Dell/Desktop/Diplomovka/Data/Literatura/links.txt'
gr='https://greenie.elist.sk/knihy.html'




# def greenie(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     rows = soup.find_all('tr')
#     for row in rows:    
#         if row.find('img', alt='Slovenčina'):
#             link=row.find('a', title='Zobraziť knihu')
#             link_book=link.get('href')
#             book_url=url.rsplit('/',1)[0] + '/' +link_book
#             #book site
#             if '.mp3' not in book_url:
#                 response=requests.get(book_url)
#                 book_web_con=BeautifulSoup(response.content, 'html.parser')
#                 link=book_web_con.find('a',title="Otvorenie v internetovom prehliadači, čítanie online bez sťahovania")
#                 if link:
#                     link_book_content=link.get('href')
#                     book_url.rsplit('/',1)[0] + '/' +link_book_content
#                     with open(file_name, "a") as file:
#                            file.write(book_url.rsplit('/',1)[0] + '/' +link_book_content+ '\n')

## check names 
# folder_path=''
# name_set= set()
# clean_links=''
# for root, dirs, files in os.walk('./Literatura'):
#     for file in files:
#         if file.endswith('.pdf'):
#             name = os.path.splitext(file)[0]
#             name_set.add(name)
# f = open("./Literatura/links.txt", "r")
# for i in f.readlines():
#     i=i.replace('\n', '')
#     last_part = i.split('/')[-1]
#     name = last_part.replace('.html', '')
#     if name not in name_set: 
#         clean_links+=i+'\n'
# with open('./Literatura/clean_greenie_links.txt', "w") as file:
#     file.write(clean_links)
# print('Done')

## change to text
# f = open("./Data/Literatura/clean_greenie_links.txt", "r")
# for i in f.readlines():
#     i=i.replace('\n', '')
#     response = requests.get(i)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     for table in soup.find_all('table'):
#         table.decompose()
#     div_to_remove = soup.find('div', id=re.compile(r'(O|o)bsah?.'))
#     if div_to_remove:
#         div_to_remove.decompose()
#     list_texts = [h.get_text(strip=True) for h in soup.find_all(['p','h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
#     texts=''.join(list_texts)
#     texts = texts.replace('knižnica,greenie.elist.sk', " ")
#     texts = texts.replace("\xa0", " ")
#     texts = texts.replace("\xe0", " ")
#     texts = texts.replace("\r\n", "\n")
#     texts= re.sub(r'\d+\/\d+', '', texts)  

#     with open('./Data/Literatura/clean_greenie_text.txt',"a",encoding='UTF-8') as file:
#         file.write('\n\n\n\n\n'+texts)

