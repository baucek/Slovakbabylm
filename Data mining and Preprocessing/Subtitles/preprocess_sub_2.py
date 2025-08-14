import re 
import json
import sys
from langdetect import detect
import os
path='C:/Users/Dell/Desktop/Diplomovka/Data/Subtitles'
del_list= ['è','¾','ã','','È','ß','Ð','æ']  
list_delete=['Preklad:','preklad:','časovanie:','Časovanie:','Korekcia:','Preklad a korekcia','Watch','Do you want subtitles for any video?',
             'Free Browser extension:','Umiestnite Vašu reklamu priamo tu.','osdb.link/ext','PoštovnéZDARMA.cz','Podpor nás a staň sa VIP členom, ',
             'odstrániš všetky reklamy z','Kontaktujte www.OpenSubtitles.org','Watch any video online with Open-SUBTITLES','Sleduj filmy online na yFilmy.sk','Subtitles by',
             'Podpor nás a staň sa VIP členom, odstrániš všetky reklamy z ','SK SUBTiTLES','Titulky:','tREmE','Link na stiahnutie:','preložil SoulM@te','preložila larelay','preklad a korekcie:\n',
             'translation:','Preložil:','Ohodnoť tieto titulky na','DVDRip.','titulky:','opensubtitles.org','Title','korekcie:'
             ]

# 23 791 po spracovani a odstraneni kopii


url_regex = re.compile(r'(?:((http|https):\/\/|www)(?:\w+|\.)(?:\S+|\.)?(?:\S+\.)?)|(?:.*?\.sk(?=[\s\p{P}\n]))',flags=re.IGNORECASE)
email_regex= re.compile(r'(\S+)(\.)?(\w+)@(\w+)(\.)(\S+)',flags=re.IGNORECASE)
punctuation_regex= re.compile(r'''([‘’~‟!\"#$%&'()*+,-.\/:;<=>?@[\\\]^_`{|}~])\1+''',flags=re.IGNORECASE)
phone_regex = re.compile(r'\d{5}[-\s]\d{4}[-\s]\d{4}|\d{3}/\s\d{3}\s\d{2}\s\d{2}',flags=re.IGNORECASE)


# add del_list= ['è','¾','ã','','È','ß','Ð','æ']  

class preprocessing_regex():
    def replace_urls(text):
        text=url_regex.sub('<URL>',text)
        return text
    def replace_emails(text):
        text=email_regex.sub('<EMAIL>',text)
        return text
    def replace_phones(text):
        text=phone_regex.sub('<TEL>',text)
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

def average_size(path):
    size_list=[]
    for root, dirs, files in os.walk(path):
        for filename in files:
            print(filename)
            if filename.endswith('.txt'):
                file_path = os.path.join(root, filename)
                file_size = os.path.getsize(file_path)
                size_list.append(file_size)
    return sum(size_list) / len(size_list)
    


import os
final_content=[]
average=average_size(path)
deleted_size=0
for root, dirs, files in os.walk(path):
    for filename in files:
        print(filename)
        if filename.endswith('.txt'):
            file_path = os.path.join(root, filename)
            file_size = os.path.getsize(file_path)
            if file_size > average:
                with open(os.path.join(root, filename), 'r', encoding='utf-8', errors="ignore") as file:
                    content = file.readlines()
                    text=" ".join(content)
                    if not any(element in text for element in del_list):
                        try:
                            if detect(text) == 'sk':
                                for string_del in list_delete:
                                    text=preprocessing_regex.delete_whole_line(string_del,text)
                                text=preprocessing_regex.replace_urls(text)
                                text=preprocessing_regex.replace_emails(text)
                                text=preprocessing_regex.replace_phones(text)
                                text=preprocessing_regex.replace_string(r'(<i|& #)','',text)
                                text=preprocessing_regex.delete_double_newline(text)
                                text=preprocessing_regex.replace_string('\n ','\n',text)
                                text = re.sub(r'([.,!?;:\'\"])\s+\1', r'\1', text) # delete '. .'
                                text = re.sub(r'([.,!?;:\'\"])\n+\1', r'\1', text)# delete '.\n.'    - -\n
                                text = re.sub(r'- -', r'', text)
                                text=preprocessing_regex.delete_double_punctuation(text)
                                text=preprocessing_regex.delete_double_spaces(text)
                                final_content.append({'url':filename,'page':text})
                        except:
                            print(f"empty: {filename}")
                            continue
            else:
                print(f'deleted:     {file_path}')
                deleted_size+=1

with open('C:/Users/Dell/Desktop/Diplomovka/Data/Subtitles/json_subtitles.json', 'a', encoding='utf-8') as json_output:
    json.dump( final_content, json_output, ensure_ascii=False, indent=4)
