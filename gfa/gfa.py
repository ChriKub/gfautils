#!/usr/bin/env python

from .link import Link
from .path import Path
from .bubble import Bubble
from .segment import Segment
from .mapping import pack
from .mapping import vectorize

class gfaHandler():

	def __init__(self, gfaFile):
		self.segmentDict={}
		self.pathDict={}
		self.linkList=[]
		self.bubbleDict={}
		self.bubbleList=[]
		self.process_GFA(gfaFile)


	def process_GFA(self, gfaFile):
		linkList=[]
		for line in gfaFile.split('\n'):
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


	def get_bubbleDict(self):
		return self.bubbleDict


	def get_bubbleList(self):
		return self.bubbleList


	def add_bubble(self, leftAnchor, coreNumber, parent=None):
		bubble=Bubble(leftAnchor, str(coreNumber), parent)
		self.bubbleList.append(bubble)
		if str(coreNumber) in self.bubbleDict:
			self.bubbleDict[str(coreNumber)].append(bubble)
		else:
			self.bubbleDict[str(coreNumber)]=[bubble]
		return bubble


	def has_bubble(self, segmentList, leftAnchorNode, rightAnchorNode):
		hasBubble=False
		for bubble in self.bubbleList:
			if set(segmentList).issubset(bubble.get_segmentSet()):
				if hasBubble:
					if len(hasBubble.get_segmentSet())>len(bubble.get_segmentSet()):
						hasBubble=bubble
				else:
					hasBubble=bubble
			elif leftAnchorNode==bubble.get_leftAnchor() and rightAnchorNode==bubble.get_rightAnchor():
				hasBubble=bubble
				break
		return hasBubble


	def build_gfa(self, header=None):
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


	def rebuild_gfa(self, header=None):
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
