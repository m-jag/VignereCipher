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

file1name = input("Enter file 1: ")
file2name = input("Enter file 2: ")


def getFreq(filename):
  data = pd.read_csv(filename, sep='\n', header=None, names=['lines'])
  data.lines = data.lines.apply(lambda x: re.findall(r"(?P<letter>[a-zA-Z])", x.lower()))
  letters = np.hstack(data.lines.apply(lambda x: np.array(x)))
  return np.unique(letters, return_counts=True);

file1_freq = getFreq(file1name)
file2_freq = getFreq(file2name)

file1_prob = np.true_divide(file1_freq[1], sum(file1_freq[1]))
file2_prob = np.true_divide(file2_freq[1], sum(file2_freq[1]))

# Text Output
if (verbose):
	print("Text Output")
	print("Counts file1: %i file2: %i" % (sum(file1_freq[1]), sum(file2_freq[1])))
	print('file1 freq')
	print(file1_freq)
	print('file2 freq')
	print(file2_freq)
	print('file1 prob')
	print(file1_prob)
	print('file2 prob')
	print(file2_prob)
	print("")

# Probability Table
probabilities = pd.DataFrame(data=np.vstack((file1_prob, file2_prob)), columns=file1_freq[0], index=['file1', 'file2'])
print("Probability Table")
print(probabilities.T)


# Graphs
graph_colors = [
    '#0000FF',
    '#FF0000'
]

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

ax1.set_title("Letter Frequency")
ax1.bar(np.arange(26), file1_freq[1], width=0.5, color=graph_colors[0])
ax1.bar(np.arange(26)+0.5, file2_freq[1], width=0.5, color=graph_colors[1])
ax1.set_xticks(np.arange(26))
ax1.set_xticklabels(file1_freq[0])
ax1.set_ylabel("Frequency")

ax2.set_title("Letter Probabilities")
ax2.bar(np.arange(26), file1_prob, width=0.5, color=graph_colors[0])
ax2.bar(np.arange(26)+0.5, file2_prob, width=0.5, color=graph_colors[1])
ax2.set_xticks(np.arange(26))
ax2.set_xticklabels(file1_freq[0])
ax2.set_ylabel("Probabilities")
plt.show()