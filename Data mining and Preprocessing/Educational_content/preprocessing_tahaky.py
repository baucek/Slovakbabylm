import json
import re 
from langdetect import detect

# 
# Použitá literatúra ak sa najde viac ako jedna tak tá posledná alebo Zdroje:
# delete Fax, mobil, email, web, isbn

url_regex = re.compile(r'((http|https):\/\/|www)(\w+|\.)(\S+|\.)?(\S+|\.)?',flags=re.IGNORECASE)
email_regex= re.compile(r'(\S+)(\.)?(\w+)@(\w+)(\.)(\S+)',flags=re.IGNORECASE)
punctuation_regex= re.compile(r'''([‘’~‟!\"#$%&'()*+,-.\/:;<=>?@[\\\]^_`{|}~])\1+''',flags=re.IGNORECASE)
markdowns_regex= re.compile(r'',flags=re.IGNORECASE)
phone_regex = re.compile(r'\d{5}[-\s]\d{4}[-\s]\d{4}|\d{3}/\s\d{3}\s\d{2}\s\d{2}',flags=re.IGNORECASE)

def replace_urls(text):
    text=url_regex.sub('<URL>',text)
    return text
def replace_emails(text):
    text=email_regex.sub('<EMAIL>',text)
    return text
def replace_phones(text):
    text=phone_regex.sub('<TEL>',text)
    return text
def delete_markdowns(text):
    text=markdowns_regex.sub(' ',text)
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

list_sources=['Zdroje:','Zdroj:','ZDROJE:','ZDROJ:','POUŽITÁ LITERATÚRA:','Použitá literatúra:',
              'Použitá literatúra a zdroje:','POUŽITÁ LITERATÚRA A ZDROJE:','ZOZNAM POUŽITEJ LITERATÚRY','Zoznam použitej literatúry']

pattern = r'([^a-zA-Z0-9\s\.,!?;:\'\"])\1{2,}|\n\s*\n'
referarty_link_set=set()
edu_l=[]
with open('C:/Users/Dell/Desktop/Diplomovka/Data/educational/tahaky_referaty_2.json','r',encoding='utf-8') as file:
    data = json.load(file)

for source in data:
    if not source['url'] in referarty_link_set:
        referarty_link_set.add(source['url'])
        for str_source in list_sources:
            last_index=source['page'].rfind(str_source)
            if last_index == -1:
                continue
            source['page']=source['page'][:last_index]
        if detect(source['page']) != 'sk': 
            continue
        source['page']=replace_phones(source['page'])
        source['page']=replace_urls(source['page'])
        source['page']=replace_emails(source['page'])
        isbn_index = source['page'].find("ISBN")
        if isbn_index != -1:
            source['page'] = source['page'][:isbn_index]
        source['page']=re.sub(r'(\n{2,})', '\n',  source['page'])
        source['page']=re.sub(r'(/{2,})', '/', source['page'])
        source['page'] = re.sub(r'(\\{2,})', r'\\', source['page'])
        source['page'] = re.sub(r'(\.{3,})', '.', source['page'])
        source['page'] = re.sub(pattern, '', source['page'])
        source['page'] = re.sub(r'([.,!?;:\'\"])\n+\1', r'\1', source['page'])
        source['page'] = re.sub(r'([.,!?;:\'\"])\s+\1', r'\1', source['page'])
        source['page'] = delete_double_newline(source['page'])
        source['page'] = delete_double_spaces(source['page'])
        if len(source['page']) > 300:     
            print(source['url'])
            edu_l.append(source)

with open("C:/Users/Dell/Desktop/Diplomovka/Data/educational/tahaky_referaty-preprocessed.json", "w", encoding="utf-8") as f:
    json.dump(edu_l, f, ensure_ascii=False, indent=4)





