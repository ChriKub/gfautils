#!/usr/bin/env python

class Segment():

	def __init__(self, segmentLine):
		self.id=segmentLine.split('\t')[1]
		self.sequence=segmentLine.split('\t')[2]
		self.pathDict={}
		self.incomingLinks=[]
		self.outgoingLinks=[]
		
		return None


	def get_id(self):
		return self.id


	def get_sequence(self):
		return self.sequence


	def get_sequence_length(self):
		return len(self.sequence)


	def fill_pathDict(self, pathId, position):
		if pathId in self.pathDict:
			self.pathDict[pathId].append(position)
		else:
			self.pathDict[pathId]=[position]


	def get_pathDict(self):
		return self.pathDict


	def get_path_positions(self, pathId):
		return self.pathDict[pathId]


	def get_predecessors(self):
		return self.incomingLinks


	def get_successors(self):
		return self.outgoingLinks


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
