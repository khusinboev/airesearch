import csv
#from home.views import parallel
import os
import pandas as pd
#import textdistance as td
from corpus.settings import MEDIA_kiril
from corpus.settings import MEDIA_lotin
from corpus.settings import MEDIA_ROOT
from corpus.settings import MEDIA_Excel
from home.models import Document, MorfemLugat, Omonim, Paronim, Parallel, Ibora, Word, Doc, Davr, Uslub, Janr, parallelDoc, parallelLanguage, Sinonim, Daraja

import re 

def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

def sentToken(text):
    result=[]
    i=0
    while(i<len(text)):
        if(text[i]=='.' or text[i]=='!' or text[i]=='?'):
            result.append(text[:i+1])
            if(i+1<len(text)):                     
                text=text[i+1:]
                i=0
            else:
                break
        else:
            i+=1
    return result

def wordToken(text):
    result=[]
    i=0
    while(i<len(text)):
        if(text[i]==' '):
            result.append(text[:i])
            if(i+1<len(text)):                     
                text=text[i+1:]
                i=0
            else:
                break
        else:
            i+=1
    return result     

def findLemma(word):


    '''Tokenni chapdan o'nga lemmasini qidiramiz. Topilgan holda qo'shimchalarni lemmani turiga qarab qo'shimchalar modelidan izlanadi.
    modellar ichida uchramasa boshqa lemmani qidirishda davom etiladi'''
    kfile=open(os.path.join(MEDIA_Excel, 'kiril.txt'), 'r', encoding='utf-8')
    lfile=open(os.path.join(MEDIA_Excel, 'lotin.txt'), 'r', encoding='utf-8')
    tfile=open(os.path.join(MEDIA_Excel, 'tur.txt'), 'r', encoding='utf-8')
    sfile=open(os.path.join(MEDIA_Excel, 'Noun.txt'), 'r', encoding='utf-8')
    suffixes=[]
    forms=[]
    for i in sfile:
        forms.append(i)
        a=i.find(":")
        suffixes.append(i[a+1:])
    for i in range(len(suffixes)):
        if(suffixes[i].startswith('shahr')):
            suffixes[i]=suffixes[i][5:]
        #print(suffixes[i])
        else:
            suffixes[i]=suffixes[i][6:]
        #print(suffixes[i])
    kiril=[]
    for i in kfile:
        kiril.append(i)
    
    lotin=[]
    for i in lfile:
        lotin.append(i)
    tur=[]
    for i in tfile:
        tur.append(i)
    lemma=[word]
    for i in range(1, len(word)):
        if (word[:len(word) - i] + '\n' in kiril):
            #a = kiril.index(word[:len(word) - i] + '\n')
            #lemma.append(word[:len(word) - i])
            #lemma.append(tur[a][:-1])
            lemma=word[:len(word) - i]
            return lemma
        elif (word[:i] + '\n' in lotin):
            for st in range(len(suffixes)):
                if(suffixes[st]==word[i:]+'\n'):
                    #print("suffix :", word[i:])
                    ind=forms[st].find(':')
                    #print('form: ', word[:i]+forms[st][6:ind+1]+word)
                    lemma = word[:i]
                    return lemma    
    for i in range(1, len(word)):
        if(word[:i]+'\n' in kiril):
            a=kiril.index(word[:i]+'\n')
            lemma.append(word[:i])
            lemma.append(tur[a][:-1])
            return lemma
        elif(word[:i]+'\n' in lotin):            
            if(not (word[i:] in suffixes)):
                continue
            else:
                a=lotin.index(word[:i]+'\n')
                lemma.append(word[:i])
                lemma.append(tur[a][:-1])
                return lemma

    return ['topilmadi']

def lemmaKiril(word, davrV, usluB):
    result=[]
    wordL=word.split()
    if(davrV=="0"):
        if(usluB=="0"):
            fileList =  list(Document.objects.filter(alpha='kirill'))
        else:
            fileList =  list(Document.objects.filter(alpha='kirill').filter(uslub=usluB))
    else:
        if(usluB=="0"):            
            fileList =  list(Document.objects.filter(alpha='kirill').filter(davr=davrV))
        else:
            fileList =  list(Document.objects.filter(alpha='kirill').filter(davr=davrV).filter(uslub=usluB))
    

    for j in fileList:                    
        f=open(j.fayl, 'r', encoding="utf-8") 
        wordsList=[]
        for i in f:
            wordsList.extend(wordToken(i))
        for i in range(len(wordsList)-len(wordL)):
            a=True
            for t in range(len(wordL)-1):
                if(wordsList[i+t].lower()!=wordL[t].lower()):
                    a=False
                    break
            if(a and wordsList[i+len(wordL)-1].lower() == wordL[-1].lower()):
                if(str(j.year).endswith(".0")):
                    metD=""
                    if(j.author!=None):
                        metD=str(j.author)+" «"+j.name+"» "+str(j.year)[:-2]
                    else:
                        metD=" «"+j.name+"» "+str(j.year)[:-2]

                    temp=[metD]
                else:
                    metD=""
                    if(j.author!=None):
                        metD=str(j.author)+" «"+j.name+"» "+str(j.year)
                    else:
                        metD=" «"+j.name+"» "+str(j.year)

                    temp=[metD]
                st=10
                while(st>0):
                    if(i-st>-1):
                        temp.append(wordsList[i-st])
                    else:
                        temp.append(" ")
                    st-=1
                for st in range(len(wordL)):
                    temp.append(wordsList[i+st])
                st=0
                while(st<10):
                    if(i+len(wordL)+st<len(wordsList)):
                        temp.append(wordsList[i+len(wordL)+st])
                    else:
                        temp.append(" ")
                    st+=1
                parag=[j.id, i]
                
                temp.append(parag)
                result.append(temp)
    return result

