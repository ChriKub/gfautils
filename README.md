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
	
	gfaFile = gfaHandler(input: _str_)

	gfaFile.build_gfa()

###Accessing the data in a the gfa:

#### Class: GFA

* segmentDict: _{segmentID: segmentObject,...}_
* pathDict: _{pathID: pathObject,...}_
* linkList: _[linkObject,...]_
* bubbleDict: _{coreNumber: [bubbleObject,...]}_
* bubbleList: _[bubbleObject,...]_

Creating the a _gfaObject_.

	GFA(GFAfile: _str_)

##### Methods:

	get_segmentDict()

Returns the full segmentDict.

	get_segment(segmentID: _str_)

Returns the segmentObject assigned to _segmentID_ in the Dict..

	get_segments()

Returns all segmentIDs

	add_segment(segmentLine: _str_)

Adds a new segment to the segmentDict. _segmentLine_ has the format of a gfa segment line.

	get_segmentList()

Returns all segments in the segmentDict in gfa format.

	get_pathDict()

Returns the pathDict.

	get_path(pathID: _str_)

Returns the pathObject assigned to pathID in the pathDict.

	get_paths()

Returns all pathIDs.

	change_pathList(pathID: _str_, pathList: _list_)

Replaces the node order list of the pathObject with the id _pathID_ with _pathList_.

	get_pathList()

Returns all path in standard gfa format.

	get_linkList()

Returns a list of all linkObjects.

	get_bubbleDict()

Returns a dictionary with all bubbles. Keys in the dictionary are the number of ecotypes traversing the anchor bubble. 

	get_bubbleList()

Returns a list of all bubbleObjects.

	add_bubble(leftAnchor: _segmentObject_, rightAnchor: _segmentObject_, segmentList: _list_, coreNumber: _int_, parent: _bubbleObject/None_)

Creates a new bubble object and adds it to the bubbleList and to the bubbleDict.

	has_bubble(segmentList: _list_, leftAnchorNode: _segmentObject_, rightAnchorNode: _segmentObject_)

Tries to find a existing bubble that is either the correct bubble, or the closest existing parentbubble.

	build_gfa(header: _str/None_)

Returns all data stored in this class as a full gfa file. If a header is given it is appended to the standard gfa header line.

	rebuild_gfa(header: _str/None_)

Returns a gfa file based on the data given in the path. Only nodes that are in the existig paths and links that are described there are written into the file, or created for this purpose. If a header is given it is appended to the standard gfa hearder line.



#### Class: Segment

* id: _str_
* sequence: _str_
* pathDict: _{pathID: [pathPosition,...],...}_
* incomingLinks: _linkObject_
* outgoingLinks: _linkObject_
* leftAnchor: _bubbleObject_
* rightAnchor: _bubbleObject_
* bubbleList: '_[bubbleObject]_'

Creating the a _segmentObject_.

	Segment(SegmentLine: _str_)


##### Methods:

	get_id()

Returns the segmentID.

	get_sequence()

Returns the segments Sequence.

	get_sequence_length()

Returns the the length of the sequence assigned to the segment object.

	fill_pathDict(pathID: _str_, position: _int_)

Adds the position this segment has in the path to the pathDict.

	get_pathDict()

Returns the pathDict with all pathPositions of this segment.

	get_ecotypeList()

Returns a list of all traversed ecotypes.

	get_path_positions(pathID: _str_)

Returns all positions this segment has in the path.

	remove_from_pathDict(pathID: _str_, pathPosition: _int_)

Removes the entry of pathPosition from the pathDict.

	get_predecessors()

Returns a list of all incoming linkObjects.

	get_predecessorNode(pathID: _str_, pathPosition: _int_)

Returns the predecessor segmentObject and start position of this segment based on the path and position given to the function.

	get_successors()

Returns a list of all outgoing linkObjects.

	get_successorNode(pathID: _str_, pathPosition: _int_, reverse: _bool/False_)

Returns the successor segmentObject and start position of this segment based on the path and position given to this function.

	add_incomingLink(linkObject: _linkobject_)

Adds a new linkObject to the predecessors.

	add_outgoingLink(linkObject: _linkObject_)

Adds a new linkObject to the successors.

	build_links()

Returns the links for this segment in gfa format.

	is_repeat()

Returns _True_ if at least on path traverses this segment twice.

	has_cycle(pathID: _str_)

