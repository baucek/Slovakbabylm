
from bs4 import BeautifulSoup
import requests
import json
import regex as re 
import os
from langdetect import detect
import pymupdf



#preprocessing books:
# Greenie:
#    kniheKniha  ak po malom písmenku alebo bodke Nasleduje velke písmenko tak rozdeliť 
#    :http://;,http:/: neodstránil link lebo nestojí samostatne 
# text pdf: 
#    " E j ,  n e s t a r '  s a  t y  o  t o .  O  t o m  p o t o m !  A l e  k d e  j e  t e n  k r á l i k ,  č o  s a  v  N i t r e  p r i  
#    3 a viac medzier a 2 viac medzier 
#    ak je slovo samotne v medzi \n
#    Autor> 
#    Spojenie čísel a textu
#     vsetky mo zne do sledky
#    ____
#    ●
import chardet

### pdf to text ### 
list_delete=['Titul:','Autor: ','Autor obalky','Ilustrácie: ','Ilustrácia:','Zdroj: ','titul:','autor: ','ilustrácie: ','zdroj: ','.....','TITUL:'
             ,'AUTOR:','ILUSTRÁCIE:','ZDROJ:','Grafická úprava:','Jazyková úprava:','Posudzovatelia:','Názov originálu:','Obsah:','©','ISBN'
             ,'EAN','\nVydavateľ','\nVydanie','\nObsah','n\ÚVOD']


pattern = r'([^a-zA-Z0-9\s\.,!?;:\'\"])\1{2,}|\n\s*\n'

binary_pattern= r'\\u000[0-9a-fA-F]{1,4}'
page_pattern=r'(\d+/\d+|\n\s*\d|/\d+)'


## pre-procesing and all books 
# if last or first position is different against average of others
    


url_regex = re.compile(r'(?:((http|https):\/\/|www)(?:\w+|\.)(?:\S+|\.)?(?:\S+\.)?)|(?:.*?\.sk(?=[\s\p{P}\n]))',flags=re.IGNORECASE)
email_regex= re.compile(r'(\S+)(\.)?(\w+)@(\w+)(\.)(\S+)',flags=re.IGNORECASE)
punctuation_regex= re.compile(r'''([‘’~‟!\"#$%&'()*+,-.\/:;<=>?@[\\\]^_`{|}~])\1+''',flags=re.IGNORECASE)
brackets_regex=re.compile(r'\(.*?\)|\<.*?\>|\[.*?\]|\{.*?\}',flags=re.IGNORECASE)
phone_regex = re.compile(r'\d{5}[-\s]\d{4}[-\s]\d{4}|\d{3}/\s\d{3}\s\d{2}\s\d{2}',flags=re.IGNORECASE)

# add del_list= ['è','¾','ã','','È','ß','Ð','æ']  

def replace_urls(text):
    text=url_regex.sub('<URL>',text)
    return text
def replace_emails(text):
    text=email_regex.sub('<EMAIL>',text)
    return text
def replace_phones(text):
    text=phone_regex.sub('<TEL>',text)
    return text

def delete_brackets(text):
    text=brackets_regex.sub('',text)
    return text
def delete_double_punctuation(text):
    text=punctuation_regex.sub(' ',text)
    return text
def delete_double_spaces(text):
    text=re.sub(r'\s{2,}',' ',text)
    return text
def delete_double_newline(text):
    text=re.sub(r'(\n{2,}|\s*\n\s*\n\s*)', '\n', text)
    return text
def delete_whole_line(target,text):
    text= re.sub(r'^.*' + re.escape(target) + r'.*$\n?', "", text, flags=re.MULTILINE)
    return text
def replace_string(input,output,text):
    text=re.sub(input,output,text)
    return text