def lemmaLotin(word, davrV, usluB):
    result=[]
    wordL=word.split()
    if(davrV=="0"):
        if(usluB=="0"):
            fileList =  list(Document.objects.filter(alpha='lotin'))
        else:
            fileList =  list(Document.objects.filter(alpha='lotin').filter(uslub=usluB))
    else:
        if(usluB=="0"):            
            fileList =  list(Document.objects.filter(alpha='lotin').filter(davr=davrV))
        else:
            fileList =  list(Document.objects.filter(alpha='lotin').filter(davr=davrV).filter(uslub=usluB))

    for j in fileList:                
        f=open(j.fayl, 'r', encoding="utf-8") 
        wordsList=[]
        for i in f:
            wordsList.extend(wordToken(i))
        for i in range(len(wordsList)-len(wordL)):
            a=True
            for t in range(len(wordL)-1):
                if(wordsList[i+t].lower()!=wordL[t].lower()):
                    a=False
                    break
            if(a and wordsList[i+len(wordL)-1].lower() == wordL[-1].lower()):
                if(str(j.year).endswith(".0")):
                    metD=""
                    if(j.author!=None):
                        metD=str(j.author)+" «"+j.name+"» "+str(j.year)[:-2]
                    else:
                        metD=" «"+j.name+"» "+str(j.year)[:-2]

                    temp=[metD]
                else:
                    metD=""
                    if(j.author!=None):
                        metD=str(j.author)+" «"+j.name+"» "+str(j.year)
                    else:
                        metD=" «"+j.name+"» "+str(j.year)

                    temp=[metD]
                st=10
                while(st>0):
                    if(i-st>-1):
                        temp.append(wordsList[i-st])
                    else:
                        temp.append(" ")
                    st-=1
                for st in range(len(wordL)):
                    temp.append(wordsList[i+st])
                st=0
                while(st<10):
                    if(i+len(wordL)+st<len(wordsList)):
                        temp.append(wordsList[i+len(wordL)+st])
                    else:
                        temp.append(" ")
                    st+=1
                parag=[j.id, i]            
                temp.append(parag)
                result.append(temp)
    return result

def birikmaLotin(word, davrV, usluB):
    result=[]
    wordL=word.split()
    if(davrV=="0"):
        if(usluB=="0"):
            fileList =  list(Document.objects.filter(alpha='lotin'))
        else:
            fileList =  list(Document.objects.filter(alpha='lotin').filter(uslub=usluB))
    else:
        if(usluB=="0"):            
            fileList =  list(Document.objects.filter(alpha='lotin').filter(davr=davrV))
        else:
            fileList =  list(Document.objects.filter(alpha='lotin').filter(davr=davrV).filter(uslub=usluB))

    for j in fileList:                
        f=open(j.fayl, 'r', encoding="utf-8") 
        wordsList=[]
        for i in f:
            wordsList.extend(wordToken(i))
        for i in range(len(wordsList)-len(wordL)):
            a=True
            for t in range(len(wordL)-1):
                if(not wordsList[i+t].lower().startswith(wordL[t].lower())):
                    a=False
                    break
            if(a and wordsList[i+len(wordL)-1].lower().startswith(wordL[-1].lower())):
                if(str(j.year).endswith(".0")):
                    metD=""
                    if(j.author!=None):
                        metD=str(j.author)+" «"+j.name+"» "+str(j.year)[:-2]
                    else:
                        metD=" «"+j.name+"» "+str(j.year)[:-2]

                    temp=[metD]
                else:
                    metD=""
                    if(j.author!=None):
                        metD=str(j.author)+" «"+j.name+"» "+str(j.year)
                    else:
                        metD=" «"+j.name+"» "+str(j.year)

                    temp=[metD]
                st=10
                temp.append([])
                while(st>0):
                    if(i-st>-1):
                        temp[1].append(wordsList[i-st])
                    else:
                        temp[1].append(" ")
                    st-=1
                temp.append([])
                for st in range(len(wordL)):
                    temp[2].append(wordsList[i+st])
                st=0
                temp.append([])
                while(st<10):
                    if(i+len(wordL)+st<len(wordsList)):
                        temp[3].append(wordsList[i+len(wordL)+st])
                    else:
                        temp[3].append(" ")
                    st+=1
                parag=[j.id, i]            
                temp.append(parag)
                result.append(temp)
    return result

