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
		if parent:
			parent.add_subBubble(self)
		self.subBubbleList=[]
		self.traversalList=[]
		self.siblingList=[]
		self.subBubbleLevels={}


	def set_bubbleID(self, nameList=None):
		if self.parent:
			nameList=self.parent.get_bubbleID().split('.')
			subBubbleLevels=self.parent.get_subBubbleLevels()
			if self.coreNumber in subBubbleLevels:
				levelCount=self.parent.get_subBubbleLevels()[self.coreNumber]
			else:
				levelCount=0
			nameList[len(nameList)-(int(self.coreNumber)-1)]=str(levelCount+1)
			self.parent.add_subBubbleLevel(self.coreNumber)
		self.bubbleID='.'.join(map(str, nameList))
		for subBubble in self.subBubbleList:
			subBubble.set_bubbleID()
		return None


	def get_bubbleID(self):
		return self.bubbleID


	def get_coreNumber(self):
		return self.coreNumber


	def get_parent(self):
		return self.parent


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
		if isinstance(segmentList, list) or isinstance(segmentList, set):
			self.segmentSet.update(set(segmentList))
		return None


	def get_traversalList(self):
		return self.traversalList


	def add_subBubble(self, subBubble):
		self.subBubbleList.append(subBubble)


	def get_siblingList(self):
		return self.siblingList


	def add_sibling(self, sibling):
		if len(set.intersection(self.segmentSet, sibling.get_segmentSet()))>0:
			self.siblingList.append(sibling)
#			for subBubble in self.subBubbleList:
#				subBubble.add_sibling(sibling)
		return None


	def is_related_bubble(self, bubbleObject):
		related=False
		bubbleIDList=bubbleObject.get_bubbleID().split('.')
		ownBubbleIDList=self.bubbleID.split('.')
		for i in range(len(bubbleIDList)):
			if bubbleIDList[i]!="0" or ownBubbleIDList[i]!="0":
				if bubbleIDList[i]==ownBubbleIDList[i]:
					related=True
			break
		return related


	def get_subBubbleLevels(self):
		return self.subBubbleLevels


	def add_subBubbleLevel(self, bubbleLevel):
		if bubbleLevel in self.subBubbleLevels:
			self.subBubbleLevels[bubbleLevel]+=1
		else:
			self.subBubbleLevels[bubbleLevel]=1
		return None




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
