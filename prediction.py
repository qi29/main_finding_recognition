import pandas as pd
import csv
from sklearn.svm import SVC
import sys
import os

learning_scores=sys.argv[1]
xmlfile=sys.argv[2]

trainingdata=pd.read_csv('416training_data.csv')
predictdata=pd.read_csv(learning_scores)

# training
trainingfeatures3=[]
trainingfeatures5=[]
# load 416 training data
for n in range(0,3455):
    score1=trainingdata["LogNormalPattern"][n]
    score2=trainingdata["NormalSimilarityFixed"][n]
    score3=trainingdata["Distribution2"][n]
    score4=trainingdata["BioSentStop"][n]
    score5=trainingdata["MaxNormalSimilarityFixed"][n]
    score6=0.00
    score6=trainingdata["MaxBioSentStop"][n]
    score7=trainingdata["Distribution5"][n]
    score8=trainingdata["Distribution4"][n]
    score9=trainingdata["NormalPattern"][n]
    score10=trainingdata["NormalWordFixed"][n]
    score11=trainingdata["Distribution1"][n]
    score12=trainingdata["Distribution3"][n]
    tag=trainingdata["mainfinding"][n]
    array3=[score1,score3,score7,score8,score9,score10,score11,score12,tag]
    array5=[score1,score2,score3,score4,score5,score6,score7,score8,score9,score10,score11,score12,tag]
    trainingfeatures3.append(array3)
    # set threthold for 3features or 5features
    if score6>0.15:
        trainingfeatures5.append(array5)
# 3features training
X3=[]
Y3=[]
for feature in trainingfeatures3:
    X3.append([feature[0],feature[1],feature[2],feature[3],feature[4],feature[5],feature[6],feature[7]])
    Y3.append([feature[8]])
clf = SVC(probability=True,kernel='linear')
clf3 = clf.fit(X3,Y3)
# 5features training
X5=[]
Y5=[]
for feature in trainingfeatures5:
    X5.append([feature[0],feature[1],feature[2],feature[3],feature[4],feature[5],feature[6],feature[7],feature[8],feature[9],feature[10],feature[11]])
    Y5.append([feature[12]])  
clf = SVC(probability=True,kernel='linear')
clf5 = clf.fit(X5,Y5)

# predicting 
testfeatures3=[]
testfeatures5=[]
# load new data need to be predicting
for n in range(0,len(predictdata)):
    score1=predictdata["LogNormalPattern"][n]
    score2=predictdata["NormalSimilarityFixed"][n]
    score3=predictdata["Distribution2"][n]
    score4=predictdata["BioSentStop"][n]
    score5=predictdata["MaxNormalSimilarityFixed"][n]
    score6=0.00
    score6=predictdata["MaxBioSentStop"][n]
    score7=predictdata["Distribution5"][n]
    score8=predictdata["Distribution4"][n]
    score9=predictdata["NormalPattern"][n]
    score10=predictdata["NormalWordFixed"][n]
    score11=predictdata["Distribution1"][n]
    score12=predictdata["Distribution3"][n]
    array3=[predictdata["ID"][n],score1,score3,score7,score8,score9,score10,score11,score12]
    array5=[predictdata["ID"][n],score1,score2,score3,score4,score5,score6,score7,score8,score9,score10,score11,score12]
    if score6>0.15:
        testfeatures5.append(array5)
    else:
        testfeatures3.append(array3)

test3pmcid=[]
test5pmcid=[]
testX3=[]
testX5=[]
# 3features box
for feature in testfeatures3:
    testX3.append([feature[1],feature[2],feature[3],feature[4],feature[5],feature[6],feature[7],feature[8]])
    test3pmcid.append(feature[0])
# 5features box
for feature in testfeatures5:
    testX5.append([feature[1],feature[2],feature[3],feature[4],feature[5],feature[6],feature[7],feature[8],feature[9],feature[10],feature[11],feature[12]])
    test5pmcid.append(feature[0])

def create_csv():
    path = xmlfile.replace(".xml","")+"_predicted_scores.csv"
    with open(path,'wb') as f:
        csv_write = csv.writer(f)
        csv_head = ["ID","predicted_score"]
        csv_write.writerow(csv_head)

def write_csv(ID,predicted_score):
    path  = xmlfile.replace(".xml","")+"_predicted_scores.csv"
    with open(path,'a+') as f:
        csv_write = csv.writer(f)
        data_row = [ID,predicted_score]
        csv_write.writerow(data_row)

create_csv()
# prediction and insert positive scores into csv
if len(testX3)>0:
    for num in range(0,len(clf3.predict_proba(testX3))):
        write_csv(test3pmcid[num],clf3.predict_proba(testX3)[num][1])
        # print str(test3pmcid[num])+','+str(clf3.predict_proba(testX3)[num][1])
if len(testX5)>0:
    for num in range(0,len(clf5.predict_proba(testX5))):
        write_csv(test5pmcid[num],clf5.predict_proba(testX5)[num][1])
        print ("training and predicting:"+str(test5pmcid[num]))
        # print str(test5pmcid[num])+','+str(clf5.predict_proba(testX5)[num][1])
prediction_scores=xmlfile.replace(".xml","")+"_predicted_scores.csv"

os.system("python main_finding_results.py %s %s" % (prediction_scores,xmlfile))