def birikmaKiril(word, davrV, usluB):
    result=[]
    wordL=word.split()
    if(davrV=="0"):
        if(usluB=="0"):
            fileList =  list(Document.objects.filter(alpha='kirill'))
        else:
            fileList =  list(Document.objects.filter(alpha='kirill').filter(uslub=usluB))
    else:
        if(usluB=="0"):            
            fileList =  list(Document.objects.filter(alpha='kirill').filter(davr=davrV))
        else:
            fileList =  list(Document.objects.filter(alpha='kirill').filter(davr=davrV).filter(uslub=usluB))

    for j in fileList:                
        f=open(j.fayl, 'r', encoding="utf-8") 
        wordsList=[]
        for i in f:
            wordsList.extend(wordToken(i))
        for i in range(len(wordsList)-len(wordL)):
            a=True
            for t in range(len(wordL)-1):
                if(not wordsList[i+t].lower().startswith(wordL[t].lower())):
                    a=False
                    break
            if(a and wordsList[i+len(wordL)-1].lower().startswith(wordL[-1].lower())):
                if(str(j.year).endswith(".0")):
                    metD=""
                    if(j.author!=None):
                        metD=str(j.author)+" «"+j.name+"» "+str(j.year)[:-2]
                    else:
                        metD=" «"+j.name+"» "+str(j.year)[:-2]

                    temp=[metD]
                else:
                    metD=""
                    if(j.author!=None):
                        metD=str(j.author)+" «"+j.name+"» "+str(j.year)
                    else:
                        metD=" «"+j.name+"» "+str(j.year)

                    temp=[metD]
                st=10
                temp.append([])
                while(st>0):
                    if(i-st>-1):
                        temp[1].append(wordsList[i-st])
                    else:
                        temp[1].append(" ")
                    st-=1
                temp.append([])
                for st in range(len(wordL)):
                    temp[2].append(wordsList[i+st])
                st=0
                temp.append([])
                while(st<10):
                    if(i+len(wordL)+st<len(wordsList)):
                        temp[3].append(wordsList[i+len(wordL)+st])
                    else:
                        temp[3].append(" ")
                    st+=1
                parag=[j.id, i]            
                temp.append(parag)
                result.append(temp)
    return result


'''
def getLemma(woord):
    lis=Word.objects.filter(wordLotin__startswith=woord[:1])
    k=len(woord)
    print(len(lis))
    lemma=""
    for i in lis:        
        if(len(i.wordLotin)<len(woord)):
            if(td.levenshtein(i.wordLotin, woord[:len(i.wordLotin)])<k):                    
                lemma=i.wordLotin
                k=td.levenshtein(i.wordLotin, woord[:len(i.wordLotin)])
                print(i.wordLotin, woord[:len(i.wordLotin)], k)
            if(td.levenshtein(i.wordLotin, woord[:len(i.wordLotin)])==k):
                if(len(i.wordLotin)>len(lemma)):                    
                    lemma=i.wordLotin
                    k=td.levenshtein(i.wordLotin, woord[:len(i.wordLotin)])
                    print(i.wordLotin, woord[:len(i.wordLotin)], k)
    print(lemma)
    return lemma'''

def searchFromLeft(tekst, word, gramm):
    gram=int(gramm)
    result = [word]
    
    indeks=tekst.lower().find(word.lower())    
    result.append(tekst[indeks+len(word):])
    if(indeks>0):
        tekst=tekst[:indeks]
    #while(len(tekst)>0):
        #if(tekst.)



    return result

def searchRight(tekst, word, gramm):
    return 0

def parallelUz(word, Guruh, Soz):
    result=[]
    if(Guruh=="Guruh"):
        a=Parallel.objects.filter(group__icontains=word)
        for i in a:
            result.append([[i.uzbSent,"",""], [i.engSent, "", ""]])
    if(Soz=="Soz"):
        a=Parallel.objects.filter(uzbWord__icontains=word)
        for i in a:
            result.append([[i.uzbSent,"",""], [i.engSent, "", ""]])
    alfabet='lotin'
    if(has_cyrillic(word)):
        alfabet='kirill'
    #return result
    fileList =  list(Document.objects.filter(alpha=alfabet).filter(uslub='parallel'))
    for files in fileList:
        df= pd.read_excel(r''+files.fayl)
        for i in range(len(df['word_uzbek'])):
            if(str(df['word_uzbek'][i]).__contains__(word)):
                a=str(df['word_uzbek'][i]).split(',')
                b=str(df['Word_english'][i]).split(',')
                s=''
                for j in range(len(a)):
                    if(a[j].__contains__(word) ):
                        s=b[j]
                ind=str(df['Text_uzbek'][i]).find(word)
                indeng=str(df['Text_english'][i]).find(s)
                uz=[str(df['Text_uzbek'][i])[:ind], word, str(df['Text_uzbek'][i])[ind+len(word):]]
                eng=[str(df['Text_english'][i])[:indeng], s, str(df['Text_english'][i])[indeng+len(s):]]
                result.append([uz, eng])
    return result

def parallelUzKor(word):
    result=[]    
    alfabet=2
    if(has_cyrillic(word)):
        alfabet=1
    #return result
    fileList =  list(parallelDoc.objects.filter(alpha=alfabet).filter(language=1))
    print(len(fileList))
    for files in fileList:
        df= pd.read_excel(r''+str(files.fayl))
        for i in range(len(df['word_uzbek'])):
            if(str(df['word_uzbek'][i]).lower().__contains__(word.lower())):
                
                uz=str(df['text_uzbek'][i])
                kor=str(df['text'][i])
                result.append([uz, kor])
    return result

def parallelUzTurk(word):
    result=[]    
    alfabet=2
    if(has_cyrillic(word)):
        alfabet=1
    #return result
    fileList =  list(parallelDoc.objects.filter(alpha=alfabet).filter(language=4))
    print(len(fileList))
    for files in fileList:
        df= pd.read_excel(r''+str(files.fayl))
        for i in range(len(df['word_uzbek'])):
            if(str(df['word_uzbek'][i]).lower().__contains__(word.lower())):                
                uz=str(df['text_uzbek'][i])
                turk=str(df['text'][i])
                result.append([uz, turk])
    return result




'''
 <!--{% else %}
            <a href="{{ base_url }}page={{ i }}">{{ i }}</a></li> -->'''

def parallelEng(word):
    path=os.path.join(MEDIA_Excel, 'parallel.xlsx')
    df= pd.read_excel(r''+path)
    result=[]
    for i in range(len(df['Word_english'])):
        if(str(df['word_uzbek'][i]).__contains__(word)):
            result.append([df['Text_uzbek'][i], df['Text_english'][i]])
    return result

