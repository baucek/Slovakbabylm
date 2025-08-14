import chardet
import re 
import os 
from langdetect import detect
import json

### pdf to text ### 
list_delete=['Titul:','Autor: ','Ilustrácie: ','Zdroj: ','titul:','autor: ','ilustrácie: ','zdroj: ','.....','TITUL:'
             ,'AUTOR:','ILUSTRÁCIE:','ZDROJ:','Grafická úprava:','Jazyková úprava:','Posudzovatelia:','Názov originálu:','Obsah:','©','ISBN'
             ,'EAN','\nVydavateľ','\nVydanie','\nObsah','vydavateľstvo']

pattern = r'(-{2,}|\${2,}|\#{2,}|\n\s*\n)'

binary_pattern= r'\\u000[0-9a-fA-F]{1,4}'
## pre-procesing and all books 
time_read = r"\d+\s*min\s*\n\s*\d+\+"



url_regex = re.compile(r'(?:((http|https):\/\/|www)(?:\w+|\.)(?:\S+|\.)?(?:\S+\.)?)|(?:.*?\.sk(?=[\s\p{P}\n]))',flags=re.IGNORECASE)
email_regex= re.compile(r'(\S+)(\.)?(\w+)@(\w+)(\.)(\S+)',flags=re.IGNORECASE)
punctuation_regex= re.compile(r'''([‘’~‟!\"#$%&'()*+,-.\/:;<=>?@[\\\]^_`{|}~])\1+''',flags=re.IGNORECASE)
brackets_regex=re.compile(r'\(.*?\)|\<.*?\>|\[.*?\]|\{.*?\}',flags=re.IGNORECASE)
markdowns_regex= re.compile(r'',flags=re.IGNORECASE)
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




# pdf books
import pymupdf

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
    if all(num == average for num in pos_list[1:-1]) and pos_list[-1]!=average: # if last or first position is different against average of others 
            part= blocks[-1]["bbox"]
            page.add_redact_annot(pymupdf.Rect(part))
            page.apply_redactions()
    return page
    
full_books=[]
delete_page=0
path='C:\\Users\\Dell\\Desktop\\Diplomovka\\Data\\Fairytales\\pdf'
for name in os.listdir(path):
    if '.pdf' not in name:
        continue
    doc = pymupdf.open(os.path.join(path, name))
    try:
        text=''
        for page_num in range(len(doc)):
            if page_num == 0:
                continue
            page=doc.load_page(page_num)# iterate the document pages
            page=delete_footer_header(page)
            not_pro_text = page.get_text()
            if not_pro_text == '':
                delete_page=delete_page+1
                continue 
            if page_num == delete_page: #  # iterate the document pages
                continue
            try:
                if detect(not_pro_text) == 'sk' and not re.search(binary_pattern, not_pro_text):
                    if '....................' in not_pro_text or 'ISBN' in not_pro_text or 'vydavateľstvo' in not_pro_text:
                        continue
                    not_pro_text = not_pro_text.replace('\x0e', '').replace('\x06', '').replace('\x1f', '').replace('\t','')
                    not_pro_text=replace_string(r'ţ','ž',not_pro_text)
                    not_pro_text=replace_string(r'ć','ď',not_pro_text) 
                    for string_del in list_delete:
                        not_pro_text=delete_whole_line(string_del,not_pro_text)
                    not_pro_text = re.sub(pattern, '', not_pro_text)
                    not_pro_text=replace_emails(not_pro_text)
                    not_pro_text=replace_urls(not_pro_text)
                    not_pro_text=delete_double_punctuation(not_pro_text)
                    not_pro_text=delete_double_newline(not_pro_text)
                    not_pro_text=re.sub(r' {2,}', ' ',  not_pro_text)
                    not_pro_text=re.sub(r'^(?=(?:\D*\d){10}(?:(?:\D*\d){3})?$)[\d-]+$','',not_pro_text) #isbn
                    text=text+not_pro_text
            except:
                continue
        print(name)
        full_books.append({"url": name, "page": text})
    except Exception as e:
        print (e)
        continue

    
with open('C:\\Users\\Dell\\Desktop\\Diplomovka\\Data\\Fairytales\\PDF_fairytales.json', 'a', encoding='utf-8') as json_output:
    json.dump( full_books, json_output, ensure_ascii=False, indent=4)



#readmio pdf


def delete_footer_header(page):
    blocks = page.get_text("dict")["blocks"]
    pos_list=[]
    for block in blocks:
        pos_list.append(block['bbox'][0])
    if len(pos_list) <= 3:
        return page
    average=sum(pos_list[1:-1])/len(pos_list[1:-1])
    if all(num == average for num in pos_list[1:-1]) and pos_list[0]!=average or pos_list[-1]!=average: # if last or first position is different against average of others 
        for parts_text in [0,-1]:
            if pos_list[parts_text] != average: 
                part= blocks[parts_text]["bbox"]
                page.add_redact_annot(pymupdf.Rect(part))
        page.apply_redactions()
        return page
    else:
        return page

text=[]
import pymupdf
path='C:\\Users\\Dell\\Desktop\\Diplomovka\\Data\\Fairytales\\readmio'
for name in os.listdir(path):
    if '.pdf' not in name:
        continue
    doc = pymupdf.open(os.path.join(path, name))
    for page_num in range(len(doc)):
        page=doc.load_page(page_num)# iterate the document pages
        page=delete_footer_header(page)
        not_pro_text = page.get_text()
        if page.number == 0: 
            title=not_pro_text.split('\n')[0]
        if not_pro_text == '':
            continue
        try: 
                match = re.search(time_read, not_pro_text)
                if match:
                    not_pro_text=not_pro_text[match.end():]
                not_pro_text=delete_whole_line('www.readmio.sk',not_pro_text)
                not_pro_text=re.sub(r'\d+/\d+', '', not_pro_text)
                not_pro_text=delete_double_punctuation(not_pro_text)
                not_pro_text=delete_double_newline(not_pro_text)
                not_pro_text=re.sub(r' {2,}', ' ',  not_pro_text)
                text.append({"url": title, "page": not_pro_text})
        except:
            continue
    
with open('C:\\Users\\Dell\\Desktop\\Diplomovka\\Data\\Fairytales\\readmio.json', 'a', encoding='utf-8') as json_output:
    json.dump( text, json_output, ensure_ascii=False, indent=4)