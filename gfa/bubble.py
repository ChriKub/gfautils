#!/usr/bin/env python


class Bubble():

	def __init__(self, leftAnchor, rightAnchor, segmentList, bubbleType):
		self.leftAnchor=leftAnchor
		self.rightAnchor=rightAnchor
		self.segmentList=segmentList
		self.bubbleType=bubbleType


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


	def contains_src(self, src):
		contains=False
		for variant in self.variantList:
			for traversingSrc in variant.get_pathList():
				if traversingSrc==src:
					contains=True
		return contains


	def get_traversals(self):
		traversalList=[]
		for variant in self.variantList:
			traversalList.append(variant.get_passes())
		return traversalList


class Variant():

	def __init__(self, id):
		self.id=id
		self.passes=0
		self.pathList=[]


	def add_pass(self):
		self.passes+=1
		return None


	def add_path(self, path):
		self.pathList.append(path)
		return None


	def get_id(self):
		return self.id


	def get_passes(self):
		return self.passes


	def get_pathList(self):
		return self.pathList


	def is_traversed(self, src):
		for path in self.pathList:
			if path==src:
				return True
		return False
