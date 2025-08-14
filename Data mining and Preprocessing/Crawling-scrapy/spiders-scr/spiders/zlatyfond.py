
from bs4 import BeautifulSoup
import requests
import json
import re







# Kristína Royová kuknu5 sa na nu dokukal som po 

# Fairytales
def ZF(url,number):
    list_fair=[]
    number=number+1
    for i in range (1,number):
        final_text=[]
        response = requests.get(url+f'{i}')
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.findAll('div',attrs={"class":"chapter"})
        if not table:
            table = soup.findAll('div',attrs={"class":"odsadenie"})
        for x in table:
            for p in x.find_all(['p', 'h1', 'h2']):
                text=p.text.replace('\xa0',' ')
                text=re.sub(' +', ' ',text)
                final_text.append(text)
        data = {'url':url+f'{i}','page':final_text}
        list_fair.append(data)
    with open('C:/Users/Dell/Desktop/Diplomovka/Data/Fairytales/zlatyfond_rozpravky.json', 'a', encoding='utf-8') as json_file:
        json.dump(list_fair, json_file,indent=2,ensure_ascii=False)

ZF(f'https://zlatyfond.sme.sk/dielo/1693/Hranko_Burko/',5)
ZF(f'https://zlatyfond.sme.sk/dielo/648/Hranko_Furko-a-Murko/',1)
ZF(f'https://zlatyfond.sme.sk/dielo/1703/Hranko_Jezkovci/',1)
ZF(f'https://zlatyfond.sme.sk/dielo/629/Hranko_Kukucka/',1)
ZF(f'https://zlatyfond.sme.sk/dielo/1694/Hranko_Vrabciak-Tulko/',1)
ZF(f'https://zlatyfond.sme.sk/dielo/585/Dobsinsky_Prostonarodne-slovenske-povesti-Prvy-zvazok/',37)
ZF(f'https://zlatyfond.sme.sk/dielo/531/Dobsinsky_Prostonarodne-slovenske-povesti-Druhy-zvazok/',51)
ZF(f'https://zlatyfond.sme.sk/dielo/389/Dobsinsky_Prostonarodne-slovenske-povesti-Treti-zvazok/',66)
ZF(f'https://zlatyfond.sme.sk/dielo/5168/Corkran_Carodejnik-Severnej-tocny/',5)
ZF(f'https://zlatyfond.sme.sk/dielo/5169/Corkran_Anickina-navsteva-v-Zemi-Nedostatku/',5)
ZF(f'https://zlatyfond.sme.sk/dielo/4050/Podjavorinska_Zena/',1)
ZF(f'https://zlatyfond.sme.sk/dielo/3081/Podjavorinska_Isli-svrcky-poza-bucky/',52)
ZF(f'https://zlatyfond.sme.sk/dielo/4028/Podjavorinska_Carovne-skielka/',1)
ZF(f'https://zlatyfond.sme.sk/dielo/4032/Podjavorinska_Baranok-Bozi/',9)
ZF(f'https://zlatyfond.sme.sk/dielo/4053/Podjavorinska_Dobry-predaj/',1)
ZF(f'https://zlatyfond.sme.sk/dielo/3073/Podjavorinska_Zajko-Bojko/',17)
ZF(f'https://zlatyfond.sme.sk/dielo/3021/Podjavorinska_Cin-Cin/',29)
ZF(f'https://zlatyfond.sme.sk/dielo/903/Czambel_Slovenske-ludove-rozpravky-I/',55)
ZF(f'https://zlatyfond.sme.sk/dielo/903/Czambel_Slovenske-ludove-rozpravky-II/',25)
ZF(f'https://zlatyfond.sme.sk/dielo/178/Razus_Marosko/',23)
ZF(f'https://zlatyfond.sme.sk/dielo/1944/GregorTajovsky_Rozpravky-o-ceskoslovenskych-legiach-v-Rusku/',7)
ZF(f'https://zlatyfond.sme.sk/dielo/5194/Kipling_Kniha-dzungle/',8)
ZF(f'https://zlatyfond.sme.sk/dielo/5069/Kipling_Biely-tulen/',1)
ZF(f'https://zlatyfond.sme.sk/dielo/1383/Royova_Ako-Kvapocka-putovala/',1)
ZF(f'https://zlatyfond.sme.sk/dielo/4128/Royova_Ako-trpaslik-zabil-obra/',1)
ZF(f'https://zlatyfond.sme.sk/dielo/1385/Royova_Ako-zomieral-Slavicek/',1)
ZF(f'https://zlatyfond.sme.sk/dielo/1386/Royova_Stastlive-Vianoce/',1)



# 8
# https://zlatyfond.sme.sk/dielo/1811/Textorisova_Tri-rozpravky/3
# https://zlatyfond.sme.sk/dielo/1944/GregorTajovsky_Rozpravky-o-ceskoslovenskych-legiach-v-Rusku/7
# https://zlatyfond.sme.sk/dielo/3073/Podjavorinska_Zajko-Bojko/17 
# https://zlatyfond.sme.sk/dielo/4042/Podjavorinska_Ondras/1
# https://zlatyfond.sme.sk/dielo/1142/Francisci_Janko-Podhorsky/1 
# https://zlatyfond.sme.sk/dielo/459/Nadasi-Jege_Bubus-Bubulik-a-Bubulinko/1

# 'https://zlatyfond.sme.sk/dielo/128/Tajovsky_Mamka-Postkova/1',
# 'https://zlatyfond.sme.sk/dielo/547/Tajovsky_Do-konca/1'
# https://zlatyfond.sme.sk/dielo/133/Tajovsky_Horky-chlieb/5
# https://zlatyfond.sme.sk/dielo/1384/Royova_Ako-prisli-lastovicky-domov/1






### pdf to text ###
# import pdfplumber
# import os 

# for root, dirs, files in os.walk('C:/Users/Dell/Desktop/Diplomovka/Data/Fairytales/pdf'):
#     for filename in files:
#         with pdfplumber.open(os.path.join(root, filename)) as pdf:
#             text = ""
#             for number,page in enumerate(pdf.pages):
#                 # if number == 0:            
#                 #     string=page.extract_text()
#                 #     name= string.split('\n')[0]
#                 #     index = string.find('...')
#                 #     if index != -1:
#                 #         string=string[index+3:]
#                 #     text += name+'\n'+string
#                 #     continue
#                 text += page.extract_text()
#             with open(f"C:/Users/Dell/Desktop/Diplomovka/Data/Fairytales/pdf_text/{os.path.splitext(filename)[0]}.txt", "w",encoding='utf-8') as file:
#                 file.write(text)
