
def removeDuplicates(seq,idfun=None):
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result

def initialize1DList(VALUE,A):
    return [VALUE for i in range(A)]

def initialize2DList(VALUE,A,B):
    return [[VALUE for i in range(B)] for j in range(A)]
    #return [ [VALUE]*A for i in range(B) ]

def initialize3DList(VALUE,A,B,C):
    return [[[VALUE for i in range(C)] for j in range(B)] for k in range(A)]

def initialize4DList(VALUE,A,B,C,D):
    return [[[[VALUE for i in range(D)] for j in range(C)] for k in range(B)] for l in range(A)]
#

def CMISS_intStringToArray(String):
	StringArray = String.split(',')
	Data = []
	for value in StringArray:
		if value.find('..')>-1:
			temp = value.split('..')
			temp2 = range(int(temp[0]),int(temp[1])+1)
			[Data.append(point) for point in temp2]
		else:
			Data.append(int(value))
	return Data
