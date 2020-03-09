#!/usr/bin/env python


from gfa import gfaHandler



class Bubble():

	def __init__(self, bubbleLine):
		self.start=bubbleLine.split('\t')[0]
		self.stop=bubbleLine.split('\t')[1]
		self.type=bubbleLine.split('\t')[3]
		self.variantList=bubbleLine.split('\t')[2].split(',')[1:-1]


	def get_start(self):
		return self.start


	def get_stop(self):
		return self.stop


	def get_variantList(self):
		return self.variantList


	def get_variant_number(self):
		return len(self.variantList)


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