def tokenKiril(word, davrV, usluB):
    result=[]
    wordL=word.split()
    davrS=list(Davr.objects.filter(id=davrV))[0].name
    uslubS=list(Uslub.objects.filter(id=usluB))[0].name
    if(davrV=="0"):
        if(usluB=="0"):
            fileList =  list(Doc.objects.filter(alpha=1))
        else:
            fileList =  list(Doc.objects.filter(alpha=1).filter(uslub=usluB))
    else:
        if(usluB=="0"):            
            fileList =  list(Doc.objects.filter(alpha=1).filter(davr=davrV))
        else:
            fileList =  list(Doc.objects.filter(alpha=1).filter(davr=davrV).filter(uslub=usluB))
    
    if(davrV=="0"):
        if(usluB=="0"):
            fileList1 =  list(Document.objects.filter(alpha='kirill'))
        else:
            fileList1 =  list(Document.objects.filter(alpha='kirill').filter(uslub=uslubS))
    else:
        if(usluB=="0"):            
            fileList1 =  list(Document.objects.filter(alpha='kirill').filter(davr=davrS))
        else:
            fileList1 =  list(Document.objects.filter(alpha='kirill').filter(davr=davrS).filter(uslub=uslubS))
    fileList.extend(fileList1)
    for j in fileList:
        if(not os.path.exists(str(j.fayl))):
            continue                         
        f=open(str(j.fayl), 'r', encoding="utf-8") 
        wordsList=[]
        for i in f:
            wordsList.extend(wordToken(i))
        for i in range(len(wordsList)-len(wordL)):
            a=True
            for t in range(len(wordL)-1):
                if(wordsList[i+t].lower()!=wordL[t].lower()):
                    a=False
                    break
            if(a and wordsList[i+len(wordL)-1].lower().startswith(wordL[-1].lower())):
                if(str(j.year).endswith(".0")):
                    metD=""
                    if(j.author!=None):
                        metD=str(j.author)+" «"+j.name+"» "+str(j.year)[:-2]
                    else:
                        metD=" «"+j.name+"» "+str(j.year)[:-2]

                    temp=[metD]
                else:
                    metD=""
                    if(j.author!=None):
                        metD=str(j.author)+" «"+j.name+"» "+str(j.year)
                    else:
                        metD=" «"+j.name+"» "+str(j.year)

                    temp=[metD]
                st=10
                while(st>0):
                    if(i-st>-1):
                        temp.append(wordsList[i-st])
                    else:
                        temp.append(" ")
                    st-=1
                for st in range(len(wordL)):
                    temp.append(wordsList[i+st])
                st=0
                while(st<10):
                    if(i+len(wordL)+st<len(wordsList)):
                        temp.append(wordsList[i+len(wordL)+st])
                    else:
                        temp.append(" ")
                    st+=1
                parag=[j.id, i]
                temp.append(parag)
                result.append(temp)
    return result

def tokenLotin(word, davrV, usluB):
    result=[]
    wordL=word.split()
    davrS=list(Davr.objects.filter(id=davrV))[0].name
    uslubS=list(Uslub.objects.filter(id=usluB))[0].name
    if(davrV=="0"):
        if(usluB=="0"):
            fileList =  list(Doc.objects.filter(alpha=2))
        else:
            fileList =  list(Doc.objects.filter(alpha=2).filter(uslub=usluB))
    else:
        if(usluB=="0"):            
            fileList =  list(Doc.objects.filter(alpha=2).filter(davr=davrV))
        else:
            fileList =  list(Doc.objects.filter(alpha=2).filter(davr=davrV).filter(uslub=usluB))
    
    if(davrV=="0"):
        if(usluB=="0"):
            fileList1 =  list(Document.objects.filter(alpha='lotin'))
        else:
            fileList1 =  list(Document.objects.filter(alpha='lotin').filter(uslub=uslubS))
    else:
        if(usluB=="0"):            
            fileList1 =  list(Document.objects.filter(alpha='lotin').filter(davr=davrS))
        else:
            fileList1 =  list(Document.objects.filter(alpha='lotin').filter(davr=davrS).filter(uslub=uslubS))
    fileList.extend(fileList1)
    for j in fileList:      
        if(not os.path.exists(str(j.fayl))):
            continue                     
        f=open(str(j.fayl), 'r', encoding="utf-8")
        wordsList=[]
        for i in f:
            wordsList.extend(wordToken(i))
        for i in range(len(wordsList)-len(wordL)):
            a=True
            for t in range(len(wordL)-1):
                if(wordsList[i+t].lower()!=wordL[t].lower()):
                    a=False
                    break
            if(a and wordsList[i+len(wordL)-1].lower().startswith(wordL[-1].lower())):
                if(str(j.year).endswith(".0")):
                    metaDat=""
                    if(j.author!=None):
                        metaDat=j.author+j.name+str(j.year)[:-2]
                    else:
                        metaDat=j.name+str(j.year)[:-2]
                    temp=[metaDat]
                else:
                    metaDat=""
                    if(j.author!=None):
                        metaDat=j.author+j.name+str(j.year)
                    else:
                        metaDat=j.name+str(j.year)
                    temp=[metaDat]
                st=10
                while(st>0):
                    if(i-st>-1):
                        temp.append(wordsList[i-st])
                    else:
                        temp.append(" ")
                    st-=1
                for st in range(len(wordL)):
                    temp.append(wordsList[i+st])
                st=0
                while(st<10):
                    if(i+len(wordL)+st<len(wordsList)):
                        temp.append(wordsList[i+len(wordL)+st])
                    else:
                        temp.append(" ")
                    st+=1
                parag=[j.id, i]
                temp.append(parag)
                result.append(temp)
    return result


