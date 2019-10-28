# Copyright 2019, University of Illinois at Chicago
# This file is part of the main_finding_recognition project.
# See the ReadMe.txt for licensing information.

import os
import sys
# implemnet all *.py in below order
inputfile = str(sys.argv[1])
# print inputfile
os.system("python xml_to_excel.py %s" % (inputfile))
# os.system("python sentences_scoring_raw.py")
# os.system("python normalization.py")
# os.system("python prediction.py")
# os.system("python main_finding_results.py")
