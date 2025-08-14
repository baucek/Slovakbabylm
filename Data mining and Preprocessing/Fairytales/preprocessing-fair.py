import pandas as pd 
import os 
from langdetect import detect
import json
import re 
from string import digits

url_regex = re.compile(r'(?:((http|https):\/\/|www)(?:\w+|\.)(?:\S+|\.)?(?:\S+\.)?)|(?:.*?\.sk(?=[\s\p{P}\n]))',flags=re.IGNORECASE)
email_regex= re.compile(r'(\S+)(\.)?(\w+)@(\w+)(\.)(\S+)',flags=re.IGNORECASE)
punctuation_regex= re.compile(r'''([‘’~‟!"#$%&'()*+,\-\:;<=>?@[\\\]^_`{|}~])\1+''',flags=re.IGNORECASE)
brackets_regex=re.compile(r'\[.*?\]', flags=re.IGNORECASE)
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


# pdf_text
# path='./Fairytales/pdf_text'
# all_fairyatles=''
# for filename in os.listdir(path):
#     if filename.endswith('.txt'):
#         filepath = os.path.join(path,filename)
#         with open(filepath,encoding='utf-8') as infile:
#             file_content = infile.read()
#             result = re.sub(r'\d+\/\d+|\d+\s*min\s*\d+\+|Prečítajte si príbeh', '', file_content)  
#             result=replace_urls(result)
#             result=replace_phones(result)
#             result=replace_emails(result)
#             remove_digits = str.maketrans('', '', digits)
#             res = result.translate(remove_digits)
#             all_fairyatles+='\n'+result
# with open('./Fairytales/all_pdf_text.txt', "w",encoding='utf-8') as text_file:
#     text_file.write(all_fairyatles)


### all json files ### 
# all_fairyatles=''
# with open('./Fairytales/full_fairytales.json',encoding='utf-8') as data_file:    
#     data = json.load(data_file)
# for line in data:
#     all_fairyatles+='\n\n'+line['page']
# with open('./Fairytales/json_fairytales.txt', "w",encoding='utf-8') as text_file:
#     text_file.write(all_fairyatles)

#### put fairytales json into one file ### 
# path='./Fairytales'
# full_dataset=[]
# for filename in os.listdir(path):
#     if filename.endswith(".json"):
#         file_path = os.path.join(path, filename)
#         with open(file_path,encoding='utf-8') as data_file:    
#             data = json.load(data_file)
#         for line in data:  
#             if 'Fairytale' in line.keys():
#                 line['url'] = None
#                 line['page'] = line.pop('Fairytale')
#             if isinstance(line['page'],list):
#                 line['page']=''.join(line['page'])
#         full_dataset.extend(data)
            
# with open("./full_fairytales.json", "w") as json_file:
#     json.dump(full_dataset, json_file)


# zones
# new_list=[]
# with open('C:/Users/Dell/Desktop/Diplomovka/Data/Fairytales/zones.json','r',encoding='utf-8') as data_file:    
#     data = json.load(data_file)
# for line in data: 
#     if not line['page']:
#         continue
#     if detect(line['page']) != 'sk': 
#         continue
#     line['page']=replace_phones(line['page'])
#     line['page']=replace_urls(line['page'])
#     line['page']=replace_emails(line['page'])
#     line['page']=delete_double_punctuation(line['page'])
#     line['page']=re.sub(r'\s{2,}',' ',line['page'])
#     new_list.append(line)
# with open('C:/Users/Dell/Desktop/Diplomovka/Data/Fairytales/zones.json', "w", encoding="utf-8") as f:    
#     json.dump(new_list, f,ensure_ascii=False, indent=4)


#sikovna mamina
# list_sources=['Autor:','<']
# new_list=[]
# with open('C:/Users/Dell/Desktop/Diplomovka/Data/Fairytales/sikovnamamina.json','r',encoding='utf-8') as data_file:    
#     data = json.load(data_file)
# for line in data: 
#     if not line['page']:
#         continue
#     line['page'] = [item for item in line['page'] if not any(sub in item for sub in list_sources)]
#     line['page']=' '.join(line['page'])
#     if detect(line['page']) != 'sk': 
#         continue
#     line['page']=replace_phones(line['page'])
#     line['page']=replace_urls(line['page'])
#     line['page']=replace_emails(line['page'])
#     line['page']=delete_double_punctuation(line['page'])
#     line['page']=line['page'].replace("\\", "") 
#     line['page']=re.sub(r'\s{2,}',' ',line['page'])
#     new_list.append(line)
# with open('C:/Users/Dell/Desktop/Diplomovka/Data/Fairytales/sikovnamamina_preprocessed.json', "w", encoding="utf-8") as f:    
#     json.dump(new_list, f,ensure_ascii=False, indent=4)