def tokenKirilByAuthor(word, davrV, janrV, authorFilter):
    result=[]
    wordL=word.split()
    davrS=list(Davr.objects.filter(id=davrV))[0].name
    janrS=list(Janr.objects.filter(id=janrV))[0].name
    if(davrV=="0"):
        if(janrV=="0"):
            fileList =  list(Doc.objects.filter(alpha=1).filter(author=authorFilter))
        else:
            fileList =  list(Doc.objects.filter(alpha=1).filter(janr=janrV).filter(author=authorFilter))
    else:
        if(janrV=="0"):            
            fileList =  list(Doc.objects.filter(alpha=1).filter(davr=davrV).filter(author=authorFilter))
        else:
            fileList =  list(Doc.objects.filter(alpha=1).filter(davr=davrV).filter(janr=janrV).filter(author=authorFilter))
    
    if(davrV=="0"):
        if(janrV=="0"):
            fileList1 =  list(Document.objects.filter(alpha='kirill').filter(author=authorFilter))
        else:
            fileList1 =  list(Document.objects.filter(alpha='kirill').filter(janr=janrS).filter(author=authorFilter))
    else:
        if(janrV=="0"):            
            fileList1 =  list(Document.objects.filter(alpha='kirill').filter(davr=davrS).filter(author=authorFilter))
        else:
            fileList1 =  list(Document.objects.filter(alpha='kirill').filter(davr=davrS).filter(janr=janrS).filter(author=authorFilter))
    fileList.extend(fileList1)
    if(len(fileList)<3):
        fileList=list(Doc.objects.filter(alpha=1).filter(author=authorFilter))
        fileList.extend(list(Document.objects.filter(alpha='kirill').filter(author=authorFilter)))
    for j in fileList:
        if(not os.path.exists(str(j.fayl))):
            continue                         
        f=open(str(j.fayl), 'r', encoding="utf-8") 
        wordsList=[]
        for i in f:
            wordsList.extend(wordToken(i))
        for i in range(len(wordsList)-len(wordL)):
            a=True
            for t in range(len(wordL)-1):
                if(wordsList[i+t].lower()!=wordL[t].lower()):
                    a=False
                    break
            if(a and wordsList[i+len(wordL)-1].lower().startswith(wordL[-1].lower())):
                if(str(j.year).endswith(".0")):
                    metD=""
                    if(j.author!=None):
                        metD=str(j.author)+" «"+j.name+"» "+str(j.year)[:-2]
                    else:
                        metD=" «"+j.name+"» "+str(j.year)[:-2]

                    temp=[metD]
                else:
                    metD=""
                    if(j.author!=None):
                        metD=str(j.author)+" «"+j.name+"» "+str(j.year)
                    else:
                        metD=" «"+j.name+"» "+str(j.year)

                    temp=[metD]
                st=10
                while(st>0):
                    if(i-st>-1):
                        temp.append(wordsList[i-st])
                    else:
                        temp.append(" ")
                    st-=1
                for st in range(len(wordL)):
                    temp.append(wordsList[i+st])
                st=0
                while(st<10):
                    if(i+len(wordL)+st<len(wordsList)):
                        temp.append(wordsList[i+len(wordL)+st])
                    else:
                        temp.append(" ")
                    st+=1
                parag=[j.id, i]
                temp.append(parag)
                result.append(temp)
    return result


def tokenLotinByAuthor(word, davrV, janrV, authorFilter):
    result=[]
    wordL=word.split()
    davrS=list(Davr.objects.filter(id=davrV))[0].name
    if(janrV==1):
        janrList=list(Janr.objects.filter(id=2))
    else:
        janrList=list(Janr.objects.filter(id=janrV))
    if(len(janrList)>0):
        janrS=janrList[0].name
    else:
        janrS=list(Janr.objects.all)[0].name
    if(davrV=="0"):
        if(janrV=="0"):
            fileList =  list(Doc.objects.filter(alpha=2).filter(author=authorFilter))
        else:
            fileList =  list(Doc.objects.filter(alpha=2).filter(janr=janrV).filter(author=authorFilter))
    else:
        if(janrV=="0"):            
            fileList =  list(Doc.objects.filter(alpha=2).filter(davr=davrV).filter(author=authorFilter))
        else:
            fileList =  list(Doc.objects.filter(alpha=2).filter(davr=davrV).filter(janr=janrV).filter(author=authorFilter))
    print("FILEEE", fileList)
    if(davrV=="0"):
        if(janrV=="0"):
            fileList1 =  list(Document.objects.filter(alpha='lotin').filter(author=authorFilter))
        else:
            fileList1 =  list(Document.objects.filter(alpha='lotin').filter(janr=janrS).filter(author=authorFilter))
    else:
        if(janrV=="0"):            
            fileList1 =  list(Document.objects.filter(alpha='lotin').filter(davr=davrS).filter(author=authorFilter))
        else:
            fileList1 =  list(Document.objects.filter(alpha='lotin').filter(davr=davrS).filter(janr=janrS).filter(author=authorFilter))
    fileList.extend(fileList1)
    if(len(fileList)<3):
        fileList=list(Doc.objects.filter(alpha=2).filter(author=authorFilter))
        fileList.extend(list(Document.objects.filter(alpha='lotin').filter(author=authorFilter)))
    for j in fileList:
        if(not os.path.exists(str(j.fayl))):
            continue                         
        for i in findWordAuthor(str(j.fayl), word):
            if(str(j.year).endswith(".0")):
                metD=""
                if(j.author!=None):
                    metD=str(j.author)+" «"+j.name+"» "+str(j.year)[:-2]
                else:
                    metD=" «"+j.name+"» "+str(j.year)[:-2]

                temp=[metD]
            else:
                metD=""
                if(j.author!=None):
                    metD=str(j.author)+" «"+j.name+"» "+str(j.year)
                else:
                    metD=" «"+j.name+"» "+str(j.year)

                temp=[metD]
            temp.append(i)
            result.append(temp)
    return result


