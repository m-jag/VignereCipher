#!/usr/bin/env python3
###############################################
# Name: vignere.py
# Author: Matt Jagodzinski
#
# Description: Encrypts input file using vignere
# cipher with key passed as input and stores the
# encrypted file in the output file
#
# Example Use:
# python3 vignere.py
# Enter input file : in.txt
# Enter output file : out.txt
# Enter key: a
#
# Requirements:
# Python 3 (for Python2 input --> raw_input on lines 21 && 22)
# pip3 install numpy
# pip3 install pandas
# pip3 install matplotlib
###############################################

import sys, getopt, math
import numpy as np
import pandas as pd
import re
import time
import mmap
import matplotlib.pyplot as plt
from enum import Enum

verbose=False

# Grabs letters from a file
def lettersFromFile(filename):
	letters = np.empty((0))
	get_letters = re.compile(b"([a-zA-Z])")

	with open(filename, "r+b") as f:
		mm_pt = mmap.mmap(f.fileno(), 0)
		letters = np.array(get_letters.findall(mm_pt[:]))
		mm_pt.close()
		f.close()

	return letters

def writeOutput(output, filename):
	# Write file to output
	with open(filename, "w") as f:
		f.write(output)
		f.close()

# Functions to convert char/ascii to and from integer
# representation 0-25 where a = 0, b = 1, ..., z = 25
def getLetterValue(c):
	return ord(c.lower()) - ord('a')
def getLetter(v):
	return chr(v + ord('a'))

class Mode(Enum):
	ENCRYPT=0
	DECRYPT=1

def vignere(text, key_values, mode=Mode.ENCRYPT):
	# Convert char/ascii to integer representation 0-25 where a = 0, b = 1, ..., z = 25
	text = np.frompyfunc(getLetterValue, 1, 1)(text)

	if (mode == Mode.ENCRYPT):
		# Define a universal function fro encryption
		def encrypt(key_pos):
			text[key_pos::len(key_values)] = (text[key_pos::len(key_values)] + key_values[key_pos]) % 26
		encrypt = np.frompyfunc(encrypt, 1, 1)

		encrypt(np.arange(len(key_values)))
	elif (mode == Mode.DECRYPT):
		# Define a universal function for decryption
		def decrypt(key_pos):
			text[key_pos::len(key_values)] = (text[key_pos::len(key_values)] - key_values[key_pos]) % 26
		decrypt = np.frompyfunc(decrypt, 1, 1)

		decrypt(np.arange(len(key_values)))

	return ''.join(np.frompyfunc(getLetter, 1, 1)(text))

def main(argv):
	# Universal functions
	# Converts numpy array of chars or strings to lower case
	to_lower = np.frompyfunc(lambda x: x.lower(), 1, 1)
	# Convert char/ascii to integer representation 0-25 where a = 0, b = 1, ..., z = 25
	calcLetterValue = np.frompyfunc(getLetterValue, 1, 1)
	# Convert integer representation to char/ascii
	calcLetter = np.frompyfunc(getLetter, 1, 1)

	fileIn = input("Enter input file : ")
	fileOut = input("Enter output file : ")
	key = to_lower(np.array(re.findall("([a-zA-Z])", input("Enter key: "))))

	# Calculate the key values 0-25 where a = 0, b = 1, ..., z = 25
	key_values = calcLetterValue(key)
	# store all the letters as lowercase in numpy array message
	plaintext = to_lower(lettersFromFile(fileIn))

	if (verbose):
		print('plaintext')
		print(''.join(np.frompyfunc(lambda x: chr(ord(x)), 1, 1)(plaintext)))

	plaintext = vignere(plaintext, key_values)

	if (verbose):
		print('ciphertext')
		print(plaintext)

	writeOutput(plaintext, fileOut)

	# Notify user of encryption being done
	print('Encrypted %s to %s' % (fileIn, fileOut))


if __name__ == "__main__":
	main(sys.argv[1:])
