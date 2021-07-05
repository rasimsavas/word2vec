import requests
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize.regexp import WordPunctTokenizer
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd


DATA = {"url" : [],
        "segment_no" : [],
        "cumle_icerigi" : [],
        "sozcuk_sayisi" : []
        }

df = pd.DataFrame(DATA)
url = ""
df.to_csv (r'data.csv', index = False, header=True)
csvData = open("dataa.csv","r+",encoding="utf-8")
rssUrl = "https://www.canlihaber.com/rss/"
total_word = ""
word_len = 0
rsssayfa = requests.get(rssUrl)
rssparse = BeautifulSoup(rsssayfa.content,"lxml")
rssread = rssparse.find_all("guid")

for links in rssread:
    url = links.text
    adres  = requests.get(url)
    source = BeautifulSoup(adres.content,"lxml")
    sourcee = source.find_all("div",attrs={"id":"article-text"})
    if word_len > 10000:
                break
    for desc in sourcee:
        desc = desc.text
        desc = desc.replace("(adsbygoogle = window.adsbygoogle || []).push({});","")               
        desc = desc.replace("\n"," ")
        desc = desc.replace("‘","")
        desc = desc.replace("'","")      
        desc = desc.replace("?","")
        desc = desc.replace(".",". ")
        desc = desc.replace(r'”',"")
        desc = desc.replace(r"’"," ")
        desc = desc.replace(","," ")
        desc = desc.replace("“"," ")
        desc = desc.replace("    "," ")
        desc = desc.replace("...",".")
        desc = desc.replace("  "," ")
        sentens = sent_tokenize(desc)
        
        sayac = 0
        for cumle in sentens:
            kelime = word_tokenize(cumle,language='turkish')
            sayac +=1
            if len(kelime) > 2:
                df = df.append({'cumle_icerigi' : str(cumle),'url' : str(url),'segment_no' : str(sayac),'sozcuk_sayisi' : str(len(kelime)-1)}, ignore_index=True)
            else:
                continue
            word_len = word_len + len(kelime)-1
            if word_len > 10000:
                break
'''            
            if word_len > 10000:
                break
            for word in kelime:
                total_word = total_word + str(word + " ")
                total_word = total_word.replace("."," ")
                total_word = total_word.replace(",","")
                total_word = total_word.replace("  "," ")
                total_word = total_word.replace("\n","")
                
                word_len = len(total_word.split(" "))
                if word_len > 1000:
                    break
                #print(total_word)
                print(word_len)
'''            
df.to_csv (r'data.csv', index = False, header=True,encoding="utf-8-sig")
csvData.close()                     
