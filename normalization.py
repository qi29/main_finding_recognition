import csv
import pandas as pd
from math import log, exp

def create_csv():
    path = "learning_scores.csv"
    with open(path,'wb') as f:
        csv_write = csv.writer(f)
        csv_head = ["PMID","index","ID","sentence","Word","Similarity","Pattern","BioSentStop","Distribution","LogNormalPattern","NormalSimilarityFixed","Distribution1","Distribution2","Distribution3","Distribution4","Distribution5","MaxNormalSimilarityFixed","MaxBioSentStop","NormalPattern","NormalWordFixed"]
        csv_write.writerow(csv_head)

def write_csv(PMID,index,ID,sentence,Word,Similarity,Pattern,BioSentStop,Distribution,LogNormalPattern,NormalSimilarityFixed,Distribution1,Distribution2,Distribution3,Distribution4,Distribution5,MaxNormalSimilarityFixed,MaxBioSentStop,NormalPattern,NormalWordFixed):
    path  = "learning_scores.csv"
    with open(path,'a+') as f:
        csv_write = csv.writer(f)
        data_row = [PMID,index,ID,sentence,Word,Similarity,Pattern,BioSentStop,Distribution,LogNormalPattern,NormalSimilarityFixed,Distribution1,Distribution2,Distribution3,Distribution4,Distribution5,MaxNormalSimilarityFixed,MaxBioSentStop,NormalPattern,NormalWordFixed]
        csv_write.writerow(data_row)
create_csv()

raw_scores=pd.read_csv('raw_scores.csv')

for raw_num in range(0,len(raw_scores)):
    PMID=raw_scores['PMID'][raw_num]
    index=raw_scores['index'][raw_num]
    ID=raw_scores['ID'][raw_num]
    sentence=raw_scores['sentence'][raw_num]
    Word=raw_scores['Word'][raw_num]
    Similarity=raw_scores['Similarity'][raw_num]
    Pattern=raw_scores['Pattern'][raw_num]
    BioSentStop=raw_scores['BioSentStop'][raw_num]
    Distribution=raw_scores['Distribution'][raw_num]
    # Pattern based scores Normalization
    Pattern_column=raw_scores['Pattern']
    max_pattern=max(Pattern_column)
    min_pattern=min(Pattern_column)
    NormalPattern=(raw_scores['Pattern'][raw_num]-min_pattern)/(max_pattern-min_pattern)
    # Distribution to dummy varibles
    Distribution1=0
    Distribution2=0
    Distribution3=0
    Distribution4=0
    Distribution5=0
    if raw_scores['Distribution'][raw_num]=="first":
        Distribution1=1
    elif raw_scores['Distribution'][raw_num]=="second":
        Distribution4=1
    elif raw_scores['Distribution'][raw_num]=="middle":
        Distribution3=1
    elif raw_scores['Distribution'][raw_num]=="second to last":
        Distribution5=1
    else:
        Distribution2=1
    # word based scores normalization: NormalWordFixed
    Word_column=raw_scores['Word']
    max_word=max(Word_column)
    min_word=min(Word_column)
    NormalWordFixed=(raw_scores['Word'][raw_num]-min_word)/(max_word-min_word)
    # N-grams based scores normalization: NormalSimilarityFixed
    max_similarity=max(raw_scores['Similarity'])
    NormalSimilarityFixed=log(float(raw_scores['Similarity'][raw_num]) + 1.0)/(log(max_similarity+1.0))
    # Pattern based scores log normalization: LogNormalPattern
    max_pattern=max(raw_scores['Pattern'])
    LogNormalPattern=log(float(raw_scores['Pattern'][raw_num]) + 1.0)/(log(max_pattern+1.0))
    # obtain the max NormalSimilarityFixed scores among one abstract MaxNormalSimilarityFixed
    MaxNormalSimilarityFixed=0.0
    for MaxNormalSimilarityFixed_num in range(0,len(raw_scores)):
        if raw_scores['PMID'][MaxNormalSimilarityFixed_num]==PMID:
            if log(float(raw_scores['Similarity'][MaxNormalSimilarityFixed_num]) + 1.0)/(log(max_similarity+1.0))>MaxNormalSimilarityFixed:
                MaxNormalSimilarityFixed=log(float(raw_scores['Similarity'][MaxNormalSimilarityFixed_num]) + 1.0)/(log(max_similarity+1.0))
    # obtain the max BioSentStop scores among one abstract: MaxBioSentStop
    MaxBioSentStop=0.0
    for MaxBioSentStop_num in range(0,len(raw_scores)):
        if raw_scores["PMID"][MaxBioSentStop_num]==PMID:
            if raw_scores["BioSentStop"][MaxBioSentStop_num]>=MaxBioSentStop:
                MaxBioSentStop=raw_scores["BioSentStop"][MaxBioSentStop_num]
    # obtain the max N-gram based similarity scores among one abstract: MaxSimilarity
    MaxSimilarity=0.0
    for MaxSimilarity_num in range(0,len(raw_scores)):
        if raw_scores["PMID"][MaxSimilarity_num]==PMID:
            if raw_scores["Similarity"][MaxSimilarity_num]>=MaxSimilarity:
                MaxSimilarity=raw_scores["Similarity"][MaxSimilarity_num]
    # insert normalization scores into csv
    write_csv(PMID,index,ID,sentence,Word,Similarity,Pattern,BioSentStop,Distribution,LogNormalPattern,NormalSimilarityFixed,Distribution1,Distribution2,Distribution3,Distribution4,Distribution5,MaxNormalSimilarityFixed,MaxBioSentStop,NormalPattern,NormalWordFixed)








    









