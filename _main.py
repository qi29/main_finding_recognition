import os
# implemnet all *.py in below order
os.system("python xml_to_excel.py")
os.system("python sentences_scoring_raw.py")
os.system("python normalization.py")
os.system("python prediction.py")
os.system("python main_finding_results.py")