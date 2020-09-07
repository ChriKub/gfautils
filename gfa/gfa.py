#!/usr/bin/env python

from .link import Link
from .path import Path
from .bubble import Bubble
from .segment import Segment
from .mapping import pack
from .mapping import vectorize

class gfaHandler():

	def __init__(self, revealFile):
		self.segmentDict={}
		self.pathDict={}
		self.linkList=[]
		self.bubbleList=[]
		self.process_Reveal(revealFile)


	def process_Reveal(self, revealFile):
		linkList=[]
		for line in revealFile.split('\n'):
			if line:
				if line[0]=='S':
					self.segmentDict[line.split('\t')[1]]=Segment(line)
				elif line[0]=='L':
					linkList.append(line)
				elif line[0]=='P':
					self.pathDict[line.split('\t')[1].split(' ')[0]]=Path(line.split('\t')[1].split(' ')[0], line.split('\t')[2], line.split('\t')[3])
		if self.pathDict:
			for pathId in self.pathDict:
				self.process_path(self.pathDict[pathId])
		if linkList:
			self.process_linkList(linkList)
		return None


	def process_linkList(self, linkList):
		for link in linkList:
			splitLink=link.split('\t')
			newLink=Link(self.segmentDict[splitLink[1]], splitLink[2], self.segmentDict[splitLink[3]], splitLink[4], splitLink[5])
			self.linkList.append(newLink)
			self.segmentDict[splitLink[1]].add_outgoingLink(newLink)
			self.segmentDict[splitLink[3]].add_incomingLink(newLink)
		return None


	def process_path(self, pathObject):
		currentPosition=0
		for node in pathObject.get_pathList():
			self.segmentDict[node[:-1]].fill_pathDict(pathObject.get_id(), currentPosition)
			pathObject.fill_positionDict(currentPosition, self.segmentDict[node[:-1]])
			currentPosition+=self.segmentDict[node[:-1]].get_sequence_length()
		return None


	def add_segment(self, segmentLine):
		self.segmentDict[segmentLine.split('\t')[1]]=Segment(segmentLine)
		return self.segmentDict[segmentLine.split('\t')[1]]


	def get_segments(self):
			return self.segmentDict.keys()


	def get_segment(self, segmentID):
		return self.segmentDict[segmentID]


	def get_segmentDict(self):
		return self.segmentDict


	def get_paths(self):
		return self.pathDict.keys()


	def get_path(self, pathID):
		return self.pathDict[pathID]


	def get_pathDict(self):
		return self.pathDict


	def change_pathList(self, pathID, pathList):
		self.pathDict[pathID].change_pathList(pathList)
		return None


	def get_linkList(self):
		linkList=[]
		for segment in self.segmentDict:
			linkList.extend(self.segmentDict[segment].build_links())
		return linkList


	def add_path(self, leftSegment, leftOrientation, rightSegment, rightOrientation, CIGAR):
			newLink=Link(leftSegment, leftOrientation, rightSegment, rightOrientation, CIGAR)
			self.linkList.append(newLink)
			leftSegment.add_outgoingLink(newLink)
			rightSegment.add_incomingLink(newLink)


	def get_segmentList(self):
		segmentList=[]
		for segment in self.segmentDict:
			segmentList.append('\t'.join(['S', segment, self.segmentDict[segment].get_sequence()]))
		return segmentList


	def get_pathList(self):
		pathList=[]
		for path in self.pathDict:
			pathList.append('\t'.join(self.pathDict[path].build_path()))
		return pathList


	def get_bubbleList(self):
		return self.bubbleList


	def add_bubble(self, leftAnchor, rightAnchor, segmentList, bubbleType):
		self.bubbleList.append(Bubble(leftAnchor, rightAnchor, segmentList, bubbleType))
		return None


	def add_pack(self, pack):
		packDict=pack.get_nodeDict()
		for segment in packDict.keys():
			self.segmentDict[segment].add_pack(packDict[segment])
		return None


	def add_vectorize(self, vectorize):
		readDict=vectorize.get_readDict()
		for read in readDict.keys():
			for segment in readDict[read]:
				self.segmentDict[segment].add_read(read)
		return None


	def build_gfa(self, header=False):
		gfa=[]
		if header:
			gfa=['H\tVN:Z:1.0'+header]
		else:
			gfa=['H\tVN:Z:1.0']
		gfa.extend(self.get_segmentList())
		gfa.extend(self.get_linkList())
		if self.pathDict:
			gfa.extend(self.get_pathList())
		return gfa


	def rebuild_gfa(self, header=False):
		gfa=[]
		segmentSet=set([])
		linkSet=set([])
		pathList=self.get_pathList()
		for pathName in self.get_pathDict():
			pathList=self.get_path(pathName).get_pathList()
			for i in range(len(pathList)):
				segmentSet.add('\t'.join(['S', pathList[i][:-1], self.segmentDict[pathList[i][:-1]].get_sequence()]))
				try:
					linkSet.add('\t'.join(['L', pathList[i][:-1], pathList[i][-1], pathList[i+1][:-1], pathList[i+1][-1], '0M']))
				except:
					pass
		if header:
			gfa=['H\tVN:Z:1.0'+header]
		else:
			gfa=['H\tVN:Z:1.0']
		gfa.extend(list(segmentSet))
		gfa.extend(list(linkSet))
		gfa.extend(self.get_pathList())
		return gfa


	def unchop(self):
		unchopList=[[]]
		for path in self.get_pathList():
			pathID=path.split('\t')[1]
			segmentList=path.split('\t')[2].split(',')
			unchop=True
			for i in range(len(segmentList)):
				segmentID=segmentList[i][:-1]
				if i==len(segmentList)-1:
					try:
						if segmentList[-2][:-1]==unchopList[-1][-1]:
							unchopList[-1].append(segmentID)
							unchopList.append([])
					except:
						pass
				elif len(self.segmentDict[segmentID].get_successors())==1 and segmentID!=self.segmentDict[segmentID].get_successors().keys()[0]:
					if len(self.segmentDict[segmentID].get_successors()[self.segmentDict[segmentID].get_successors().keys()[0]])==1:
						if self.segmentDict[segmentID].get_pathDict().keys()==self.segmentDict[self.segmentDict[segmentID].get_successors().keys()[0]].get_pathDict().keys():
							unchopList[-1].append(segmentID)
						else:
							try:
								if segmentList[i-1][:-1]==unchopList[-1][-1]:
									unchopList[-1].append(segmentID)
							except:
								pass 
							unchopList.append([])
					else:
						try:
							if segmentList[i-1][:-1]==unchopList[-1][-1]:
								unchopList[-1].append(segmentID)
						except:
							pass
						unchopList.append([])
				else:
					try:
						if segmentList[i-1][:-1]==unchopList[-1][-1]:
							unchopList[-1].append(segmentID)
					except:
						pass
					unchopList.append([])
		cleanList=[]
		for newNode in unchopList:
			if newNode:
				cleanList.append(','.join(newNode))
		unchopList=list(set(cleanList))
		if unchopList:
			self.rebuild_segmentDict(unchopList)
		return None


	def rebuild_segmentDict(self, unchopList):
		for newNode in unchopList:
			splitNodes=newNode.split(',')
			successorDict={}
			sequence=self.segmentDict[splitNodes[0]].get_sequence()
			for segment in splitNodes[1:]:
				sequence+=self.segmentDict[segment].get_sequence()
				successorDict=self.segmentDict[segment].get_successors()
#				del self.segmentDict[segment]
			self.segmentDict[splitNodes[0]].set_sequence(sequence)
			self.segmentDict[splitNodes[0]].set_successors(successorDict)
		self.clean_segmentDict(unchopList)
		self.rebuild_pathDict()
		return None


	def clean_segmentDict(self, unchopList):
		for newNode in unchopList:
			splitNodes=newNode.split(',')
			for segment in splitNodes[1:]:
				try:
					del self.segmentDict[segment]
				except:
					pass
		return None


	def rebuild_pathDict(self):
		for path in self.pathDict:
			for place in sorted(self.pathDict[path].get_pathDict().keys()):
				try:
					self.segmentDict[self.pathDict[path].get_pathDict()[place][0].get_id()]
				except:
					del self.pathDict[path].get_pathDict()[place]
		return None
