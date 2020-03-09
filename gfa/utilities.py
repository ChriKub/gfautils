#!/usr/bin/env python


def is_intersect(ref, query):
	if ref[0]>=query[0] and ref[0]<=query[1]:
		return True
	elif ref[1]>=query[0] and ref[1]<=query[1]:
		return True
	elif ref[0]<=query[0] and ref[1]>=query[1]:
		return True
	else:
		return False


def get_colorList():
	colorList=['red', 'green', 'blue', 'yellow', 'violett']
	return colorList


def open_file(inpath):
        file=open(inpath, 'r')
        input=file.read()
        file.close()
        return input

def write_file(outpath, output):
        file=open(outpath, 'w')
        file.write(output)
        file.close()
        return None


def append_line(filepath, line):
	file=open(filepath, 'a')
	file.write(line)
	file.close()
	return None


def reverse_complement(sequence):
	reverseComplement=''
	for i in range(len(sequence)-1,-1,-1):
		if sequence[i].upper()=='N':
			reverseComplement+='N'
		elif sequence[i].upper()=='A':
			reverseComplement+='T'
		elif sequence[i].upper()=='T':
			reverseComplement+='A'
		elif sequence[i].upper()=='C':
			reverseComplement+='G'
		elif sequence[i].upper()=='G':
			reverseComplement+='C'
	return reverseComplement
