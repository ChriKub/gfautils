#!/usr/bin/env python


class Bubble():

	def __init__(self, leftAnchor, rightAnchor, segmentList, bubbleType):
		self.leftAnchor=leftAnchor
		leftAnchor.add_leftAnchor(self)
		self.rightAnchor=rightAnchor
		rightAnchor.add_rightAnchor(self)
		self.segmentList=segmentList
		self.pathDict={}
		self.traversalList=[]
		self.keeperTraversal=None
		self.build_traversals()
		self.bubbleType=self.calculate_bubbleType()


	def get_Anchors(self):
		return self.leftAnchor, self.rightAnchor


	def get_leftAnchor(self):
		return self.leftAnchor


	def get_rightAnchor(self):
		return self.rightAnchor


	def get_segmentList(self):
		return self.segmentList


	def get_traversing_path(self):
		return self.leftAnchor.get_pathDict()


	def get_type(self):
		return self.type


	def is_indel(self):
		variantPathNumber=0
		for segment in self.segmentList:
			variantPathNumber+=segment.get_pathNumber()			
		if variantPathNumber==self.leftAnchor.get_pathNumber():
			return False
		else:
			return True


	def build_traversals(self):
		pathDict={}
		for path in self.leftAnchor.get_pathDict():
			for pathPosition in self.leftAnchor.get_pathDict()[path]:
				completeTraversal=False
				reverseTraversal=False
				brokenTraversal=False
				currentNode=self.leftAnchor
				currentNodePosition=pathPosition
				segmentList=[]
				nextNode=None
				while nextNode!=self.rightAnchor:
					nextNode, nextNodeStart=currentNode.get_successorNode(path, currentNodePosition, reverseTraversal)
					if nextNode==self.rightAnchor:
						completeTraversal=True
						if len(segmentList)!=0:
							segmentList.append(reverseTraversal)
						else:
							segmentList=['InDel', False]
					elif not nextNode:
						if reverseTraversal:
							brokenTraversal=True
							break
						if len(segmentList)==0:
							reverseTraversal=True
							currentNode=self.leftAnchor
							currentNodePosition=pathPosition
						else:
							brokenTraversal=True
							break
					elif not brokenTraversal:
						segmentList.append(nextNode)
						currentNode=nextNode
						currentNodePosition=nextNodeStart
				if completeTraversal:
					if path in pathDict.keys():
						pathDict[path].append(segmentList)
					else:
						pathDict[path]=[segmentList]
		self.process_traverals(pathDict)
		return None


	def process_traverals(self, pathDict):
		traversalDict=self.join_traversals(pathDict)
		for traversal in traversalDict:
			traversalObject=Traversal(traversalDict[traversal][1:], traversalDict[traversal][0][:-1], traversalDict[traversal][0][-1])
			self.traversalList.append(traversalObject)
			for path in traversalDict[traversal][1:]:
				if path[0] in list(self.pathDict.keys()):
					self.pathDict[path[0]].append([traversalObject, path[1]])
				else:
					self.pathDict[path[0]]=[[traversalObject, path[1]]]
		return None


	def join_traversals(self, pathDict):
		traversalDict={}
		for path in pathDict:
			for traversal in pathDict[path]:
				reverse=False
				if traversal[-1]==True:
					traversal.reverse()
					traversal=traversal[1:]
					travesal.append(True)
				if str(traversal[:-1]) in traversalDict:
					traversalDict[str(traversal[:-1])].append([path, traversal[-1]])
				else:
					traversalDict[str(traversal[:-1])]=[traversal, [path, traversal[-1]]]
		return traversalDict


	def calculate_bubbleType(self):
		bubbleType=None
		longestTraversal=0
		shortestTraversal=1000000000000000000000
		for traversalObject in self.traversalList:
			if len(traversalObject.get_segmentList())>longestTraversal:
				longestTraversal=len(traversalObject.get_segmentList())
			if len(traversalObject.get_segmentList())<shortestTraversal:
				shortestTraversal=len(traversalObject.get_segmentList())
		if shortestTraversal!=0:
			if longestTraversal>1:
				return 'complex'
			elif longestTraversal==1:
				return 'simple'
		else:
			if longestTraversal>1:
				return 'complexIndel'
			elif longestTraversal==1:
				return 'simpleIndel'


	def get_pathTraversals(self, path):
		if path in self.pathDict:
			return self.pathDict[path]
		else:
			return None


	def find_keeperTraversal(self, refBase, maxLength):
		hasRef=None
		potentialTraversals=[]
		for path in self.pathDict:
			if path.split('_')[0]==refBase:
				hasRef=True
				potentialTraversals.extend(self.pathDict[path])
		if not potentialTraversals:
			potentialTraversals=self.get_most_common_traversals()
		if len(potentialTraversals)==1:
			self.keeperTraversal=potentialTraversals[0]
		elif len(potentialTraversals)>1:
			traversalLength=0
#			for traversal in potentialTraversals:
#				traversalObject=traversal[0]
#				if traversalNumber<traversalObject.get_traversalNumber():
#					self.keeperTraversal=traversalObject
#					traversalNumber=traversalObject.get_traversalNumber()
#					traversalLength=traversalObject.get_traversalLength()
#				elif traversalNumber==traversalObject.get_traversalNumber():
#					if traversalLength<traversalObject.get_traversalLength():
#						self.keeperTraversal=traversalObject
#						traversalNumber=traversalObject.get_traversalNumber()
#						traversalLength=traversalObject.get_traversalLength()
		return None


	def get_keeperTraversal(self):
		return self.keeperTraversal


	def get_most_common_traversals(self):
		commonTraversalList=[]
		commonTraversalPath=0
		for traversalObject in self.traversalList:
			if len(traversalObject.get_pathDict())>commonTraversalPath:
				commonTraversalList=[traversalObject]
			elif len(traversalObject.get_pathDict())==commonTraversalPath:
				commonTraversalList.append(traversalObject)
		return commonTraversalList


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
