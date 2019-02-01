#Tetrads Recombination
class GeneSegment:
    def __init__(self, _id, _start, _end, _parent):
        self.id = _id
        self.start = _start
        self.end = _end
        self.parent = _parent

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
        res += self.id + ',' + self.parent + ',' + str(self.start) + ',' + str(self.end)
        return res

class MergedSegment:
    def __init__(self):
        self.segments = []

    def AddSegment(self, genesegment):
        self.segments.append(genesegment)

    def RemoveSegment(self, genesegment):
        self.segments.remove(genesegment)

    def __str__(self):
        res = ''
        for segment in self.segments:
            res += segment.id
        return res

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
        for mergedsegment in self.results:
            partlength = len(mergedsegment.segments) - 1
            if partlength > 0:
                for pos in range(partlength):
                    currseg = mergedsegment.segments[pos]
                    nextseg = mergedsegment.segments[pos + 1]
                    if currseg.id != nextseg.id and nextseg.start < currseg.end:
                        convseg = GeneSegment(nextseg.id, nextseg.start, currseg.end, currseg.parent)
                        conversions.AddSegment(convseg)
        self.results.append(conversions)

    def GetResultStr(self):
        resstr = []
        rescount = len(self.results) - 1
        for pos in range(rescount):
            resstr.append(str(self.results[pos]))
        return resstr

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


def ReadSegmentsCSV(prefix, parentname):
    filename = prefix + '_' + parentname + '.csv'
    segments = []
    with open(filename, 'r') as file:
        lines = file.readlines()[1:]
    lines = [l.strip() for l in lines]

    for line in lines:
        parts = line.split(',')
        parts = [p.strip('\"') for p in parts]
        geneseg = GeneSegment(parts[1], int(parts[2]), int(parts[3]), parentname)
        segments.append(geneseg)
    
    return segments
    
def CalculateCrossover(segmentresult, costat):
    rescocount = len(segmentresult.results) - 1
    if rescocount > 0:
        for id in range(rescocount):
            partlength = len(segmentresult.results[id].segments) - 1
            if partlength > 0:
                for pos in range(partlength):
                    if segmentresult.results[id].segments[pos].id != segmentresult.results[id].segments[pos + 1].id:
                        #costat[segmentresult.results[id].segments[pos].id] += 1
                        costat[segmentresult.results[id].segments[0].id] += 1

def OutputResult(prefix):
    segments1 = ReadSegmentsCSV(prefix, 'F1')
    segments1.sort()
    print('Processing ' + prefix + 'F1')
    result1 = MergeSegments(segments1)
    segments2 = ReadSegmentsCSV(prefix, 'NA')
    segments2.sort()
    print('Processing ' + prefix + 'NA')
    result2 = MergeSegments(segments2)
    costat = { 'A': 0, 'B': 0, 'C': 0, 'D': 0}
    CalculateCrossover(result1, costat)
    CalculateCrossover(result2, costat)

    resstr = result1.GetResultStr() + result2.GetResultStr()
    resstr.sort()

    coresult = prefix + ',' + resstr[0] + ',' + str(costat['A']) + ',' + resstr[1] + ',' + str(costat['B']) + ',' + resstr[2] + ',' + str(costat['C']) + ',' + resstr[3] + ',' + str(costat['D'])
    totalcount =  sum(costat.values())
    coresult += ',' + str(totalcount) + '\n'
    # write result
    foutcrossover = open('crossoverstat.csv', 'a')
    foutcrossover.write(coresult)
    foutconversion = open('conversion.csv', 'a')
    for segment in result1.results[-1].segments:
        convstr = prefix + str(segment) + '\n'
        foutconversion.write(convstr)
    for segment in result2.results[-1].segments:
        convstr = prefix + str(segment) + '\n'
        foutconversion.write(convstr)

# Example code:
#
# firstly put this file to the same folder as all tetrads, then open terminal in that folder, run:
# python -i ./SegmentMerge.py
#
# within python run:
# OutputResult('D01')
# the result would be created into two files, crossoverstat,csv and conversion.csv
#
# in order to run all files you could run something like:
# for i in range(1, 16):
#    filename = 'D%02d' % i
#    OutputResult(filename)
# this should run through all files between range 1..15
#
# the code cannot handle overlap at the moment
