#!/usr/bin/env python

class Path():

	def __init__(self, pathID, pathList, cigarList):
		self.pathID=pathID
		self.pathList=pathList.split(',')
		self.cigarList=cigarList.split(',')
		self.positionDict={}
		return None


	def get_id(self):
		return self.pathID


	def get_pathList(self):
		return self.pathList


	def get_cigarList(self):
		return self.cigarList


	def build_path(self):
		path=['P', self.pathID]
		path.append(','.join(self.get_pathList()))
		path.append(','.join(self.get_cigarList()))
		return path


	def fill_positionDict(self, position, segmentObject):
		for i in range(position, position+segmentObject.get_sequence_length(), 1):
			self.positionDict[i]=segmentObject
		return None


	def get_positionDict(self):
		return self.positionDict


	def get_position(self, position):
		return self.positionDict[position]


	def change_pathList(self, pathList, cigarList=None):
		self.pathList=pathList
		if cigarList:
			self.cigarList=cigarList
		return None