def findWordAuthor(fayl, word):
    openedFile=open(str(fayl), 'r', encoding="utf-8")
    result=[]
    lines=[]
    lineNumber=0
    for i in openedFile:
        lineNumber+=1

        lines.append(i)
        tempWords=wordToken(i)
        for j in tempWords:
            if(j.lower().startswith(word.lower())):
                if(lineNumber>1):
                    result.append([lines[lineNumber-2],lines[lineNumber-1]])
                else:
                    result.append(["", lines[lineNumber-1]])
    return result





'''
def tokenLotin(word, davrV, usluB):
    davrS=list(Davr.objects.filter(id=davrV))[0].name
    uslubS=list(Uslub.objects.filter(id=usluB))[0].name
    result=[]
    wordL=word.split()
    if(davrV=="0"):
        if(usluB=="0"):
            fileList =  list(Document.objects.filter(alpha='lotin'))
        else:
            fileList =  list(Document.objects.filter(alpha='lotin').filter(uslub=usluB))
    else:
        if(usluB=="0"):            
            fileList =  list(Document.objects.filter(alpha='lotin').filter(davr=davrV))
        else:
            fileList =  list(Document.objects.filter(alpha='lotin').filter(davr=davrV).filter(uslub=usluB))
    
    if(davrV=="0"):
        if(usluB=="0"):
            fileList1 =  list(Document.objects.filter(alpha='lotin'))
        else:
            fileList1 =  list(Doc.objects.filter(alpha='lotin').filter(uslub=uslubS))
    else:
        if(usluB=="0"):            
            fileList1 =  list(Doc.objects.filter(alpha='lotin').filter(davr=davrS))
        else:
            fileList1 =  list(Doc.objects.filter(alpha='lotin').filter(davr=davrS).filter(uslub=uslubS))
    fileList.extend(fileList1)

    for j in fileList:                 
        f=open(j.fayl, 'r', encoding="utf-8") 
        wordsList=[]
        for i in f:
            wordsList.extend(wordToken(i))
        for i in range(len(wordsList)-len(wordL)):
            a=True
            for t in range(len(wordL)-1):
                if(wordsList[i+t].lower()!=wordL[t].lower()):
                    a=False
                    break
            if(a and wordsList[i+len(wordL)-1].lower().startswith(wordL[-1].lower())):
                if(str(j.year).endswith(".0")):
                    temp=[j.author+" «"+j.name+"» "+str(j.year)[:-2]]
                else:
                    temp=[j.author+" «"+j.name+"» "+str(j.year)]
                st=10
                while(st>0):
                    if(i-st>-1):
                        temp.append(wordsList[i-st])
                    else:
                        temp.append(" ")
                    st-=1
                for st in range(len(wordL)):
                    temp.append(wordsList[i+st])
                st=0
                while(st<10):
                    if(i+len(wordL)+st<len(wordsList)):
                        temp.append(wordsList[i+len(wordL)+st])
                    else:
                        temp.append(" ")
                    st+=1
                parag=[j.id, i]
                temp.append(parag)

                result.append(temp)
    return result
'''




def phraseKiril(word, davrV, usluB):
    result=[]
    wordL=word.split()
    davrS=list(Davr.objects.filter(id=davrV))[0].name
    uslubS=list(Uslub.objects.filter(id=usluB))[0].name
    if(davrV=="0"):
        if(usluB=="0"):
            fileList =  list(Doc.objects.filter(alpha=1))
        else:
            fileList =  list(Doc.objects.filter(alpha=1).filter(uslub=usluB))
    else:
        if(usluB=="0"):            
            fileList =  list(Doc.objects.filter(alpha=1).filter(davr=davrV))
        else:
            fileList =  list(Doc.objects.filter(alpha=1).filter(davr=davrV).filter(uslub=usluB))
    
    if(davrV=="0"):
        if(usluB=="0"):
            fileList1 =  list(Document.objects.filter(alpha='kirill'))
        else:
            fileList1 =  list(Document.objects.filter(alpha='kirill').filter(uslub=uslubS))
    else:
        if(usluB=="0"):            
            fileList1 =  list(Document.objects.filter(alpha='kirill').filter(davr=davrS))
        else:
            fileList1 =  list(Document.objects.filter(alpha='kirill').filter(davr=davrS).filter(uslub=uslubS))
    fileList.extend(fileList1)

    for j in fileList:
        if(not os.path.exists(str(j.fayl))):
            continue
        f=open(str(j.fayl), 'r', encoding="utf-8") 
        wordsList=[]
        for i in f:
            wordsList.extend(wordToken(i))
        for i in range(len(wordsList)-len(wordL)):
            a=True
            for t in range(len(wordL)-1):
                if(wordsList[i+t].lower()!=wordL[t].lower()):
                    a=False
                    break
            if(a and wordsList[i+len(wordL)-1].lower().startswith(wordL[-1].lower())):
                if(str(j.year).endswith(".0")):
                    metD=""
                    if(j.author!=None):
                        metD=str(j.author)+" «"+j.name+"» "+str(j.year)[:-2]
                    else:
                        metD=" «"+j.name+"» "+str(j.year)[:-2]

                    temp=[metD]
                else:
                    metD=""
                    if(j.author!=None):
                        metD=str(j.author)+" «"+j.name+"» "+str(j.year)
                    else:
                        metD=" «"+j.name+"» "+str(j.year)

                    temp=[metD]
                st=10
                while(st>0):
                    if(i-st>-1):
                        temp.append(wordsList[i-st])
                    else:
                        temp.append(" ")
                    st-=1
                for st in range(len(wordL)):
                    temp.append(wordsList[i+st])
                st=0
                while(st<10):
                    if(i+len(wordL)+st<len(wordsList)):
                        temp.append(wordsList[i+len(wordL)+st])
                    else:
                        temp.append(" ")
                    st+=1
                parag=[j.id, i]
                temp.append(parag)                
                result.append(temp)
    return result

