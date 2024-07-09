import re
import xlrd
from xlrd import formula
import textdistance
from uniconGrant.settings import MEDIA_Excel
from contentanalyze.models import Word
import os
suff=[]
ksuff=[]
kvSuff=[]
vSuff=[]
words=[]
wordsKiril=[]
filename=os.path.join(MEDIA_Excel, 'lotin.xls')
wordFile=os.path.join(MEDIA_Excel, 'wordFull1.xls')
wordFile2=os.path.join(MEDIA_Excel, 'wordFull2.xls')
kSufFile=os.path.join(MEDIA_Excel, 'kirillSuff.xls')
wb = xlrd.open_workbook(filename)
kwb=xlrd.open_workbook(kSufFile)
sheet = wb.sheet_by_index(0)
ksheet=kwb.sheet_by_index(0)
wb1=xlrd.open_workbook(wordFile)
wb2=xlrd.open_workbook(wordFile2)
wordSheet=wb1.sheet_by_index(0)
wordSheet2=wb2.sheet_by_index(0)

for i in range(1, 65536):#88295):
    if(wordSheet.cell_value(i, 1)!="" and wordSheet.cell_value(i, 1)!=" "):
        words.append([wordSheet.cell_value(i, 1).lower(), wordSheet.cell_value(i, 2).lower()])

for i in range(1, 22760):#88295):
    if(wordSheet2.cell_value(i, 1)!="" and wordSheet2.cell_value(i, 1)!=" "):
        words.append([wordSheet2.cell_value(i, 1).lower(), wordSheet2.cell_value(i, 2).lower()])

for i in range(1, 65536):#88295):
    if(wordSheet.cell_value(i, 1)!="" and wordSheet.cell_value(i, 1)!=" "):
        wordsKiril.append([wordSheet.cell_value(i, 0).lower(), wordSheet.cell_value(i, 2).lower()])

for i in range(1, 22760):#88295):
    if(wordSheet2.cell_value(i, 1)!="" and wordSheet2.cell_value(i, 1)!=" "):
        wordsKiril.append([wordSheet2.cell_value(i, 0).lower(), wordSheet2.cell_value(i, 2).lower()])



for i in range(0, 1886):
    kvSuff.append([ksheet.cell_value(i, 2), ksheet.cell_value(i, 3)])

for i in range(0, 5254):
    ksuff.append([ksheet.cell_value(i, 0), ksheet.cell_value(i, 1)])

for i in range(0, 1886):
    vSuff.append([sheet.cell_value(i, 2), sheet.cell_value(i, 3)])

for i in range(0, 5254):
    suff.append([sheet.cell_value(i, 0), sheet.cell_value(i, 1)])

def findLemma(word):
    print(word)
    if(word.endswith(',') or word.endswith('.') or word.endswith('!') or word.endswith('?')):
        word=word[:-1]
    a=Word.objects.filter(wordLotin__iexact=word)
    print(len(a))
    if(len(a)>0):
        for i in words:
            if(i[0]==a[0].wordLotin):
                if(i[1].startswith('v')):
                    return word, "Verb+Imp.+P2+SG", i[1]
                elif(i[1].startswith('n')):
                    return word, "Noun+P3+SG", i[1]
                else:
                    return word, "", i[1]
    for i in words:
        if(len(i[0])<=len(word) and word.startswith(i[0])):
            if(i[0]==word):
                if(i[1].startswith('v')):
                    return word, "Verb+Imp.+P2+SG", i[1]
                elif(i[1].startswith('n')):
                    return word, "Noun+P3+SG", i[1]
                else:
                    return word, "", i[1]
            if(i[1].startswith('v')):
                for j in vSuff:
                    if(j[1]==word[len(i[0]):]):
                        return i[0], j[0], i[1]
            else:
                for j in suff:                    
                    if(j[1]==word[len(i[0]):]):
                        return i[0], j[0], i[1]
    lenLem=0
    found=False
    for i in words:
        if(len(i[0])<=len(word) and word.startswith(i[0])):
            if(len(i[0])>lenLem):
                lenLem=len(i[0])
                lemma=i[0]
                turkum=i[1]
                found=True
    if(found):
        return lemma, "", turkum
    else:
        return "", "", ""

def findLemmaKiril(word):
    if(word.endswith(',') or word.endswith('.') or word.endswith('!') or word.endswith('?')):
        word=word[:-1]
    a=Word.objects.filter(wordKiril__iexact=word)
    if(len(a)>0):
        for i in wordsKiril:
            if(i[0]==a[0].wordKiril):
                if(i[1].startswith('v')):
                    return word, "Verb+Imp.+P2+SG", i[1]
                elif(i[1].startswith('n')):
                    return word, "Noun+P3+SG", i[1]
                else:
                    return word, "", i[1]
    for i in wordsKiril:
        if(len(i[0])<=len(word) and word.startswith(i[0])):
            if(i[0]==word):
                if(i[1].startswith('v')):
                    return word, "Verb+Imp.+P2+SG", i[1]
                elif(i[1].startswith('n')):
                    return word, "Noun+P3+SG", i[1]
                else:
                    return word, "", i[1]

            if(i[1].startswith('v')):
                for j in kvSuff:
                    if(j[1]==word[len(i[0]):]):
                        return i[0], j[0], i[1]
            else:
                for j in ksuff:
                    if(j[1]==word[len(i[0]):]):
                        return i[0], j[0], i[1]
    lenLem=0
    found=False
    for i in wordsKiril:
        if(len(i[0])<=len(word) and word.startswith(i[0])):
            if(len(i[0])>lenLem):
                lenLem=len(i[0])
                lemma=i[0]
                turkum=i[1]
                found=True
    if(found):
        return lemma, "", turkum
    else:
        return "", "", ""
    
def findVariants(word):
    print("chaqirildi")
    variants=[]
    for i in words:
        if(textdistance.jaro_winkler(word, i[0], 0.1)>0.89):
            variants.append([i[0], textdistance.jaro_winkler(word, i[0], 0.1)])
            print("variant", i)
    v=sorted(variants, key=lambda x: x[1], reverse=True)
    if(len(v)>7):
        v=v[:7]
    return v

def findVariantskiril(word):
    variants=[]
    for i in wordsKiril:
        if(textdistance.jaro_winkler(word, i[0], 0.1)>0.89):
            variants.append([i[0], textdistance.jaro_winkler(word, i[0], 0.1)])
    v=sorted(variants, key=lambda x: x[1], reverse=True)
    if(len(v)>7):
        v=v[:7]
    return v