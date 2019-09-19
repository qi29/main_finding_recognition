import xlrd
import pandas as pd
import csv

def readworkbook(workbookname,i):
    workbook = xlrd.open_workbook(workbookname)
    sheet = workbook.sheet_by_index(i)
    return sheet

def create_csv():
    path = "main_finding_results.csv"
    with open(path,'wb') as f:
        csv_write = csv.writer(f)
        csv_head = ["PMID","ID","main_finding"]
        csv_write.writerow(csv_head)

def write_csv(PMID,ID,main_finding):
    path  = "main_finding_results.csv"
    with open(path,'a+') as f:
        csv_write = csv.writer(f)
        data_row = [PMID,ID,main_finding]
        csv_write.writerow(data_row)

# create final output file
create_csv()

source_text_sheet=readworkbook("source_text.xls",0)
predicted_scores=pd.read_csv('predicted_scores.csv')
all_sentences_sheet=readworkbook("source_text.xls",1)
# load sentences and positive scores from last step csv
for source_num in range(1,source_text_sheet.nrows):
    PMID=source_text_sheet.cell(source_num,0).value
    # print PMID
    main_finding_ID_array=[]
    predicted_scores_ID_array=[]
    predicted_scores_array=[]
    # score>=0.9 should be mainfinding, score<0.1 should be negative sentence
    # when there is no sentence with score>=0.9 in one abstract, choose the sentence with highest scores among abstract as main finidng (score should larger than 0.1)
    for predicted_num in range(0,len(predicted_scores)):
        if predicted_scores["ID"][predicted_num].find(PMID)!=-1:
            if predicted_scores["predicted_score"][predicted_num]>=0.9:
                main_finding_ID_array.append(predicted_scores["ID"][predicted_num])
            elif predicted_scores["predicted_score"][predicted_num]>=0.1:
                predicted_scores_ID_array.append(predicted_scores["ID"][predicted_num])
                predicted_scores_array.append(predicted_scores["predicted_score"][predicted_num])
    if len(main_finding_ID_array)==0 and len(predicted_scores_ID_array)>0:
        main_finding_score=0.0
        main_finding_ID=''
        for predicted_score_num in range(0,len(predicted_scores_array)):
            if predicted_scores_array[predicted_score_num]>main_finding_score:
                main_finding_score=predicted_scores_array[predicted_score_num]
                main_finding_ID=predicted_scores_ID_array[predicted_score_num]
        main_finding_ID_array.append(main_finding_ID)

    # add results to final output file
    if len(main_finding_ID_array)==0:
        write_csv(PMID,"","")
    else:
        for main_finding_ID in main_finding_ID_array:
            for all_sentences_sheet_num in range(1,all_sentences_sheet.nrows):
                if main_finding_ID==all_sentences_sheet.cell(all_sentences_sheet_num,2).value:
                    write_csv(PMID,main_finding_ID,all_sentences_sheet.cell(all_sentences_sheet_num,3).value.encode('ascii','ignore'))



        