def phraseLotin(word, davrV, usluB):
    result=[]
    wordL=word.split()
    davrS=list(Davr.objects.filter(id=davrV))[0].name
    uslubS=list(Uslub.objects.filter(id=usluB))[0].name
    if(davrV=="0"):
        if(usluB=="0"):
            fileList =  list(Doc.objects.filter(alpha=2))
        else:
            fileList =  list(Doc.objects.filter(alpha=2).filter(uslub=usluB))
    else:
        if(usluB=="0"):            
            fileList =  list(Doc.objects.filter(alpha=2).filter(davr=davrV))
        else:
            fileList =  list(Doc.objects.filter(alpha=2).filter(davr=davrV).filter(uslub=usluB))
    
    if(davrV=="0"):
        if(usluB=="0"):
            fileList1 =  list(Document.objects.filter(alpha='lotin'))
        else:
            fileList1 =  list(Document.objects.filter(alpha='lotin').filter(uslub=uslubS))
    else:
        if(usluB=="0"):            
            fileList1 =  list(Document.objects.filter(alpha='lotin').filter(davr=davrS))
        else:
            fileList1 =  list(Document.objects.filter(alpha='lotin').filter(davr=davrS).filter(uslub=uslubS))
    fileList.extend(fileList1)

    for j in fileList:
        if(not os.path.exists(str(j.fayl))):
            continue
        f=open(str(j.fayl), 'r', encoding="utf-8")
        wordsList=[]
        for i in f:
            wordsList.extend(wordToken(i))
        for i in range(len(wordsList)-len(wordL)):

            a=True
            for t in range(len(wordL)-1):
                if(wordsList[i+t].lower()!=wordL[t].lower()):
                    a=False
                    break
            if(a and wordsList[i+len(wordL)-1].lower().startswith(wordL[-1].lower())):
                if(str(j.year).endswith(".0")):
                    metD=""
                    if(j.author!=None):
                        metD=str(j.author)+" «"+j.name+"» "+str(j.year)[:-2]
                    else:
                        metD=" «"+j.name+"» "+str(j.year)[:-2]

                    temp=[metD]
                else:
                    metD=""
                    if(j.author!=None):
                        metD=str(j.author)+" «"+j.name+"» "+str(j.year)
                    else:
                        metD=" «"+j.name+"» "+str(j.year)

                    temp=[metD]
                st=10
                while(st>0):
                    if(i-st>-1):
                        temp.append(wordsList[i-st])
                    else:
                        temp.append(" ")
                    st-=1
                for st in range(len(wordL)):
                    temp.append(wordsList[i+st])
                st=0
                while(st<10):
                    if(i+len(wordL)+st<len(wordsList)):
                        temp.append(wordsList[i+len(wordL)+st])
                    else:
                        temp.append(" ")
                    st+=1
                parag=[j.id, i]
                temp.append(parag)
                result.append(temp)
    return result

def edu(word):
    result=[]
    wordL=word.split()
    fileList=Document.objects.filter(nashr__contains='sinf')
    #fileList1=Doc.objects.filter(nashr_contains='sinf')
    #fileList.extend(fileList1)

    for j in fileList:           
        f=open(j.fayl, 'r', encoding="utf-8") 
        wordsList=[]
        for i in f:
            wordsList.extend(wordToken(i))
        for i in range(len(wordsList)-len(wordL)):
            a=True
            for t in range(len(wordL)-1):
                if(wordsList[i+t].lower()!=wordL[t].lower()):
                    a=False
                    break
            if(a and wordsList[i+len(wordL)-1].lower().startswith(wordL[-1].lower())):
                temp=[j.nashr+" "+j.author+" "+j.name+" "]
                st=10
                while(st>0):
                    if(i-st>-1):
                        temp.append(wordsList[i-st])
                    else:
                        temp.append(" ")
                    st-=1
                for st in range(len(wordL)):
                    temp.append(wordsList[i+st])
                st=0
                while(st<10):
                    if(i+len(wordL)+st<len(wordsList)):
                        temp.append(wordsList[i+len(wordL)+st])
                    else:
                        temp.append(" ")
                    st+=1
                parag=[j.id, i]
                temp.append(parag)
                result.append(temp)
    return result


