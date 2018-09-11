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


import numpy as np
import pandas as pd
import re
import time
import mmap
import matplotlib.pyplot as plt

verbose=False

get_letters = re.compile(b"([a-zA-Z])")
to_lower = np.frompyfunc(lambda x: x.lower(), 1, 1)

fileIn = input("Enter input file : ")
fileOut = input("Enter output file : ")
key = to_lower(np.array(re.findall("([a-zA-Z])", input("Enter key: "))))
#fileOut = "out.txt" #input("Enter file 1: ")



# Functions to convert char/ascii to and from integer
# representation 0-25 where a = 0, b = 1, ..., z = 25 
def getLetterValue(c):
	return ord(c.lower()) - ord('a')
def getLetter(v):
	return chr(v + ord('a'))

calcLetterValue = np.frompyfunc(getLetterValue, 1, 1)
calcLetter = np.frompyfunc(getLetter, 1, 1)

# Calculate the key values 0-25 where a = 0, b = 1, ..., z = 25 
key_values = calcLetterValue(key)

#open plaintext
with open(fileIn, "r+b") as f:
	mm_pt = mmap.mmap(f.fileno(), 0)
	# store all the letters as lowercase in numpy array message
	message = to_lower(np.array(get_letters.findall(mm_pt[:])))

	if (verbose):
		print('plaintext')
		print(''.join(np.frompyfunc(lambda x: chr(ord(x)), 1, 1)(message)))
	
	# Define a universal function for encryption
	def encrypt(key_pos):
		message[key_pos::len(key_values)] = (message[key_pos::len(key_values)] + key_values[key_pos]) % 26
	encrypt = np.frompyfunc(encrypt, 1, 1)

	# Define a universal function for decryption
	def decrypt(key_pos):
		message[key_pos::len(key_values)] = (message[key_pos::len(key_values)] - key_values[key_pos]) % 26
	decrypt = np.frompyfunc(decrypt, 1, 1)

	# convert char/ascii to integer representation 0-25 where a = 0, b = 1, ..., z = 25 
	message = calcLetterValue(message)

	# Encrypt the message here
	# note: encrypted/decrypted message is currently being stored as the same variable (message)
	encrypt(np.arange(len(key_values)))
	# Decrypt the message here
	#decrypt(np.arange(len(key_values)))

	# Convert from integer representation to char/ascii and join array values
	message = ''.join(calcLetter(message))

	if (verbose):
		print('ciphertext')
		print(message)
	
	mm_pt.close()
	f.close()
del mm_pt

# Write file to output
with open(fileOut, "w") as f:
	f.write(message)
	f.close()

# Notify user of encryption being done
print('Encrypted %s to %s' % (fileIn, fileOut))