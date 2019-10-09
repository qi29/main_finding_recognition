import xlrd
import xlwt
from xlwt import Workbook
import csv
import nltk
from bs4 import BeautifulSoup
import string
import sent2vec
from sklearn.metrics.pairwise import cosine_similarity
import re
from nltk.parse import stanford
from nltk.parse.stanford import StanfordDependencyParser
import os
import sys

def readworkbook(workbookname,i):
    workbook = xlrd.open_workbook(workbookname)
    sheet = workbook.sheet_by_index(i)
    return sheet

def create_csv():
    path = xmlfile.replace(".xml","")+"_raw_scores.csv"
    with open(path,'wb') as f:
        csv_write = csv.writer(f)
        csv_head = ["PMID","index","ID","sentence","Word","Similarity","Pattern","BioSentStop","Distribution"]
        csv_write.writerow(csv_head)

def write_csv(PMID,index,ID,sentence,Word,Similarity,Pattern,BioSentStop,Distribution):
    path  = xmlfile.replace(".xml","")+"_raw_scores.csv"
    with open(path,'a+') as f:
        csv_write = csv.writer(f)
        data_row = [PMID,index,ID,sentence,Word,Similarity,Pattern,BioSentStop,Distribution]
        csv_write.writerow(data_row)


# print str(sys.argv[1])
source_text=sys.argv[1]
xmlfile=sys.argv[2]
create_csv()
title_abstract_sheet=readworkbook(source_text,0)
all_sentences_sheet=readworkbook(source_text,1)

content = open(xmlfile).read()
bs = BeautifulSoup(content, features="xml")
articles=bs.findAll('PubmedArticle')


# load model
model = sent2vec.Sent2vecModel()
model.load_model('BioSentVec_PubMed_MIMICIII-bigram_d700.bin')
dependencyparser=StanfordDependencyParser('stanfordnlp/stanford-parser-full-2018-10-17/stanford-parser.jar', 'stanfordnlp/stanford-parser-full-2018-10-17/stanford-parser-3.9.2-models.jar')

# load all sentences from sheet
num=0
while (num+1)<all_sentences_sheet.nrows:
    num=num+1
    PMID=all_sentences_sheet.cell(num,0).value
    
    index=all_sentences_sheet.cell(num,1).value
    ID=all_sentences_sheet.cell(num,2).value
    print ("sentences scoring:"+str(ID))
    sentence=all_sentences_sheet.cell(num,3).value
    title=''
    for title_abstract_sheet_num in range(1,title_abstract_sheet.nrows):
        if str(int(PMID))==str(int(title_abstract_sheet.cell(title_abstract_sheet_num,0).value)):
            title=title_abstract_sheet.cell(title_abstract_sheet_num,1).value
            break
    # # word based feature scoring
    word_frequency_sheet=readworkbook("word.xlsx",0)
    mainfindingwordsfre=nltk.word_tokenize(sentence)
    mainfindingwordsfre=list(set(mainfindingwordsfre))
    Word=0.0
    for mainfindingword in mainfindingwordsfre:
        for numberwordfre in range(1,61):
            wordin=word_frequency_sheet.cell(numberwordfre,0).value
            negativescore=word_frequency_sheet.cell(numberwordfre,6).value
            if mainfindingword==wordin:
                Word=Word-negativescore
        for numberwordfre in range(62,111):
            wordin=word_frequency_sheet.cell(numberwordfre,0).value
            positivescore=word_frequency_sheet.cell(numberwordfre,5).value
            if mainfindingword==wordin:
                Word=Word+positivescore
    
    # obtain sentence location
    Distribution=''
    for article in articles:
        abstracttexts=article.findAll('AbstractText')
        if str(int(PMID))==article.find('PMID').text:
            if len(abstracttexts)==1:
                abstract_xml=''
                for abstracttext in abstracttexts:
                    abstract_xml=abstract_xml+abstracttext.text+" "
                sentences_xml=nltk.sent_tokenize(abstract_xml)
                sentencenumber=0
                for sentence_xml in sentences_xml:
                    sentencenumber=sentencenumber+1
                    if sentence==sentence_xml:
                        if sentencenumber==1:
                            Distribution='first'
                        elif sentencenumber==2:
                            Distribution='second'
                        elif sentencenumber==len(sentences_xml):
                            Distribution='last'
                        elif sentencenumber==(len(sentences_xml)-1):
                            Distribution='second to last'
                        else:
                            Distribution='middle'
            else:
                sentencenumber=0
                for abstracttext in abstracttexts:
                    sentencenumber=sentencenumber+1
                    if abstracttext.text.find(sentence)!=-1 or sentence.find(abstracttext.text)!=-1:
                        if sentencenumber==1:
                            Distribution='first'
                        elif sentencenumber==2:
                            Distribution='second'
                        elif sentencenumber==len(abstracttexts):
                            Distribution='last'
                        elif sentencenumber==(len(abstracttexts)-1):
                            Distribution='second to last'
                        else:
                            Distribution='middle'

    # n-grams based similarity comparing to title
    sentencelower=sentence.lower()
    titlelower=title.lower()
    Similarity=0.00
    sentencelower_words=nltk.word_tokenize(sentencelower)
    #(8-2_gram)
    all_grams=''
    count_gram=8
    while count_gram>=2:
        for n in range(0,len(sentencelower_words)-(count_gram-1)):
            n_gram=''
            for sentence_lower_num in range(n,n+count_gram):
                n_gram=n_gram+sentencelower_words[sentence_lower_num]+" "
            if titlelower.find(n_gram)!=-1 and all_grams.find(n_gram)==-1:
                Similarity=Similarity+count_gram*count_gram
                all_grams=all_grams+n_gram+"#"
        count_gram=count_gram-1
    # 1_gram
    for n in range(0,len(sentencelower_words)):
        one_gram=sentencelower_words[n]
        file = open('stoplist1392.txt')
        lines = file.readlines()
        tag=0
        for line in lines:
            if line.lower().strip()==one_gram:
                tag=tag+1
                break
        if all_grams.find(one_gram)!=-1:
            tag=tag+1
        for c in string.punctuation:
            if c==one_gram:
                tag=tag+1
                break
        if tag==0 and titlelower.find(one_gram)!=-1:
            Similarity=Similarity+1

