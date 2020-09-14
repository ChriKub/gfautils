#!/usr/bin/env python


class Bubble():

	def __init__(self, bubbleID, leftAnchor, rightAnchor, segmentList, coreNumber, parent=None):
		self.bubbleID=bubbleID
		self.leftAnchor=leftAnchor
		if leftAnchor:
			leftAnchor.add_leftAnchor(self)
		self.rightAnchor=rightAnchor
		if rightAnchor:
			rightAnchor.add_rightAnchor(self)
		self.segmentSet=set(segmentList)
		self.pathDict={}
		self.coreNumber=coreNumber
		self.parent=parent
		self.subBubbleList=[]
		self.traversalList=[]


	def get_bubbleID(self):
		return self.bubbleID


	def get_coreNumber(self):
		return self.coreNumber


	def get_Anchors(self):
		return self.leftAnchor, self.rightAnchor


	def get_leftAnchor(self):
		return self.leftAnchor


	def get_rightAnchor(self):
		return self.rightAnchor


	def get_segmentSet(self):
		return self.segmentSet


	def find_subBubble(self, bubbleID, leftAnchor, rightAnchor, traversalSet, coreNumber):
		subBubbleObject=None
		for subBubble in self.subBubbleList:
			if subBubble.get_leftAnchor()==leftAnchor and subBubble.get_rightAnchor()==rightAnchor:
				subBubbleObject=subBubble
			elif set(traversalSet).issubset(subBubble.get_segmentSet()):
				subBubbleObject=subBubble.find_subBubble(bubbleID, leftAnchor, rightAnchor, traversalSet, coreNumber)
		return subBubbleObject


	def get_subBubbles(self):
		return self.subBubbleList


	def add_segments(self, newSegments):
		self.segmentSet.update(set(newSegments))


	def add_traversal(self, pathName, segmentList, leftPosition, rightPosition):
		oldTraversal=None
		for traversal in self.traversalList:
			if segmentList==traversal.get_segmentList():
				traversal.add_path([pathName, leftPosition, rightPosition])
				oldTraversal=traversal
		if not oldTraversal:
			self.traversalList.append(Traversal(segmentList, [pathName, leftPosition, rightPosition]))
		self.segmentSet.update(set(segmentList))
		return None


	def get_traversalList(self):
		return self.traversalList


	def add_subBubble(self, subBubble):
		self.subBubbleList.append(subBubble)


class Traversal():

	def __init__(self, segmentList, path):
		self.pathList=[]
		self.add_path(path)
		self.segmentList=segmentList


	def add_path(self, path):
		self.pathList.append(path)


	def get_pathList(self):
		return self.pathList


	def get_segmentList(self):
		return self.segmentList