def findSinonim(alfabet, word):
    if(alfabet==1):
        sinRes=Sinonim.objects.filter(wordKiril__contains=word)
        
        sinList=[]
        sinonimFound=False
        for i in sinRes:
            sinList.append(i.wordKiril.split(", "))
            print(sinList[-1])
            for j in sinList[-1]:
                if(j.lower()==word.lower()):
                    sinList[-1].remove(word)
                    sinonimFound=True
                    break
            if(sinonimFound):
                break
    else:
        '''Ikki xil holat bo'lishi mumkin. Birinchi holatda qidirilayotgan so'z birga bir mos tushadi.
        Ikkinchi holatda qidirilayotgan so'z bazadagi so'zni affixi b'ladi. '''
        sinRes=Sinonim.objects.filter(wordLotin__contains=word)
        sinList=[]
        sinonimFound=False
        for i in sinRes:
            sinList.append(i.wordLotin.split(", "))
            for j in sinList[-1]:
                if(j.lower()==word.lower()):
                    sinList[-1].remove(word),
                    sinonimFound=True
                    break
            if(sinonimFound):
                break
    if(sinonimFound):
        return sinList[-1]           
    else:
        return ["Ma'lumot mavjud emas"]

def findDaraja(alfabet, word):
    if(alfabet==1):
        darRes=Daraja.objects.filter(wordKiril__contains=word)
        bir, ikki, uch=[], [], []
        darList=[]
        sinonimFound=False
        for i in darRes:
            darList.append(i.wordKiril.split(", "))
            
            for j in range(len(darList[-1])):
                if(darList[-1][j].lower()==word.lower()):
                    if(j>0):
                        bir=darList[-1][:j]
                    else:
                        bir=[]
                    ikki=darList[-1][j]
                    if(j<len(darList[-1])-1):
                        uch=darList[-1][j+1:]
                    else:
                        uch=[]                    
                    sinonimFound=True
                    break
            if(sinonimFound):
                break
    else:
        '''Ikki xil holat bo'lishi mumkin. Birinchi holatda qidirilayotgan so'z birga bir mos tushadi.
        Ikkinchi holatda qidirilayotgan so'z bazadagi so'zni affixi b'ladi. '''
        darRes=Daraja.objects.filter(wordLotin__contains=word)
        bir, ikki, uch=[], [], []
        darList=[]
        sinonimFound=False
        for i in darRes:
            darList.append(i.wordLotin.split(", "))
            
            for j in range(len(darList[-1])):
                if(darList[-1][j].lower()==word.lower()):
                    if(j>0):
                        bir=darList[-1][:j]
                    else:
                        bir=[]
                    ikki=darList[-1][j]
                    if(j<len(darList[-1])-1):
                        uch=darList[-1][j+1:]
                    else:
                        uch=[]                    
                    sinonimFound=True
                    break
            if(sinonimFound):
                break
    if(sinonimFound):
        return [bir, ikki, uch]         
    else:
        return [["Ma'lumot mavjud emas"], [],[]]

def findOmonim(alfabet, word):
    res=[]
    if(alfabet==1):
        omonimRes=Omonim.objects.filter(wordKiril__iexact=word)
        for i in omonimRes:
            res.append([i.turkum, i.izohKiril, i.misolKiril])
    else:
        omonimRes=Omonim.objects.filter(wordLotin__iexact=word)
        for i in omonimRes:
            res.append([i.turkum, i.izohLotin, i.misolLotin])
    return res
    
def findParonim(alfabet, word):
    
    res=[]
    if(alfabet==1):
        paronimRes=Paronim.objects.filter(kiril1__iexact=word)
        if(len(paronimRes)>0):
            res=[paronimRes[0].kiril3, paronimRes[0].kiril4]
        else:
            paronimRes=Paronim.objects.filter(kiril3__iexact=word)
            if(len(paronimRes)>0):
                res=[paronimRes[0].kiril1, paronimRes[0].kiril2]
    else:
        paronimRes=Paronim.objects.filter(lotin1__iexact=word)
        print(len(paronimRes))
        if(len(paronimRes)>0):
            res=[paronimRes[0].lotin3, paronimRes[0].lotin4]
        else:
            paronimRes=Paronim.objects.filter(lotin3__iexact=word)
            if(len(paronimRes)>0):
                res=[paronimRes[0].lotin1, paronimRes[0].lotin2]
    return res

def findIbora(alfabet, word):
    res=[]
    if(alfabet==1):
        iboralar=Ibora.objects.all()
        for i in iboralar:
            a=i.iboraKiril.split()
            j1=[]
            for j in a:
                j1.append(j.lower())
            for t in j1:
                if(t.startswith(word.lower())):
                    res.append([i.iboraKiril, i.izohKiril, i.sinonimKiril, i.antonimKiril])
                    break  
    else:        
        iboralar=Ibora.objects.all()
        for i in iboralar:
            a=i.ibora.split()
            j1=[]
            for j in a:
                j1.append(j.lower())
            for t in j1:
                if(t.startswith(word.lower())):
                    res.append([i.ibora, i.izoh, i.sinonim, i.antonim])
                    break                  
    return res

def findMorfema(alfabet, word):
    if(alfabet==1):
        morfRes=MorfemLugat.objects.filter(wordKiril__iexact=word)        
        if(len(morfRes)>0):
            morfList=morfRes[0].morfemKiril.split("/")
            res=morfList[0]
            if(len(morfList)>1):                
                for i in range(1, len(morfList)):
                    res=res+"-"+morfList[i]
            return res
        else:
            return word
        
    else:
        morfRes=MorfemLugat.objects.filter(wordLotin__iexact=word)
        print(word)
        print(len(morfRes))    
        if(len(morfRes)>0):
            print(morfRes[0].morfemLotin)
            morfList=morfRes[0].morfemLotin.split("/")
            print(morfList)
            res=morfList[0]
            if(len(morfList)>1):                
                for i in range(1, len(morfList)):
                    res=res+"-"+morfList[i]
            return res
        else:
            return word