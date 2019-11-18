Copyright 2019, University of Illinois at Chicago
 
This file is part of the main_finding_recognition project.
 
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 
    http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
===

Require Python 2; Java JRE (Runtime Environment) 1.8; Linux System

Required package: 
                xlrd (1.2.0); (command)pip install xlrd==1.2.0
                xlwt (1.3.0); (command)pip install xlwt==1.3.0
                beautifulsoup4 (4.8.0); (command)pip install bs4
                nltk (3.4); (command)pip install nltk==3.4
                punkt:  >>> import nltk
                        >>> nltk.download('punkt')
                fastText(0.9.1); (command)pip install fastText==0.9.1
                sent2vec; unzip sent2vec-master.zip; run a make command; go into sent2vec-master folder run (command) pip install .
                cython is required for sent2vec; (command) pip install Cython
                scikit-learn (0.20.4);(command)pip install https://pypi.org/project/scikit-learn/0.20.4
                pandas (0.24.0); (command)pip install pandas==0.24.0
                Stanford Parser (Version 3.9.2): 1) Download Stanford Parser (Version 3.9.2) from https://nlp.stanford.edu/software/lex-parser.shtml#Download and put it inside the project folder 
                Download BioSentVec model: BioSentVec_PubMed_MIMICIII-bigram_d700.bin from https://github.com/ncbi-nlp/BioSentVec and put it inside the project folder
implement from _main.py: python _main.py (your file name).xml, it will automatically implement all others *.py in order
first input file is (your file name).xml downloaded from pubmed, and the Publication Type of articles in the .xml files should be Case Reports; final output file is main_finding_results.csv containing PMID, ID and main finding sentences.
(xml_to_excel.py extracts PMID, titles and abstracts from .xml file, and output is (your file name)_source_text.xls; sentences_scoring_raw.py gives the raw scores to all sentences, and output is (your file name)_raw_scores.csv; normalization.py normalizes the raw scores, and output is (your file name)_learning_scores.csv; prediction.py gives predicted scores to all sentences, and output is (your file name)_predicted_scores.csv; main_finding_results.py outputs all main finding sentences in (your file name)_main_finding_results.csv)
supplementary files: stoplist1392.txt; word.xlsx (word based features); Pattern.xlsx (pattern based features); 416training_data.csv; 
