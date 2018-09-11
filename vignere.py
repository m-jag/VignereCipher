###############################################
# Name: FrequencyAnalysisCode.py
# Author: Matt Jagodzinski
# 
# Description: Calculates letter frequencies 
# and probabilities for 2 text files
#
# Requirements:
# Python 3 (for Python2 input --> raw_input on lines 21 && 22)
# pip install matplotlib
###############################################


import numpy as np
import pandas as pd
import re
import time
import matplotlib.pyplot as plt

verbose=False

fileIn = "in.txt" #input("Enter file 1: ")
key = np.array("abc".split()) #input("Enter key: ")
#fileOut = "out.txt" #input("Enter file 1: ")


def getKeyValue(c):
	return ord(c.lower()) - ord('a')

calcKeyValue = np.frompyfunc(getKeyValue, 1, 1)
#key_values = calcKeyValue(key)


print(key.size)

#def encrypt(filename):
#	data = pd.read_csv(filename, sep='\n', header=None, names=['lines'])
#	data.lines = data.lines.apply(lambda x: re.findall(r"(?P<letter>[a-zA-Z])", x.lower()))
#	letters = np.hstack(data.lines.apply(lambda x: np.array(x)))
#	def enc(ltr):
#		letters[pos:letters.size():len(key)] += ord(ltr) - ord('a')
#	enc_func = np.frompyfunc(enc, 1, 1)
#	enc_func(letters)
#	return letters

#print(encrypt(file1name))