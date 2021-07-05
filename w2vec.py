import re
import csv
import gensim
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize.regexp import WordPunctTokenizer
import nltk
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from nltk.stem import WordNetLemmatizer

two_words= []
similarity = []
tum_kelimeler = []
tum_kelimeler2 = []
aranan_kelimeler = []
model_veri = []
lemmatizer = WordNetLemmatizer()

with open('data.csv',encoding="utf-8-sig", newline='\n') as csvfile:
    satirlar = csv.reader(csvfile, delimiter=',')
    for satir in satirlar:
        gecici = []
        for kelime in nltk.word_tokenize(satir[2]):
            tum_kelimeler.append(kelime)
            gecici.append(kelime.lower())
            tum_kelimeler2.append(kelime.lower())
        model_veri.append(gecici)

model = gensim.models.Word2Vec(model_veri, min_count = 1, size = 1000, window = 5) 

while True:
  num = input("Karsilastirilacak kelime sayisini giriniz: ")
  try:
    val = int(num)
    print("Girilen sayi degeri: ", val)
    j = 0
    while True:
        strVal = input(str(j+1)+". kelimeyi giriniz: \n----------------------------------------------------------------:")        
        if strVal in tum_kelimeler2:            
            aranan_kelimeler.append(strVal)
            j = j+1
            if j >= int(val):
                break
        else:           
            print("girdiginiz kelime corpusda mevcut degildir!!..\n----------------------------------------------------------------:")        
    break
  except ValueError:
      print ("String ifade girdiniz.. Lutfen bir numeric ifade giriniz..")
      
for i in range(len(aranan_kelimeler)):
    for j in range(len(aranan_kelimeler)):
        if i == j or i > j:
            continue
        else:
            print(aranan_kelimeler[i]," kelimesi ile ",aranan_kelimeler[j],"kelimesinin benzerliği: ",model.wv.similarity(aranan_kelimeler[i], aranan_kelimeler[j]))
            tmp = str(str(aranan_kelimeler[i]).upper() +"/" + str(aranan_kelimeler[j]).upper())
            two_words.append(tmp)
            similarity.append(model.wv.similarity(aranan_kelimeler[i], aranan_kelimeler[j]))
            
print("\n-----------------------------------------\nModeldeki toplam kelime sayisi: " + str(len(tum_kelimeler2)))
print("Modeldeki toplam birbirinden farkli kelime sayisi: " +str(len(set(tum_kelimeler))))


x = np.arange(len(two_words))  
width = 0.35  
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, similarity, width, label='DISTANCE')

ax.set_ylabel('DISTANCE')
ax.set_title('WORD2VEC')
ax.set_xticks(x)
ax.set_xticklabels(two_words)
ax.legend()

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')
        
autolabel(rects1)
fig.tight_layout()
fig.canvas.set_window_title('DOGAL DIL ISMELE ODEV')
mng = plt.get_current_fig_manager()
mng.resize(1440,960)
plt.show()

