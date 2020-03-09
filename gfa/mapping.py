#!/usr/bin/env python

class gam():

	def __init__(self, bubbleLine):
		self.start=bubbleLine.split('\t')[0]
		self.stop=bubbleLine.split('\t')[1]
		self.type=bubbleLine.split('\t')[3]
		self.variantList=bubbleLine.split('\t')[2].split(',')[1:-1]


class pack():

	def __init__(self, packList):
		self.nodeDict=self.process_pack(packList[1:])
	

	def process_pack(self, packList):
		nodeDict={}
		packList=[]
		nodeid=packList[0].split('\t')[1]
		for line in packList:
			if line.split('\t')[1]!=nodeid:
				nodeDict[nodeid]=packList
				nodeid=line.split('\t')[1]
				packList=[line.split('\t')]
			else:
				packList.append(line.split('\t'))
		return nodeDict


	def get_nodeDict(self):
		return self.nodeDict


class vectorize():

	def __init__(self, vectorList):
		vectorList=vectorList.split('\n')
		self.nodeList=vectorList[0].split('\t')
		self.readDict=self.build_readList(vectorList[1:], self.nodeList)
		return None


	def build_readList(self, vectorList, nodeList):
		readDict={}
		for line in vectorList:
			readList=[]
			for i in range(len(line.split('\t'))):
				if line.split('\t')[i]=='1':
					readList.append(nodeList[i].split('.')[1])
			readDict[line.split('\t')[0]]=readList
		return readDict


	def get_readDict(self):
		return self.readDict