Returns _True_ if the specified path traverses the segment at least twice.

	has_path(pathID: _str_)

Returns _True_ if the specified path traverses this segment at least once.

	has_ecotype(ecotypeBase: _str_)

Returns _True_ if the segment is traversed by any path that has this ecotypeBase. (PathID=EcotypeBase_contigID e.g. TAIR10_Chr1)

	get_pathNumber()

Returns the total number of traversals through this segment.

	get_ecotypeNumber()

Returns the number of different ecotypes that traverse through this segment.

	get_traversalNumber()

Returns the number of times the segment is being traversed.

	get_leftAnchor()

Returns a _list_ of all bubbleObjects for which this segment is a left anchor.

	add_leftAnchor(anchor: _bubbleObject_)

Adds a new bubbleObject for which this segment is a left anchor.

	get_rightAnchor()

Returns a _list_ of all bubbleObjects for which this segment is a right anchor.

	add_rightAnchor(anchor: _bubbleObject_)

Adds a new bubbleObject for which this segment is a right anchor.

	add_bubble(bubble: _bubbleObject_)

Adds a new bubbleObject that this segment is part of to the bubbleList.

	get_bubbleList()

Returns _list_ of all bubbleObjects that this segment is part of


#### Class: Link

* leftSegment: _segmentObject_
* leftSegmentOrientation: _str_ (+/-)
* rightSegment: _segmentObject_
* rightSegmentOrientation: _str_ (+/-)
* CIGAR: _str_
* pathList: _list_

Creating the a _linkObject_.

	Link(leftSegment: _segmentObject_, leftOrientation: _str_, rightSegment: _segmentObject_, rightOrientation: _str_, CIGAR: _str_)

##### Methods:


#### Class: Path

* pathID: _str_
* pathList: _list_
* cigarList: _list_

Creating the a _pathObject_.

	Path(pathID: _str_, pathList: _str_, cigarList: _str_)

##### Methods:


#### Class: Bubble

* bubbleID: _str_
* leftAnchor: _segmentObject_
* rightAnchor: _segmentObject_
* segmentSet: _{segmentIDs}_
* coreNumber: _int_ (first core size for which the bubble has been detected)
* parent: _bubbleObject_ (None if top bubble)
* subBubbles: _[bubbleObjects]_

Creating the a _bubbleObject_.

	Bubble(bubbleID: _str_, leftAnchor: _segmentObject/None_, rightAnchor: _segmentObject/None_, segmentList: _list_, coreNumber: _str_, parent: _bubbleObject_)


##### Methods:

	get_bubbleID()

Returns the ID string of the bubble.

	get_Anchors()

Returns both anchors as _segmentObjects_: leftAnchor, rightAnchor.

	get_leftAnchor()

Returns the leftAnchor as _segmentObject_.

	get_rightAnchor()

Returns the rightAnchor as_ segmentObject_.

	get_segmentSet()

Returns a set of all segmentIDs that are part of this bubble

	find_subBubble(bubbleID: _str_, leftAnchor: _segmentObject_, rightAnchor: _segmentObject_, traversalSet: _set_, coreNumber: _int_)

Returns a existing sub bubble that fits the current traversal, if non can be found _None_.

	get_subBubbles()

Returns a list of all _bubbleObjects_ that are assigned as sub bubbles.

	add_segments(newSegments: _list_)

Adds all segmentIDs in the _segmentList_ to the bubbles segmentSet.

	add_traversal(pathName: _string_, segmentList: _list_)

Adds a new _traversalObject_ to this bubble, or if this traversal already existsadds the path to the existing traversal.

	get_traversalList()

Returns a list of all _traversalObjects_ attached to the_ bubbleObject_.

	add_subBubble(subBubble: _bubbleObject_)

Adds the _bubbleObject_ as sub bubble.


#### Class: Traversal

* pathList: _list_
* segmentList: _list_

Creating the a traversalObject_.

	Traversal(segmentList: _list_, path: _list_)

##### Methods:

	add_path(path: _list_)

Adds the path [pathID, startposition, stopPosition] to the objects pathList.

	get_pathList()

Returns the pathList of all paths going through this traversal.

	get_segmentList()

Returns the segmentList that contains all the segmentIDs and their orientation on the correct order that make up this traversal.

















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
