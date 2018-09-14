#!/usr/bin/env python3
###############################################
# Name: FrequencyAnalysisCode.py
# Author: Matt Jagodzinski
#
# Description: Calculates letter frequencies
# and probabilities for 2 text files
#
#
# Requirements:
# Python 3 (for Python2 input --> raw_input on lines 21 && 22)
# pip3 install numpy
# pip3 install pandas
# pip3 install matplotlib
###############################################

import sys
import numpy as np
import pandas as pd
import re
import time
import matplotlib.pyplot as plt

verbose=False

# Counts all of the unique characters in a file (converts to lowercase)
def getFreq(filename):
  data = pd.read_csv(filename, sep='\n', header=None, names=['lines'])
  data.lines = data.lines.apply(lambda x: re.findall(r"(?P<letter>[a-zA-Z])", x.lower()))
  letters = np.hstack(data.lines.apply(lambda x: np.array(x)))
  return np.unique(letters, return_counts=True);

# Adds 0's for every frequency letter not in the text
def padFrequencies(ltrs, stats):
	values = np.zeros((1, 26), dtype=np.uint64)
	def setVal(pos):
		values[0][ord(ltrs[pos]) - ord('a')] = stats[pos]
	np.frompyfunc(setVal, 1, 1)(np.arange(len(ltrs)))
	return values[0]

def main(argv):
	alphabet = np.frompyfunc(lambda offset: chr(ord('a') + offset), 1, 1)(np.arange(26))

	# Get filenames
	file1name = input("Enter file 1: ")
	file2name = input("Enter file 2: ")

	# Count characters
	file1_freq = getFreq(file1name)
	file2_freq = getFreq(file2name)

	# Add values that weren't in file as 0
	file1_freq = (alphabet, padFrequencies(file1_freq[0], file1_freq[1]))
	file2_freq = (alphabet, padFrequencies(file2_freq[0], file2_freq[1]))

	# Calculate probabilities
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

	# Create 2 plots in window
	fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

	# Plot letter frequency
	ax1.set_title("Letter Frequency")
	ax1.bar(np.arange(26), file1_freq[1], width=0.5, color=graph_colors[0])
	ax1.bar(np.arange(26)+0.5, file2_freq[1], width=0.5, color=graph_colors[1])
	ax1.set_xticks(np.arange(26))
	ax1.set_xticklabels(alphabet)
	ax1.set_ylabel("Frequency")

	# Plot letter probability
	ax2.set_title("Letter Probabilities")
	ax2.bar(np.arange(26), file1_prob, width=0.5, color=graph_colors[0])
	ax2.bar(np.arange(26)+0.5, file2_prob, width=0.5, color=graph_colors[1])
	ax2.set_xticks(np.arange(26))
	ax2.set_xticklabels(alphabet)
	ax2.set_ylabel("Probabilities")
	plt.show()


if __name__ == "__main__":
	main(sys.argv[1:])
