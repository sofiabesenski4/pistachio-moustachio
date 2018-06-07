#result_analysis.py
"""
idea:
so we want to look through a file directory called Test_Results, and find out how many of what type of matches have been made
from the processed samples

-start a tally for each type of match
-navigate to folder
-for every file in directory:
	-parse through to find if a match!= F
		-record the sample number and match in the csv
		-
"""

import os
import csv

