#!/usr/bin/env python

class Link():

	def __init__(self, leftSegment, leftOrientation, rightSegment, rightOrientation, CIGAR):
		self.leftSegment=leftSegment
		self.leftSegmentOrientation=leftOrientation
		self.rightSegment=rightSegment
		self.rightSegmentOrientation=rightOrientation
		self.CIGAR=CIGAR
		self.pathList=[]
		return None


	def add_path(self, path):
		self.pathList.append(path)
		return None


	def get_pathList(self):
		return self.pathList


	def get_leftSegment(self):
		return self.leftSegment


	def get_leftOrientation(self):
		return self.leftSegmentOrientation


	def get_rightSegment(self):
		return self.rightSegment


	def get_rightOrientation(self):
		return self.rightSegmentOrientation


	def get_linkLine(self):
		return '\t'.join(['L', self.leftSegment.get_id(), self.leftSegmentOrientation, self.rightSegment.get_id(), self.rightSegmentOrientation, self.CIGAR])
