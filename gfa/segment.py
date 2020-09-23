#!/usr/bin/env python

class Segment():

	def __init__(self, segmentLine):
		self.id=segmentLine.split('\t')[1]
		self.sequence=segmentLine.split('\t')[2]
		self.pathDict={}
		self.incomingLinks=[]
		self.outgoingLinks=[]
		self.leftAnchor=[]
		self.rightAnchor=[]
		self.bubbleList=[]
		return None


	def get_id(self):
		return self.id


	def get_sequence(self):
		return self.sequence


	def get_sequence_length(self):
		return len(self.sequence)


	def fill_pathDict(self, pathID, position):
		if pathID in self.pathDict:
			self.pathDict[pathID].append(position)
		else:
			self.pathDict[pathID]=[position]
		return None


	def get_pathDict(self):
		return self.pathDict


	def get_ecotypeList(self):
		ecotypeList=set([])
		for path in self.pathList:
			ecotypeList.add(path.split('_')[0])
		return list(ecotypeList)


	def get_path_positions(self, pathID):
		return self.pathDict[pathID]


	def remove_from_pathDict(self, pathID, pathPosition):
		positionList=[]
		for position in self.pathDict[pathID]:
			if position!=pathPosition:
				positionList.append(position)
		if len(positionList)>=1:
			self.pathDict[pathID]=positionList
		else:
			del self.pathDict[pathID]
		return None


	def get_predecessors(self):
		return self.incomingLinks


	def get_predecessorNode(self, path, pathPosition):
		previousNode=None
		previousNodeStart=0
		for predecessor in self.incomingLinks:
			if path in predecessor.get_leftSegment().get_pathDict():
				for position in predecessor.get_leftSegment().get_path_positions(path):
					if startPosition==position+predecessor.get_leftSegment().get_sequence_length():
						previousNode=predecessor.get_leftSegment()
						previousNodeStart=position
		return previousNode, previousNodeStart


	def get_successors(self):
		return self.outgoingLinks


	def get_successorNode(self, path, pathPosition, reverse=False):
		nextNode=None
		nextNodeStart=0
		for successor in self.outgoingLinks:
			if path in successor.get_rightSegment().get_pathDict():
				for position in successor.get_rightSegment().get_path_positions(path):
					if reverse:
						if pathPosition==position+successor.get_rightSegment().get_sequence_length():
							nextNode=successor.get_rightSegment()
							nextNodeStart=position
					else:
						if pathPosition+self.get_sequence_length()==position:
							nextNode=successor.get_rightSegment()
							nextNodeStart=position
		return nextNode, nextNodeStart




	def add_incomingLink(self, linkObject):
		self.incomingLinks.append(linkObject)
		return None


	def add_outgoingLink(self, linkObject):
		self.outgoingLinks.append(linkObject)
		return None


	def build_links(self):
		linkList=[]
		for link in self.outgoingLinks:
			linkList.append(link.get_linkLine())
		return linkList


	def is_repeat(self):
		repeat=False
		for path in self.pathDict:
			if len(self.pathDict[path])!=1:
				repeat=True
				break
		return repeat


	def has_cycle(self, pathID):
		if len(self.pathDict[pathID])!=1:
			return True
		else:
			return False


	def has_path(self, pathID):
		if pathID in self.pathDict.keys():
			return True
		else:
			return False


	def has_ecotype(self, ecotypeBase):
		ecotype=False
		for path in self.pathDict.keys():
			if ecotypeBase==path.split('_')[0]:
				ecotype=True
		return ecotype


	def get_pathNumber(self):
		pathNumber=0
		for path in self.pathDict:
			pathNumber+=len(self.pathDict[path])
		return pathNumber			


	def get_ecotypeNumber(self):
		ecotypes=set([])
		for path in self.pathDict:
			ecotypes.add(path.split('_')[0])
		return len(list(ecotypes))


	def get_traversalNumber(self):
		traversalNumber=0
		for path in self.pathDict:
			traversalNumber+=len(self.pathDict[path])
		return traversalNumber


	def get_leftAnchor(self):
		return self.leftAnchor


	def add_leftAnchor(self, anchor):
		self.leftAnchor.append(anchor)


	def get_rightAnchor(self):
		return self.rightAnchor


	def add_rightAnchor(self, anchor):
		self.rightAnchor.append(anchor)


	def add_bubble(self, bubble):
		self.bubbleList.append(bubble)


	def get_bubbleList(self):
		return self.bubbleList
