Require Python 2; Java JRE (Runtime Environment) 1.8
Required package: xlrd (1.2.0); xlwt (1.3.0); beautifulsoup4 (4.6.3); nltk (3.4); sent2vec (0.0.0); scikit-learn (0.20.2);pandas (0.24.0)
Third part packages: 1) Download Stanford Parser (Version 3.9.2), and put it inside the project folder 2)Downloade BioSentVec model: BioSentVec_PubMed_MIMICIII-bigram_d700.bin, and put it inside the project folder
implement from _main.py, it will automatically implement all others *.py in order
first input file is pubmed_result.xml downloaded from pubmed, and the Publication Type of articles in the .xml files should be Case Reports; final output file is main_finding_results.csv containing PMID, ID and main finding sentences.
(xml_to_excel.py extracts PMID, titles and abstracts from .xml file, and output is source_text.xls; sentences_scoring_raw.py gives the raw scores to all sentences, and output is raw_scores.csv; normalization.py normalizes the raw scores, and output is learning_scores.csv; prediction.py gives predicted scores to all sentences, and output is predicted_scores.csv; main_finding_results.py outputs all main finding sentences in main_finding_results.csv)
supplementary files: stoplist1392.txt; word.xlsx (word based features); Pattern.xlsx (pattern based features); 416training_data.csv; 

