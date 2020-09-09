# gfautils

A package to read and modify gfa files.

This package encodes a data structure that allows access to gfa files.

## Quick start-up:

Install:

	python setup.py install

Loading a gfa:

	from gfa import gfaHandler

	file=open(inpath, 'r')
	input=file.read()
	file.close()
	
	gfaFile = gfaHandler(input)

	gfaFile.build_gfa()

###Accessing the data in a the gfa:

#### Class: GFA

* segmentDict: _{segmentID: segmentObject,...}_
* pathDict: _{pathName: pathObject,...}_
* linkList: _[linkObject,...]_
* bubbleDict: _{coreNumber: [bubbleObject,...]}_
* bubbleList: _[bubbleObject,...]_

	get_segmentDict()

Returns the full segmentDict.

	get_segment(segmentID)

Returns the segmentObject assigned to _segmentID_ in the Dict..

	get_segments()

Returns all segmentIDs

	add_segment(segmentLine)

Adds a new segment to the segmentDict. _segmentLine_ has the format of a gfa segment line.


	get_segmentList()

Returns all segments in the segmentDict in gfa format.

	get_pathDict()

Returns the pathDict.

	get_path(pathName)

Returns the pathObject assigned to pathName in the pathDict.

	get_paths()

Returns all pathNames.

	change_pathList(pathName, pathList)

Replaces the node order list of the pathObject with the id _pathName_ with _pathList_.

	get_pathList()

Returns all path in standard gfa format.

	get_linkList()

Returns a list of all linkObjects.

#### Class: Segment

* id: _str_
* sequence: _str_
* pathDict: _{pathName: [pathPosition,...],...}_
* incomingLinks: _linkObject_
* outgoingLinks: _linkObject_
* leftAnchor: _bubbleObject_
* rightAnchor: _bubbleObject_

Segment objects are stored in a dictionary and can be accessed using their segment id. The same ID used in the gfa file

	gfaFile.get_segmentDict()

Returns the complete segment dictionary. {segmentID: segmentObject, ...}

	gfaFile.get_segments()

Returns a list of segment ids

	self.get_segment(str(segmentId))

Returns the segment object with the given segment id.

#### Accessing Segment Data

	segment.get_id()

Returns the segment id.

	segment.get_sequence()
	segment.set_sequence(newSequence)
	segment.get_sequence_length()

Returns or changes the sequence, or the length of the segment.

	segment.get_pathList()

Returns a list of al paths traversing this segment

	segment.get_pathDict()

Returns a dictionary of all paths traversing this segment that contains the positions of the segment within the path.

	segment.is_unique()

Returns `TRUE` if the segment is traversed by only one path.

### Paths

	self.get_pathDict()

Returns a dictionary of path names and their path objects

	self.get_paths()

Returns a list of path names that where present in the gfa.

	self.get_path(str(pathID))

Returns the path object with the given pathID.

#### Accessing Path Data

A path is stored in dictionary of float numbers that specify the position in the path.

	path.pathDict[float(position)]=[segmentID, strand, CIGAR]

	path.get_id()

Returns the id of the path object.

	path.get_pathDict()

Returns the path dictionary in which path information is stored by their position in the path. 'path.pathDict[float(position)]=[segmentID, strand, CIGAR]'

	path.get_pathList()

Returns a list of nodes and strands [1+,2-,3+,...] ordered by their occurence in the path.

	path.get_position()

Returns the segmentID, strand and CIGAR for this position in the path.

# **Class: Bubble**

* bubbleID: <str>
* leftAnchor: <segmentObject>
* rightAnchor: <segmentObject>
* segmentSet: {segmentIDs}
* coreNumber: <int> (first core size for which the bubble has been detected)
* parent: <bubbleObject> (None if top bubble)
* subBubbles: [bubbleObjects]

## Methods:
> *get_bubbleID()*
> returns the ID string of the bubble

> *get_Anchors()*
> returns both anchors as segmentObjects: leftAnchor, rightAnchor

> *get_leftAnchor()*
> returns the leftAnchor as segmentObject

> *get_rightAnchor()*
> returns the rightAnchor as segmentObject

> *get_segmentSet()*
> returns a set of all segmentIDs that are part of this bubble

> *find_subBubble(bubbleID: <str>, leftAnchor: <segmentObject>, rightAnchor: 
<segmentObject>, traversalSet: <set>, coreNumber: <int>)
> Returns a existing sub bubble that fits the current traversal, if non can be 
found **None**

> *get_subBubbles()*
> Returns a list of all bubbleObjects that are assigned as sub bubbles.

> *add_segments(segmentList: <list>)*
> Adds all segmentIDs in the segmentList to the bubbles segmentSet

> *add_traversal(pathName: <string>, segmentList: <list>)*
> Adds a new traversalObject to this bubble, or if this traversal already exists 
adds the path to the existing traversal

> *get_traversalList()*
> Returns a list of all traversalObjects attached to the bubbleObject

> *add_subBubble(subBubble: <bubbleObject>)*
> Adds the new subBubble to the bubbles subBubbleList.

# Contact

<christian.kubica@tuebingen.mpg.de>

