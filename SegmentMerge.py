class GeneSegment:
    def __init__(self, _id, _start, _end):
        self.id = _id
        self.start = _start
        self.end = _end

    def __lt__(self, another):
        if (self.start < another.start):
            return True
        if (self.start == another.start):
            return self.end < another.end
        return False

    def __cmp__(self, another):
        if (self.start == another.start):
            return cmp(self.end, another.end)
        else:
            return cmp(self.start, another.start)

    def __eq__(self, another):
        return self.id == another.id

class MergedSegment:
    def __init__(self):
        self.segments = []

    def AddSegment(self, genesegment):
        self.segments.append(genesegment)

class SegmentResult:
    def __init__(self):
        self.results = []
    
    def AddSegStart(self, segment):
        segstart = MergedSegment
        segstart.AddSegment(segment)
        self.results.append(segstart)

    def MergeSegment(self, genesegment):


    
def MergeSegments(sortedsegments):
    segstart = min(sortedsegments).start
    segend = max(sortedsegments).end
    print(segstart)
    print(segend)

    mergedsegments = []
    while (sortedsegments):
        segment = min(sortedsegments)
        if (segment.start == segstart):
            mergedsegments.append()


y12segs = []
y12segs.append(GeneSegment('A', 27051, 126600))
y12segs.append(GeneSegment('A', 129476, 132005))
y12segs.append(GeneSegment('A', 194781, 197996))
y12segs.append(GeneSegment('A', 27051, 126600))
y12segs.append(GeneSegment('B', 135827, 138160))
y12segs.append(GeneSegment('C', 50270, 195585))
y12segs.append(GeneSegment('D', 27051, 49114))
y12segs.append(GeneSegment('D', 133361, 197996))

y12segs.sort()