# biosetstop: semantic similarity comparing title
    BioSentStop=0.00
    file = open('stoplist1392.txt')
    lines = file.readlines()
    titlewords_biosetsimilar=nltk.sent_tokenize(title.lower())
    sentencewords_biosetsimilar=nltk.sent_tokenize(sentence.lower())
    for line in lines:
        stopword=line.strip()
        for titleword in titlewords_biosetsimilar:
            if stopword==titleword:
                titlewords_biosetsimilar.remove(titleword)
        for sentenceword in sentencewords_biosetsimilar:
            if stopword==sentenceword:
                sentencewords_biosetsimilar.remove(sentenceword)
    title_biosetsimilar=''
    sentence_biosetsimilar=''
    for titleword in titlewords_biosetsimilar:
        title_biosetsimilar=title_biosetsimilar+titleword+" "
    for sentenceword in sentencewords_biosetsimilar:
        sentence_biosetsimilar=sentence_biosetsimilar+sentenceword+" "
    titlevector=model.embed_sentence(title_biosetsimilar)
    mainfindingvector=model.embed_sentence(sentence_biosetsimilar)
    try:
        BioSentStopArray=cosine_similarity(titlevector,mainfindingvector)
    except:
        BioSentStopArray=BioSentStopArray
    else:
        BioSentStopArray=cosine_similarity(titlevector,mainfindingvector)
    BioSentStop=BioSentStopArray[0][0]


    # pattern based feature scoring
    Pattern=0.00
    pattern_sheet=readworkbook("Pattern.xlsx",0)
    for string_num in range(1,7):
        if re.search(pattern_sheet.cell(string_num,0).value,sentence.lower()):
            Pattern=Pattern+pattern_sheet.cell(string_num,1).value

    if sentence.split():
        res=list(dependencyparser.parse(sentence.lower().split()))
        for row in res[0].triples():
            rowtext=''.join(str(row))
            if rowtext.find("(u'we', u'PRP')")!=-1:
                for pattern_num in range(1,16):
                    if rowtext.find(pattern_sheet.cell(pattern_num,2).value)!=-1:
                        Pattern=Pattern+pattern_sheet.cell(pattern_num,3).value
    mainfindingwordspattern=nltk.word_tokenize(sentence.lower())
    if len(mainfindingwordspattern)>3:
        for first_three_num in range(1,38):
            if mainfindingwordspattern[0]+' '+mainfindingwordspattern[1]+' '+mainfindingwordspattern[2]==pattern_sheet.cell(first_three_num,4).value:
                Pattern=Pattern+pattern_sheet.cell(first_three_num,5).value
    # print str(ID)+";"+sentence.encode("utf-8")+";"+str(Word)+";"+str(Similarity)+";"+str(Pattern)+";"+str(BioSentStop)+";"+Distribution
    # insert all scores into csv
    write_csv(PMID,index,ID,sentence.encode("utf-8"),Word,Similarity,Pattern,BioSentStop,Distribution)
 
raw_scores=xmlfile.replace(".xml","")+"_raw_scores.csv"

os.system("python normalization.py %s %s" % (raw_scores,xmlfile))