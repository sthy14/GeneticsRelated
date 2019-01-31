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
        return self.id == another.id and self.start == another.start and self.end == another.end

class MergedSegment:
    def __init__(self):
        self.segments = []

    def AddSegment(self, genesegment):
        self.segments.append(genesegment)

    def RemoveSegment(self, genesegment):
        self.segments.remove(genesegment)

class SegmentResult:
    def __init__(self):
        self.results = []
        return
    
    def AddSegStart(self, segment):
        segstart = MergedSegment()
        segstart.AddSegment(segment)
        self.results.append(segstart)
    
    def AppendSegment(self, segmenttoadd, segment):
        for mergedseg in results:
            if segment in mergedseg:
                mergedseg.AddSegment(segmenttoadd)

    def AppendConversion(self, listofseg):
        conversions = MergedSegment()
        for segment in listofseg:
            conversions.AddSegment(segment)
        self.results.append(conversions)
    
def MergeSegments(sortedsegments):
    segstart = min(sortedsegments).start
    segend = max(sortedsegments).end
    #print(segstart)
    #print(segend)

    mergeresult = SegmentResult()
    for segment in sortedsegments:
        if segment.start == segstart:
            mergeresult.AddSegStart(segment)
        
    sortedsegnostart = [seg for seg in sortedsegments if seg.start != segstart]

    for merged in mergeresult.results:
        while merged.segments[-1].end != segend:
            tomerge = findNearestSeg(merged.segments[-1], sortedsegnostart)
            print('seg remaining')
            print(len(sortedsegnostart))
            print('current end: ')
            print(merged.segments[-1].id)
            print(merged.segments[-1].start)
            print(merged.segments[-1].end)
            print('to merge:')
            print(tomerge.id)
            print(tomerge.start)
            print(tomerge.end)
            sortedsegnostart.remove(tomerge)
            merged.segments.append(tomerge)
        
    if len(sortedsegments) > 0:
        mergeresult.AppendConversion(sortedsegnostart)

    return mergeresult


def findNearestSeg(segment, sortedsegments):
    absdist = []
    filteredseg = []
    print('finding nearest for ')
    print(segment.id)
    print(segment.start)
    print(segment.end)
    print('in')
    
    for seg in sortedsegments:
        print(seg.id)
        print(seg.start)
        print(seg.end)
        if not (seg.start < segment.start or seg.end < segment.end):
            filteredseg.append(seg)

    for seg in filteredseg:
        dist = abs(segment.end - seg.start)
        absdist.append(dist)

    minpos = absdist.index(min(absdist))
    return filteredseg[minpos]


y12segs = []

y12segs.append(GeneSegment('A', 27051, 126600))
y12segs.append(GeneSegment('A', 129476, 132005))
y12segs.append(GeneSegment('A', 194781, 197996))
y12segs.append(GeneSegment('B', 135827, 138160))
y12segs.append(GeneSegment('C', 50270, 195585))
y12segs.append(GeneSegment('D', 27051, 49114))
y12segs.append(GeneSegment('D', 133361, 197996))

y12segs.sort()

testmerge = MergeSegments(y12segs)

testmerge.results[0].segments[0].id
testmerge.results[0].segments[1].id
testmerge.results[0].segments[2].id
testmerge.results[1].segments[0].id
testmerge.results[1].segments[1].id
testmerge.results[1].segments[2].id
testmerge.results[2].segments[0].id
testmerge.results[2].segments[1].id