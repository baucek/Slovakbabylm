import os 
import sys
import json
import regex as re 
from langdetect import detect


# file='C:/Users/Dell/Desktop/Diplomovka/Data/Wiki/output.json'
# vymazat este pred posjením listu
#       FILIT – zdroj, z ktorého pôvodne čerpal tento článok.
#       Oficiálna stránka Oficiálne stránky 
#       Toto je rozlišovacia stránka. 
#       Zdroje: INSEE
#       Zoznam NGC objektov
## samohlasky
##spoluhlasky


list_delete=['FILIT – zdroj, z ktorého pôvodne čerpal tento článok.','Oficiálna stránka','Oficiálna stránka','Zdroje: INSEE','Zoznam NGC objektov','Môže byť:']

diacritics = {
    '%C4%BE': 'ľ', '%C4%BD': 'Ľ',
    '%C5%88': 'ň', '%C5%87': 'Ň',
    '%C4%8D': 'č', '%C4%8C': 'Č',
    '%C5%A5': 'ť', '%C5%A4': 'Ť',
    '%C5%BE': 'ž', '%C5%BD': 'Ž',
    '%C5%99': 'ř', '%C5%98': 'Ř',
    '%C5%A0': 'š', '%C5%A1': 'Š',
    '%C4%8E': 'ď', '%C4%8D': 'Ď',
    '%C3%A1': 'á', '%C3%81': 'Á',
    '%C3%BA': 'ú', '%C3%9A': 'Ú',
    '%C3%B3': 'ó', '%C3%93': 'Ó',
    '%C3%A9': 'é', '%C3%89': 'É',
    '%C3%AD': 'í', '%C3%8D': 'Í',
    '%C3%BD': 'ý', '%C3%9D': 'Ý',
    '%C3%A4': 'ä', '%C3%84': 'Ä',
    '%C3%B4': 'ô', '%C3%94': 'Ô',
    '%C5%91': 'ő', '%C5%90': 'Ő',
    '%C5%B1': 'ű', '%C5%B0': 'Ű'
}


pattern = r'([^a-zA-Z0-9\s\.,!?;:\'\"])\1{2,}|\n\s*\n'



## pre-procesing and all books 



binary_pattern= r'\\u000[0-9a-fA-F]{1,4}'
page_pattern=r'(\d+/\d+|\n\s*\d|/\d+)'

markdowns_regex= re.compile(r'',flags=re.IGNORECASE)
# add del_list= ['è','¾','ã','','È','ß','Ð','æ']  



url_regex = re.compile(r'(?:((http|https):\/\/|www)(?:\w+|\.)(?:\S+|\.)?(?:\S+\.)?)|(?:.*?\.sk(?=[\s\p{P}\n]))',flags=re.IGNORECASE)
email_regex= re.compile(r'(\S+)(\.)?(\w+)@(\w+)(\.)(\S+)',flags=re.IGNORECASE)
punctuation_regex= re.compile(r'''([‘’~‟!\"#$%&'()*+,-.\/:;<=>?@[\\\]^_`{|}~])\1+''',flags=re.IGNORECASE)
brackets_regex=re.compile(r'\(.*?\)|\<.*?\>|\[.*?\]|\{.*?\}',flags=re.IGNORECASE)
phone_regex = re.compile(r'\d{5}[-\s]\d{4}[-\s]\d{4}|\d{3}/\s\d{3}\s\d{2}\s\d{2}',flags=re.IGNORECASE)


def replace_urls(text):
    text=url_regex.sub('<URL>',text)
    return text
def replace_emails(text):
    text=email_regex.sub('<EMAIL>',text)
    return text
def delete_brackets(text):
    text=brackets_regex.sub('',text)
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



def dia_function(text):
    for key, value in diacritics.items():
        if key in text:
            text = text.replace(key, value)
    return text



wiki_link_set=set()

# file='C:/Users/Dell/Desktop/Diplomovka/diploma_thesis/data/wiki/output_wiki_predmety.json'

for root, dirs, files in os.walk('C:/Users/Dell/Desktop/Diplomovka/Data/Wiki/full_wikisources'):
    for filename in files:
        wiki_f=[]  
        print(filename)
        with open(os.path.join(root, filename),encoding='utf-8') as data_file:    
            data = json.load(data_file)
            # total_word_count=0
            for i in data:
                if i['url'] not in wiki_link_set and not re.search(r'pedia\.org\/wiki\/Zoznam', i['url']) and detect(i['page']) == 'sk':
                    wiki_link_set.add(i['url'])
                    i['page']=''.join(i['page'])
                    for string_del in list_delete:
                        i['page']=delete_whole_line(string_del,i['page'])
                    i['url']=dia_function(i['url'])
                    isbn_index = i['page'].find("ISBN")
                    if isbn_index != -1:
                        i['page'] = i['page'][:isbn_index]
                    i['page']=replace_string(r'\[\d+\]','',i['page'])
                    i['page']=re.sub(r'([.,!?;:\'\"])\s+\1', r'\1', i['page']) # delete '. .'
                    i['page'] = re.sub(r'([.,!?;:\'\"])\n+\1', r'\1', i['page'])# delete '.\n.'
                    i['page'] = re.sub(pattern, '', i['page'])
                    i['page']=replace_urls(i['page'])
                    i['page']=replace_emails(i['page']) 
                    i['page']=replace_phones(i['page'])
                    i['page']=delete_brackets(i['page'])
                    i['page']=delete_double_newline(i['page'])
                    i['page']=delete_double_spaces(i['page'])
                    # print(i['url'])
                    if len(i['page']) > 500:
                        wiki_f.append(i)
        file_list=filename.split('.')
        filename_pr=file_list[0]+'_processed.'+file_list[1]
        root_pr=root+'/preprocessed/'
        with open(os.path.join(root_pr, filename_pr), 'a', encoding='utf-8') as json_output:
            json.dump( wiki_f, json_output, ensure_ascii=False, indent=4)       

# with open('C:/Users/Dell/Desktop/Diplomovka/diploma_thesis/data/wiki/processed_full_subj.json', 'a', encoding='utf-8') as json_output:
#     json.dump( wiki_f, json_output, ensure_ascii=False, indent=4)
