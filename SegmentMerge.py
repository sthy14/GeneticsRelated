#Tetrads Recombination
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

    def __str__(self):
        res = ''
        res += self.id + ':(' + str(self.start) + ',' + str(self.end) + ')'
        return res

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

    def __str__(self):
        res = ''
        for merged in self.results:
            for segment in merged.segments:
                res += str(segment) + ','
            res += '\n'
        
        return res
    
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
            print(merged.segments[-1])
            print('to merge:')
            print(tomerge)
            sortedsegnostart.remove(tomerge)
            merged.segments.append(tomerge)
        
    if len(sortedsegments) > 0:
        mergeresult.AppendConversion(sortedsegnostart)

    return mergeresult


def findNearestSeg(segment, sortedsegments):
    absdist = []
    filteredseg = []
    print('finding nearest for ')
    print(segment)
    print('in')
    
    for seg in sortedsegments:
        print(seg)
        if not (seg.start < segment.start or seg.end < segment.end):
            filteredseg.append(seg)

    for seg in filteredseg:
        dist = abs(segment.end - seg.start)
        absdist.append(dist)

    minpos = absdist.index(min(absdist))
    return filteredseg[minpos]


def ReadSegmentsCSV(filename):
    segments = []
    with open(filename, 'r') as file:
        lines = file.readlines()[1:]
    lines = [l.strip() for l in lines]

    for line in lines:
        parts = line.split(',')
        parts = [p.strip('\"') for p in parts]
        geneseg = GeneSegment(parts[1], int(parts[2]), int(parts[3]))
        segments.append(geneseg)
    
    return segments
    

def OutputResult(prefix):
    file1name = prefix + '_F1.csv'
    file2name = prefix + '_NA.csv'
    segments1 = ReadSegmentsCSV(file1name)
    segments1.sort()
    result1 = MergeSegments(segments1)
    segments2 = ReadSegmentsCSV(file2name)
    segments2.sort()
    result2 = MergeSegments(segments2)
    costat = { 'A': 0, 'B': 0, 'C': 0, 'D': 0}
    res1cocount = len(result1.results) - 1
    if res1cocount > 0:
        for id in range(res1cocount):
            partlength = len(result1.results[id]) - 1
            if partlength > 1:
                for pos in range(partlength):
                    if result1.results[id].segments[pos].id != result1.results[id].segments[pos + 1].id:
                        costat[result1.results[id].segments[pos].id] += 1
                        costat[result1.results[id].segments[pos].id + 1] += 1

    coresult = prefix + ','
    # write result
    foutcrossover = open('crossoverstat.csv', 'a')
    foutconversion = open('conversion.csv', 'a')

y12segs = []

#y12segs.append(GeneSegment('A', 27051, 126600))
#y12segs.append(GeneSegment('A', 129476, 132005))
#y12segs.append(GeneSegment('A', 194781, 197996))
#y12segs.append(GeneSegment('B', 135827, 138160))
#y12segs.append(GeneSegment('C', 50270, 195585))
#y12segs.append(GeneSegment('D', 27051, 49114))
#y12segs.append(GeneSegment('D', 133361, 197996))

y12segs.append(GeneSegment('A',126656,129075))
y12segs.append(GeneSegment('A',132468,194626))
y12segs.append(GeneSegment('B',	27141,135417))
y12segs.append(GeneSegment('B',	138806,197996))
y12segs.append(GeneSegment('C',27141,50024))
y12segs.append(GeneSegment('C',196113,197996))
y12segs.append(GeneSegment('D',49247,133198))
y12segs.sort()