def delete_footer_header(page):
    blocks = page.get_text("dict")["blocks"]
    pos_list=[]
    for block in blocks:
        pos_list.append(block['bbox'][0])
    if len(pos_list) <= 3:
        return page
    average=sum(pos_list[1:-1])/len(pos_list[1:-1])
    if all(num == average for num in pos_list[1:-1]) and pos_list[0]!=average:
            part= blocks[0]["bbox"]
            page.add_redact_annot(pymupdf.Rect(part))
            page.apply_redactions()
    if all(num == average for num in pos_list[1:-1]) and pos_list[-1]!=average:  
            part= blocks[-1]["bbox"]
            page.add_redact_annot(pymupdf.Rect(part))
            page.apply_redactions()
    return page

name_files=[]
counter_text=0
path='C:\\Users\\Dell\\Desktop\\Diplomovka\\Data\\Literatura\\pdf books'
for folder in os.listdir(path):
    f = os.path.join(path, folder)
    full_books=[]
    for file in os.listdir(f):
        if file not in name_files:
            name_files.append(file)
            pdf_file = os.path.join(f, file)
            doc = pymupdf.open(pdf_file)
            delete_page=0
            try:
                text=''
                last_string_page=''
                for page_num in range(len(doc)):
                    page=doc.load_page(page_num)
                    page=delete_footer_header(page)
                    not_pro_text = page.get_text()
                    if not_pro_text == '':
                        delete_page=delete_page+1
                        continue 
                    if page_num == delete_page:
                        continue
                    try: 
                        if detect(not_pro_text) == 'sk' and  '.......'  not in not_pro_text  and  '. . . . . . . .'  not in not_pro_text and not 'ISBN' in not_pro_text and not re.search(binary_pattern, not_pro_text):
                            not_pro_text = not_pro_text.replace('\x0e', ' ').replace('\x06', ' ').replace('\x1f', ' ').replace('\t',' ').replace("\xa0", " ")
                            not_pro_text=replace_string(r'ţ','ž',not_pro_text)
                            not_pro_text=replace_string(r'ć','ď',not_pro_text) 
                            for string_del in list_delete:
                                not_pro_text=delete_whole_line(string_del,not_pro_text)
                            not_pro_text=replace_string(r'greenie.elist.sk','',not_pro_text)
                            not_pro_text=replace_string(r'eknizky.sk','',not_pro_text)
                            not_pro_text=replace_urls(not_pro_text)
                            not_pro_text=replace_phones(not_pro_text)
                            not_pro_text=replace_emails(not_pro_text)
                            not_pro_text = re.sub(pattern, '', not_pro_text)
                            not_pro_text=delete_double_newline(not_pro_text)
                            not_pro_text=re.sub(r'ISBN[\d\W]+?(?:\.|$)','',not_pro_text) #isbn
                            not_pro_text=re.sub(page_pattern,' ',not_pro_text)
                            not_pro_text=re.sub(r' {2,}', ' ',  not_pro_text)
                            not_pro_text = re.sub(r'([.,!?;:\'\"])\s+\1', r'\1', not_pro_text) # delete '. .'
                            not_pro_text = re.sub(r'([.,!?;:\'\"])\n+\1', r'\1', not_pro_text)# delete '.\n.'
                            not_pro_text = re.sub(r'\r \r', r'', not_pro_text)
                            if not_pro_text[-1] == '\n':
                                not_pro_text=not_pro_text[:-1]
                            if last_string_page == not_pro_text.split('\n')[-1]:
                                not_pro_text='\n'.join(not_pro_text.split('\n')[:-1])
                            else: 
                                last_string_page=not_pro_text.split('\n')[-1]
                            text=text+' '+not_pro_text
                    except:
                        continue
                print(file)
                if text: 
                    full_books.append({"url": file, "page": text})
            except Exception as e:
                continue 
        with open(f'C:/Users/Dell/Desktop/Diplomovka/Data/Literatura/{folder}_new_processed.json', 'a', encoding='utf-8') as json_output:
            json.dump( full_books, json_output, ensure_ascii=False, indent=4)


print('')






