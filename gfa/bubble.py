#!/usr/bin/env python


class Bubble():

	def __init__(self, bubbleID, leftAnchor, rightAnchor, segmentList, bubbleType, coreNumber, parent=None):
		self.bubbleID=bubbleID
		self.leftAnchor=leftAnchor
		leftAnchor.add_leftAnchor(self)
		self.rightAnchor=rightAnchor
		rightAnchor.add_rightAnchor(self)
		self.segmentSet=set(segmentList)
		self.pathDict={}
		self.coreNumber=coreNumber
		self.parent=parent
		self.subBubbleList=[]


	def get_bubbleID(self):
		return self.bubbleID


	def get_Anchors(self):
		return self.leftAnchor, self.rightAnchor


	def get_leftAnchor(self):
		return self.leftAnchor


	def get_rightAnchor(self):
		return self.rightAnchor


	def get_segmentSet(self):
		return self.segmentSet


	def add_subBubble(self, bubbleObject):
		self.subBubbleList.add(bubbleObject)


	def get_subBubbles(self):
		return self.subBubbleList



class Traversal():

	def __init__(self, pathList, segmentList, orientation):
		self.pathDict={}
		self.traversalLength=self.calculate_traversalLength(segmentList)
		self.segmentList=segmentList
		self.orientation=orientation
		self.fill_pathDict(pathList)


	def calculate_traversalLength(self, segmentList):
		traversalLength=0
		if segmentList[0]!='InDel':
			for segmentObject in segmentList:
				traversalLength+=segmentObject.get_sequence_length()
		return traversalLength


	def get_traversalLength(self):
		return self.traversalLength


	def fill_pathDict(self, pathList):
		for path in pathList:
			if path[0] in self.pathDict:
				self.pathDict[path[0]].append(path[1])
			else:
				self.pathDict[path[0]]=[path[1]]
		return None


	def get_pathList(self):
		return self.pathList


	def get_traversalNumber(self):
		traversalSet=set([])
		for path in self.pathDict.keys():
			traversalSet.add(path.split('_')[0])
		return len(traversalSet)


	def is_traversed(self, src):
		traversed=False
		for path in self.pathList:
			if path==src:
				traversed=True
		return traversed


	def get_segmentList(self):
		return self.segmentList


	def get_orientation(self):
		return self.orientation