# created fairytales

# import os 
# import re
# import json 
# folder_path="C:\\Users\\Dell\\Desktop\\Diplomovka\\Data\\Fairytales\\created_fairytales"
# list_of_conv=[]
# for filename in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, filename)
#         with open(file_path, 'r',encoding='utf-8') as file:
#             content = file.read()
#             cleaned_text = re.sub(r'\n{3,}', '\n\n', content)
#             split_text = re.split(r'\n\d+\.\s', cleaned_text)
#             for text in split_text:
#                 source={}
#                 if text.strip() == '':
#                     continue
#                 lines=text.split('\n')
#                 conv='\n'.join(lines[1:])
#                 conv=re.sub(r'\n{2,}', '\n',conv)
#                 source['url']=lines[0]
#                 source['page']=conv
#                 if len(source['page']) >=100: 
#                     list_of_conv.append(source)
# with open('C:/Users/Dell/Desktop/Diplomovka/Data/Fairytales/created_fairytales.json', 'w',encoding='utf-8') as json_file:
#     json.dump(list_of_conv, json_file, indent=4, ensure_ascii=False)


### zlatyfond

# new_list=[]
# with open('C:/Users/Dell/Desktop/Diplomovka/Data/Fairytales/zlatyfond.json','r',encoding='utf-8') as data_file:    
#     data = json.load(data_file)
# for line in data: 
#     if not line['page']:
#         continue
#     line['page'] = [item for item in line['page'] if not re.match(r'^\[\d+\]', item)]
#     line['page'] =line['page'][1:]
#     line['page']=' '.join(line['page'])
#     if detect(line['page']) != 'sk': 
#         continue
#     line['page']= re.sub(r'\*\s', '', line['page'])
#     line['page']= re.sub(r'\[\d+\]', '', line['page'])
#     line['page']=phone_regex(line['page'])
#     line['page']=replace_urls(line['page'])
#     line['page']=replace_emails(line['page'])
#     line['page']=re.sub(r'\s{2,}',' ',line['page'])
#     line['page']=re.sub(r'\n{2,}',' ',line['page'])
#     new_list.append(line)
# with open('C:/Users/Dell/Desktop/Diplomovka/Data/Fairytales/zlatyfond_preprocessed.json', "w", encoding="utf-8") as f:    
#     json.dump(new_list, f,ensure_ascii=False, indent=4)



## rozprávky online 
# new_list=[]
# with open('C:/Users/Dell/Desktop/Diplomovka/Data/Fairytales/rozpravky_online.json','r',encoding='utf-8') as data_file:    
#     data = json.load(data_file)
# for line in data: 
#     if not line['page']:
#         continue
#     line['page']=' '.join(line['page'])
#     if detect(line['page']) != 'sk': 
#         continue
#     line['page']= re.sub(r'\*\s', '', line['page'])
#     line['page']= re.sub(r'\[\d+\]', '', line['page'])
#     line['page']=replace_phones(line['page'])
#     line['page']=replace_urls(line['page'])
#     line['page']=replace_emails(line['page'])
#     line['page']=re.sub(r'\s{2,}',' ',line['page'])
#     line['page']=re.sub(r'\n{2,}',' ',line['page'])
#     new_list.append(line)
# with open('C:/Users/Dell/Desktop/Diplomovka/Data/Fairytales/rozpravky_online_preprocessed.json', "w", encoding="utf-8") as f:    
#     json.dump(new_list, f,ensure_ascii=False, indent=4)


## svetrozpravok
# new_list=[]
# with open('C:/Users/Dell/Desktop/Diplomovka/Data/Fairytales/svetrozpravok.json','r',encoding='utf-8') as data_file:    
#     data = json.load(data_file)
# for line in data:
#     line['page']=' '.join(line['page'])
#     if detect(line['page']) != 'sk': 
#       continue
#     line['page']=replace_urls(line['page'])
#     line['page']=replace_emails(line['page'])
#     line['page']=replace_phones(line['page'])
#     line['page']=re.sub(r'\s{2,}',' ',line['page'])
#     line['page']=re.sub(r'\n{2,}',' ',line['page'])
#     new_list.append(line)
# with open('C:/Users/Dell/Desktop/Diplomovka/Data/Fairytales/svetrozpravok_preprocessed.json', "w", encoding="utf-8") as f:    
#     json.dump(new_list, f,ensure_ascii=False, indent=4)