# Copyright 2019, University of Illinois at Chicago
# This file is part of the main_finding_recognition project.
# See the ReadMe.txt for licensing information.

import os
from bs4 import BeautifulSoup
import xlrd
import xlwt
from xlwt import Workbook
import nltk
import sys

# print str(sys.argv[1])
inputxml=sys.argv[1]
# create new xlsx
Excel = Workbook(encoding='utf-8')
# sheet1 title and abstract
sheet1 = Excel.add_sheet('title_abstract')
sheet1.write(0,0,"PMID")
sheet1.write(0,1,"title")
sheet1.write(0,2,"abstract")
# sheet2 all sentences
sheet2=Excel.add_sheet('all_sentences')
sheet2.write(0,0,"PMID")
sheet2.write(0,1,"index")
sheet2.write(0,2,"ID")
sheet2.write(0,3,"sentence")


# parse .xml (first input file:pubmed_result.xml)
xml_file = inputxml
content = open(xml_file).read()
bs = BeautifulSoup(content, features="xml")
articles=bs.findAll('PubmedArticle')

# parse title and abstract, insert into xlsx
title_abstract_num=1
all_sentences_num=1
for article in articles:
    PMID=article.find("PMID").text
    sheet1.write(title_abstract_num,0,PMID)
    title=article.find("ArticleTitle").text
    sheet1.write(title_abstract_num,1,title)
    abstract=''
    abstracttexts=article.findAll('AbstractText')
    for abstracttext in abstracttexts:
        abstract=abstract+abstracttext.text+" "
    sheet1.write(title_abstract_num,2,abstract)
    title_abstract_num=title_abstract_num+1
    print ("parsing article:"+str(PMID))

# parse senencese in abstract, insert into xlsx
    sentences=nltk.sent_tokenize(abstract)
    sentence_index=1
    for sentence in sentences:
        sheet2.write(all_sentences_num,0,PMID)
        sheet2.write(all_sentences_num,1,sentence_index)
        sheet2.write(all_sentences_num,2,str(PMID)+";"+str(sentence_index))
        sheet2.write(all_sentences_num,3,sentence)
        all_sentences_num=all_sentences_num+1
        sentence_index=sentence_index+1
source_text=inputxml.replace(".xml","")+'_source_text.xls'
Excel.save(source_text)
os.system("python sentences_scoring_raw.py %s %s" % (source_text,inputxml))
